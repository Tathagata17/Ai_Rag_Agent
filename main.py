from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from service import retriever # <--- Imports directly from your vector.py file!

model = OllamaLLM(model="llama3.2")

template = """
You are a QA Lead and you are responsible for answering questions related to software testing.

Here are some test cases for which automation is present along with their tags: {test_cases}

Here is the acceptance criteria for the test cases for which you have to say which tag to run: {acceptance_criteria}

Please identify which tags should be run to cover this criteria.
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    question = input("Enter the acceptance criteria (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    # 1. Retrieve the matching test cases
    matched_docs = retriever.invoke(question)
    
    # 2. Format the matching test cases into a clean string block
    formatted_cases = ""
    for doc in matched_docs:
        formatted_cases += f"\n- ID: {doc.id}\n"
        formatted_cases += f"  Tags: {doc.metadata.get('tags')}\n"
        formatted_cases += f"  Description: {doc.page_content}\n"
    
    # 3. Ask your AI QA Lead
    result = chain.invoke({"test_cases": formatted_cases, "acceptance_criteria": question})
    print(result)