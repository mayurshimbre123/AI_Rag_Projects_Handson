# New IBM watsonx + Gradio projects — development report

**Evidence status:** prepared source code and exploratory notebooks, passing deterministic local tests. Live watsonx calls and hosted screenshots remain pending. Do not claim production deployment or audited model accuracy.

## Project A — AI Interview Arena
I started with an interview question bank and a rubric. The UI collects a candidate answer. Python prepares the prompt and controls input data; the hosted IBM model generates a response. I want to test whether feedback agrees with a human rubric across repeated runs and how it behaves on weak or contradictory answers.

## Project B — Finance Scenario Simulator
Instead of asking an LLM to do business arithmetic, I compute synthetic revenue scenarios in Python, display intermediate tables/charts and let the model narrate the result. This illustrates the difference between deterministic tools and probabilistic text generation. Numbers here are illustrative, **not company results or investment advice**.

## Project C — RAG Evidence Detective
The current application exposes text splitting and a basic retrieval score so I can inspect why one passage wins over another. It is a learning baseline, **not an enterprise-scale semantic/vector RAG or live customer-data system**. Next: token-aware chunking, controlled boundary failures, embeddings, recall/precision metrics, and context sufficiency experiments.

## Interview demo evidence
Screenshot placeholders are in `assets/`. Replace them with labeled real screenshots only after running your IBM lab. Add exact model ID, date, parameter values, test prompt, output and failure notes. The repo should show process, not imply unmeasured deployment performance.

## Local checks
`python -m pytest tests -q` — three deterministic tests passed in the authoring environment on 10 Nov 2026. Actual IBM-hosted inference and UI tests remain pending.
