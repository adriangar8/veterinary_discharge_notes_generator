
# -- import necessary libraries --
import os
import json
import sys
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

#### UTILS ####

# -- utility function to validate input file --
def validate_input_file(file_path):
    
    """Validate the input file exists and is a .json file."""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
    
    if not file_path.lower().endswith('.json'):
        raise ValueError("Error: Input file must be a .json file.")
    
    try:
        with open(file_path, 'r') as f:
            json.load(f)
            
    except json.JSONDecodeError:
        raise ValueError(f"Error: The file '{file_path}' contains invalid JSON.")

# -- utility function to save discharge note to solution directory --
def save_discharge_note(input_path: str, output: Dict[str, Any]):
    
    """Save discharge note to solution directory with proper naming convention"""
    
    solution_dir = Path(input_path).parent.parent / "solution"
    solution_dir.mkdir(exist_ok=True)
    
    input_name = Path(input_path).stem
    output_file = solution_dir / f"{input_name}_discharge_note.json"
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)
        
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

#### FUNCTIONS ####

# -- discharge notes generation function --
def generate_discharge_note(consultation_data):
    
    """Generates a discharge note using Llama 3 via Together.ai"""
    
    load_dotenv() # load environment variables from .env file
    api_key = os.getenv("TOGETHER_API_KEY") # get API key from environment variable
    
    if not api_key: # check if API key is set
        raise ValueError("API key not found. Please set TOGETHER_API_KEY in .env file")
    
    client = OpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=api_key
    ) # initialize the API client
    
    prompt = f"""
    You are a veterinary assistant tasked with writing clear, compassionate discharge notes for pet owners.
    Based on the following consultation data, write a concise discharge note that summarizes:
    - The patient's condition
    - Any treatments or procedures performed
    - Important observations
    - Follow-up instructions
    
    Write in a professional yet friendly tone, addressing the pet owner directly.
    
    Consultation Data:
    {json.dumps(consultation_data, indent=2)}
    """ # format of the prompt with consultation data
    
    try:
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf", # model used for generating text
            messages=[
                {"role": "system", "content": "You are a helpful veterinary assistant."},
                {"role": "user", "content": prompt}
            ], # user message
            temperature=0.7, # allow some creativity
            max_tokens=500 # limit the response length
        )
        
        return response.choices[0].message.content.strip() # extract the generated text from the response and return it
    
    except Exception as e:
        raise ValueError(f"API request failed: {str(e)}")

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

#### MAIN ####

# -- main function to handle command line arguments and generate discharge notes --
def main():
    
    if len(sys.argv) != 2: # script should only accept one argument
        print("Usage: python generate_discharge_notes.py <path_to_json_file>")
        sys.exit(1)
    
    input_file = sys.argv[1] # path to the input JSON file
    
    try:
        
        validate_input_file(input_file) # validate the input file
        
        with open(input_file, 'r') as f:
            consultation_data = json.load(f) # load the consultation data
        
        discharge_note = generate_discharge_note(consultation_data) # generate the discharge note
        output = {"discharge_note": discharge_note}
        
        save_discharge_note(input_file, output) # 
        
    except Exception as e:
        
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()