import os

from dotenv import load_dotenv

load_dotenv()

from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), os.getenv("AZURE_TOKEN_SCOPE")
)

seed = 1
llm_config = {
    "cache_seed": seed,
    "config_list": [
        {
            "model": os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            "api_type": "azure",
            "base_url": os.environ["AZURE_OPENAI_ENDPOINT"],
            "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
            "api_key": os.environ["AZURE_OPENAI_API_KEY"],
            # "azure_ad_token_provider": token_provider,
        }
    ],
}
