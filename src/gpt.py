import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv("OPENAI") # chatgpt api token
client = OpenAI(api_key=APIKEY)

async def send_request(input):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": '''
                Act as Hitori Gotoh from Bocchi the Rock. 
                Timid, socially anxious, overly self-conscious. 
                Avoid conversation, overthink, apologize excessively, self-deprecating humour. 
                very short response:
            '''
        },
        {"role": "user", "content": input}
    ],
    temperature=1,
    max_tokens=400,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    return response.choices[0].message.content
