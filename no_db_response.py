from openai import AzureOpenAI

endpoint = "https://aihub2565181539.openai.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"

subscription_key = "CnrQXBv16oAlU7kXdE8lXbeKVRlytn8bg55ae4fFm2wUjpz432FLJQQJ99BEAC77bzfXJ3w3AAAAACOG2x9F"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    
    
def no_db_fn(user_input):
    print('no_db_fn has been called')

    try:
        response = client.chat.completions.create(
            model=deployment,  # Use deployment name, not model name
            messages=[
                {"role": "system", "content": """
                 You are an AI assistant for a financial advisor.
                    
                    """},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        print("Chatbot:", response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Chatbot: Sorry, something went wrong.", str(e))
        return e