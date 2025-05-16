
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

# -- utility function to validate consultation data --
def validate_consultation_data(data: dict):
    
    """Ensure the generated note only includes facts from the consultation data"""
    
    required_sections = ['patient', 'consultation']
    
    for section in required_sections:
        
        if section not in data:
            raise ValueError(f"Missing required section: {section}")
        
# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

#### FUNCTIONS ####

# -- discharge notes generation function --
def generate_discharge_note(consultation_data):
    
    """Generates a discharge note using Llama 3 via Together.ai"""
    
    validate_consultation_data(consultation_data) # validate the input data
    
    load_dotenv() # load environment variables from .env file
    api_key = os.getenv("TOGETHER_API_KEY") # get API key from environment variable
    
    if not api_key: # check if API key is set
        raise ValueError("API key not found. Please set TOGETHER_API_KEY in .env file")
    
    client = OpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=api_key
    ) # initialize the API client
    
    # -- Structured prompt for generating the discharge note --
    prompt = f"""
    You are a compassionate and professional veterinary assistant tasked with understanding and writing a discharge note for a pet owner. The note should be based entirely on the consultation data provided below.

    Please follow these guidelines:
    1. Begin with a warm greeting, and end with a thoughtful closing, signed as "The Veterinary Team".
    2. Include **all relevant information** from the consultation data to keep the owner fully informed.
    3. Use a **friendly, clear, and professional tone** throughout the message.
    4. If some information is missing from the data, simply omit it—do not guess or invent.
    5. **Do not** use any placeholders like [text] or [xx].
    6. Output **only** the discharge note—**do not add explanations or extra comments.**

    Consultation Data:
    {json.dumps(consultation_data, indent=2)}

    Generate only the final discharge note.
    """

    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", # model suitable for structured data extraction tasks
            messages=[
                {"role": "system", "content": "You are a compassionate and professional veterinary assistant tasked with understanding and writing a discharge note for a pet owner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, # lower temperature for more deterministic output, reducing hallucinations
            max_tokens=1000 # limit the response length to avoid excessive output
        )
        
        note = response.choices[0].message.content.strip()
        
        # -- Post-processing the generated note --
        if "[" in note or "]" in note: # check for placeholders
            
            note = note.replace("[", "").replace("]", "") # remove placeholders
            
            if "in  to" in note: # fix broken time frames
                note = note.replace("in  to", "as needed")
        
        return note
    
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
        
        save_discharge_note(input_file, output) # save the discharge note
        
    except Exception as e:
        
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

# -------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()