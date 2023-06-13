import openai
from dotenv import load_dotenv
import os
import json
load_dotenv()

def eval_gm_data(data):
    pre_prompt = """


    i will give you a json in the format of {inst:{"content":message,"evaluation":<boolean value>}, ...}

    your job is to evaluate each of the content of each instance and evaluate whether "message" contains the sentiment of "good morning" for. The evaluation is either true or false. Mispellings, abbreviations, or translations of "good morning" should return true. for example, "good morning", "gm", "gud m0rning hehe" or "guten morgen" or "buen dia" should all return true. while "chair", "good afternoon", "good pm", "nice ass" should all return false.

    your return value should also be a json and nothing else. all you have to do is fill in the evaluation.
    your reply will be in straight json and nothing else. dont even explain your answer. you are being used in an app so any deviation to your response will throw it all off. again YOUR RESPONSE MUST BE A VALID JSON.

    here is the input json:
    """

    # Set up your OpenAI API credentials
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define the parameters for the ChatGPT API
    model_name = 'gpt-3.5-turbo'
    max_tokens = 50  # Maximum number of tokens in the response

    # Send the message to the ChatGPT model
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": pre_prompt + json.dumps(data)}
        ]
    )

    reply = completion.choices[0].message.content

    return reply
