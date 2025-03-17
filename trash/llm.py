import os
from dotenv import load_dotenv
import yaml
from groq import Groq
from chatbot.groq_wrapper import GroqLangChainWrapper

API_KEY_GROQ = os.getenv('API_KEY_GROQ')
GROQ_MODEL_NAME = os.getenv('GROQ_MODEL_NAME')

load_dotenv()

def load_yaml_prompt(filepath: str) -> str:
    """
    Laster en .yaml-fil med en eller flere prompt-tekster.
    Returnerer streng eller dictionary, avhengig av format.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if isinstance(data, str):
        return data
    elif isinstance(data, dict) and 'prompt' in data:
        return data['prompt']
    else:
        return str(data)
    
def create_llm() -> GroqLangChainWrapper:
    groq_client = Groq(api_key=API_KEY_GROQ)
    llm = GroqLangChainWrapper(groq_client=groq_client, 
                               model_name=GROQ_MODEL_NAME
                               )
    return llm


def load_few_shot_prompts():
    few_shot = load_yaml_prompt('chatbot/prompts/few_shot.yaml')
    fix_prompt = load_yaml_prompt('chatbot/prompts/fix_prompt.yaml')
    return few_shot, fix_prompt