from google import genai #need to first install the genai package using pip install google-genai
from app.config import settings #then need to import the settings from the config.py file to access the gemini_api_key

client = genai.Client(api_key=settings.gemini_api_key) #create a client object using the gemini_api_key from the settings

def generate(prompt):
    response = client.models.generate_content( #this means that we are using the generate_content method from the models module of the client object to generate content based on the prompt provided
        model = "gemini-flash-latest",
        contents = prompt,
    )
    return response.text

