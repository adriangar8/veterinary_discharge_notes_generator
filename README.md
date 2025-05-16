# Veterinary Discharge Notes Generator

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Conda](https://img.shields.io/badge/conda-supported-brightgreen)

An AI-powered tool for generating veterinary discharge notes from consultation data.

## Project Structure

veterinary-notes-generator/
├── data/ # Sample consultation JSON files
├── solution/ # Generated discharge notes
├── scripts/
│ ├── generate_discharge_notes.py # Main script
│ └── .env # API keys (gitignored)
├── requirements.txt # Python dependencies
└── environment.yml # Conda environment spec

## Installation (Conda)

```bash
# Clone repository
git clone https://github.com/yourusername/veterinary-notes-generator.git
cd veterinary-notes-generator

# Create conda environment
conda create -n vetnotes python=3.9 -y

# Activate environment
conda activate vetnotes

# Install dependencies
conda install --file requirements.txt -c conda-forge
```

## Configuration

1. Get API key from Together.ai
2. Create .env file on scripts directory (.../veterinary_discharge_notes/scripts/):

```bash
echo "TOGETHER_API_KEY=your_api_key_here" > .env
```

## Usage 

```bash
conda activate vetnotes
python scripts/generate_discharge_notes.py data/consultation_sample.json
```

## License

MIT License
