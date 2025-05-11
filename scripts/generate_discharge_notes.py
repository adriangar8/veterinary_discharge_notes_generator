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
    
    if not os.path.exists(file_path): # check if file exists
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
    
    if not file_path.lower().endswith('.json'): # check if file is a .json file
        raise ValueError("Error: Input file must be a .json file.")
    
    try:
        with open(file_path, 'r') as f:
            json.load(f) # check if file contains valid JSON
            
    except json.JSONDecodeError: # JSON decode error
        raise ValueError(f"Error: The file '{file_path}' contains invalid JSON.")
    
# -- api key validation function --
def validate_api_key(key: str) -> bool:
    return key.startswith('di-')  # DeepInfra API keys typically start with 'di-'

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

#### FUNCTIONS ####

# -- discharge notes generation function --
def generate_discharge_note(consultation_data):
    
    """Generates a discharge note using Llama 3 via DeepInfra."""
    
    load_dotenv()
    api_key = os.getenv("DEEPINFRA_API_KEY")
    
    if not api_key: # check if API key is set
        raise ValueError("API key not found. Please set DEEPINFRA_API_KEY in .env file")
    
    if not validate_api_key(api_key): # validate API key format
        raise ValueError("Invalid DeepInfra API key format")
    
    client = OpenAI(
        base_url="https://api.deepinfra.com/v1/openai",
        api_key=api_key
    )
    
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
    """
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful veterinary assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500  # Llama 3 can handle longer outputs
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise ValueError(f"API request failed: {str(e)}")

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

#### MAIN ####

# -- main function to handle command line arguments and generate discharge notes --
def main():
    
    if len(sys.argv) != 2: # check if correct number of arguments is provided
        
        print("Usage: python generate_discharge_notes.py <path_to_json_file>")
        sys.exit(1)
    
    input_file = sys.argv[1] # get the input file path
    
    try:
        
        validate_input_file(input_file) # validate input file before processing
        
        with open(input_file, 'r') as f: # load and process the consultation data
            
            consultation_data = json.load(f)
        
        discharge_note = generate_discharge_note(consultation_data)
        
        output = {
            "discharge_note": discharge_note
        }
        
        print(json.dumps(output, indent=4))
        
    except FileNotFoundError as e:
        
        print(str(e))
        sys.exit(1)
        
    except ValueError as e:
        
        print(str(e))
        sys.exit(1)
        
    except Exception as e:
        
        print(f"Error: {str(e)}")
        sys.exit(1)

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()