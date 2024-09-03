import openai
from config import API_KEY, BASE_URL

def get_openai_client():
    return openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
