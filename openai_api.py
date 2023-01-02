import argparse
import openai
import os

# Get the current working directory
current_dir = os.getcwd()

script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct a file path relative to the script directory
file_path = os.path.join(script_dir, 'api_keys.txt')
# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('prompt', type=str, help='The prompt to generate text for')
parser.add_argument('--file', type=str, default=file_path, help='The name of the file to read')
args = parser.parse_args()

with open(args.file, 'r') as f:
    # Read the file line by line
    openai.organization = f.readline().strip()
    openai.api_key = f.readline().strip()

models = openai.Model.list()

# print(models)

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
