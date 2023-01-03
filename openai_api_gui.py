import PySimpleGUI as sg
import openai
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct a file path relative to the script directory
file_path = os.path.join(script_dir, 'api_keys.txt')

def clear_output():
    """Clear the output element"""
    # Get the output element
    output = window['output']
    # Clear the output
    output.update('')

# Create the GUI layout
layout = [
    [sg.Text('Enter the prompt:'), sg.InputText()],
    [sg.Text('Enter the file name:'), sg.InputText(default_text=file_path), sg.FileBrowse()],
    [sg.Button('Generate Text'), sg.Output(size=(100, 20), font=('Arial', 20))],
    [sg.Button('Clear Output')]
]

# Create the window
window = sg.Window('OpenAI API', layout, size=(1024, 720))

# Run the event loop
while True:
    # Get the event and values
    event, values = window.read()

    # Check if the button was clicked
    if event == 'Generate Text':
        # Get the values from the input fields
        prompt = values[0]
        file_name = values[1]

        # Open the file
        with open(file_name, 'r') as f:
            # Read the file line by line
            openai.organization = f.readline().strip()
            openai.api_key = f.readline().strip()

        models = openai.Model.list()

        # Use a model to generate text
        model_engine = "text-davinci-003"

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
    elif event == 'Clear Output':
        # Clear the output
        clear_output()

