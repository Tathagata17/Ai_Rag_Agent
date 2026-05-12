AI RAG Test Orchestrator Agent 🤖⚡
An intelligent, event-driven test automation runner that automatically maps Jira Acceptance Criteria (A.C.) to specific test automation suites using an AI Agent and Retrieval-Augmented Generation (RAG).

By listening to real-time updates via Jira Webhooks, the agent analyzes the requirement context, intelligently queries the available regression/sanity suite metadata, and dynamically triggers targeted Jenkins pipelines—providing instant, closed-loop feedback and reports back to Development and QA teams.

🚀 The Problem & Solution
The Bottleneck
Manually identifying and mapping which automation test suites need to run for a given Jira ticket's Acceptance Criteria is time-consuming, prone to human error, and introduces a delay in rapid CI/CD feedback loops.

The AI Solution
This project automates the entire lifecycle:

Trigger: Jira Webhook catches changes/transitions in issue Acceptance Criteria.

Context Retrieval (RAG): The AI Agent looks at the A.C. and queries a vectorized knowledge base containing your test suite descriptions, metadata, and step mappings.

Smart Decisioning: The LLM-backed Agent selects the optimal minimum-viable test suite(s) required to validate the feature.

Execution: The agent automatically calls the remote Jenkins API to trigger the builds.

Reporting: Feedback loops are closed by publishing compiled reports straight back to the stakeholders.
