# Veterinary Discharge Note Generator

This script generates discharge notes for pet owners based on consultation data provided in JSON format using the Llama 3 model via the Together.ai API.

## Overview

The `generate_discharge_notes.py` script takes a JSON file containing veterinary consultation information as input. It then uses a structured prompt with the Llama 3 model to generate a compassionate and professional discharge note. The generated note is saved as a JSON file in the `solution` directory.

## Prerequisites

Before running the script, ensure you have the following:

* **Python 3.6 or higher**
* **Conda** (if you intend to use the provided `environment.yml`)
* **Together.ai API Key:** You will need an API key from Together.ai to interact with their models. Set this key as an environment variable named `TOGETHER_API_KEY` in a `.env` file in the `scripts` directory (see "Setup" below).

## Setup

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone <repository_url>
    cd veterinary_discharge_notes_generator
    ```

2.  **Create and activate the Conda environment (recommended):**

    ```bash
    conda env create -f environment.yml
    conda activate vet_notes
    ```

    Alternatively, you can install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file in the `scripts` directory:**

    ```bash
    cd scripts
    touch .env
    ```

4.  **Add your Together.ai API key to the `.env` file:**

    Open the `.env` file and add your API key:

    ```
    TOGETHER_API_KEY=YOUR_API_KEY_HERE
    ```

    Replace `YOUR_API_KEY_HERE` with your actual Together.ai API key.

## Usage

1.  **Place your consultation data JSON files in the `data` directory.** The script expects JSON files with at least the keys `"patient"` and `"consultation"`.

2.  **Run the `generate_discharge_notes.py` script, providing the path to your consultation JSON file as a command-line argument:**

    ```bash
    python scripts/generate_discharge_notes.py data/consultation1.json
    ```

    Replace `data/consultation1.json` with the actual path to your input file.

3.  **The generated discharge note will be saved as a JSON file in the `solution` directory.** The filename will follow the convention `<input_filename>_discharge_note.json`. For example, if the input file is `consultation1.json`, the output file will be `solution/consultation1_discharge_note.json`.

## Directory Structure

veterinary_discharge_notes_generator/
├── data/
│   ├── consultation1.json
│   └── consultation2.json
├── scripts/
│   ├── .env
│   └── generate_discharge_notes.py
├── solution/
│   ├── consultation1_discharge_note.json
│   └── consultation2_discharge_note.json
├── .gitignore
├── environment.yml
└── README.md

## Dependencies

The script relies on the following Python libraries:

* `openai`: For interacting with the Together.ai API.
* `python-dotenv`: For loading environment variables from a `.env` file.
* `pathlib`: For working with file paths in an object-oriented way.
* `typing`: For type hinting.

These dependencies are listed in the `requirements.txt` file and are managed by the `environment.yml` for Conda environments.

## Error Handling

The script includes basic error handling for:

* Invalid number of command-line arguments.
* Non-existent input files.
* Input files that are not valid JSON.
* Missing or invalid JSON structure within the input file.
* Missing `TOGETHER_API_KEY` in the `.env` file.
* Errors during the API request to Together.ai.

## Contributing

Contributions to this project are welcome. Please feel free to submit pull requests or open issues for any bugs or enhancements.

## License

[Specify your license here, e.g., MIT License]