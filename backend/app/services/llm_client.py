import time

from google import genai #need to first install the genai package using pip install google-genai
from app.config import settings #then need to import the settings from the config.py file to access the gemini_api_key

client = genai.Client(api_key=settings.gemini_api_key) #create a client object using the gemini_api_key from the settings

def generate(prompt, max_retries=5): #this means that we are defining a function called generate that takes in a prompt and a maximum number of retries as parameters
    for i in range(max_retries): #this means that we are trying to generate content for a maximum of max_retries times
        try:
            response = client.models.generate_content( #this means that we are using the generate_content method from the models module of the client object to generate content based on the prompt provided
                model = "gemini-flash-latest",
                contents = prompt,
                )
            return response.text
        except Exception as e:
            if i < max_retries - 1: #this means that if the current retry count is less than the maximum number of retries minus one, we will print a message indicating that the AI call failed and we will retry
                print(f"[llm_client] AI 调用失败: {e}, 正在重试...({i+1}/{max_retries})")
                time.sleep(2**i) #this means that we will wait for 2 seconds before retrying the AI call, and we will increment the retry count by 1
            else: #this means that if the current retry count is equal to the maximum number of
                print(f"[llm_client] AI 调用失败: {e}")
                raise                    # ← 关键:把错误继续往上抛
        
