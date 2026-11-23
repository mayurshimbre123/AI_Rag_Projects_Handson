"""Small wrapper around the exact IBM watsonx client from the Skills Network lab.
Import lazily so offline unit tests do not require IBM credentials/packages.
"""
import os

MODEL_ID = os.getenv("WATSONX_MODEL_ID", "mistralai/mistral-small-3-1-24b-instruct-2503")

def generate(prompt: str, max_new_tokens: int = 350, temperature: float = 0.3) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    from langchain_ibm import WatsonxLLM
    llm = WatsonxLLM(
        model_id=MODEL_ID,
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params={GenParams.MAX_NEW_TOKENS: max_new_tokens,
                GenParams.TEMPERATURE: temperature},
    )
    return str(llm.invoke(prompt))
