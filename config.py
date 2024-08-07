import os
frm dotenv import load_dotenv

# Load the environment variables from the .env file
def load_config():
    load_dotenv()

def get_groq_api_key():
    return os.getenv('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')
