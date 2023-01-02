import argparse
import openai

with open('api_keys.txt', 'r') as f:
    # Read the file line by line
    openai.organization = f.readline().strip()
    openai.api_key = f.readline().strip()

models = openai.Model.list()

# print(models)
# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('prompt', type=str, help='The prompt to generate text for')
args = parser.parse_args()

# Use a model to generate text
model_engine = "text-davinci-003"
prompt = args.prompt

try:
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
except Exception as e:
    print(f"An error occurred: {e}")
else:
    data = completion.to_dict()
    choices = data['choices']
    first_choice = choices[0]
    text = first_choice['text']
    print(text)
