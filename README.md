# Forklift Rental Inquiry Agent

A Python-based web application that processes natural language forklift rental requests, asks qualifying questions, matches requirements to suitable forklift models, and generates detailed quotes.


## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Other dependencies listed in `requirements.txt`

## Setup and Installation

### Option 1: Using Virtual Environment

#### For Unix/Linux/macOS:

```bash
# Clone the repository
git clone https://github.com/yourusername/forklift-rental-agent.git
cd forklift-rental-agent

# Run the setup script
chmod +x run_app.sh
./run_app.sh
```

#### For Windows:

```cmd
# Clone the repository
git clone https://github.com/yourusername/forklift-rental-agent.git
cd forklift-rental-agent

# Run the setup script
run_app.bat
```

### Option 2: Manual Setup with Virtual Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/forklift-rental-agent.git
cd forklift-rental-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Option 3: Using Docker

```bash
# Clone the repository
git clone https://github.com/yourusername/forklift-rental-agent.git
cd forklift-rental-agent

# Build and run with Docker Compose
docker-compose up --build
```

The application will be available at http://localhost:8501

## Running Tests

```bash
# With activated virtual environment
python run_tests.py

# OR run individual test files
python -m unittest tests/test_data_loader.py
python -m unittest tests/test_matcher.py
python -m unittest tests/test_conversation.py
python -m unittest tests/test_quote.py
```

## Workflow

1. The user enters a natural language request for a forklift rental
2. The system asks a series of qualifying questions to gather necessary information:
   - Weight of the heaviest load
   - Rental period
   - Indoor/outdoor usage
   - Maximum lifting height
   - Special requirements
3. The system matches the requirements to an appropriate forklift model
4. A detailed quote is generated with specifications, pricing, and availability
5. The user can save/print the quote or start a new inquiry

## Deployment

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Deploy the application with app.py as the entry point

### Hugging Face Spaces Deployment

1. Create a new Space on Hugging Face
2. Choose Streamlit as the SDK
3. Upload your code to the Space's repository
4. Configure the Space to use app.py as the entry point

### Custom Server Deployment

For deploying on your own server:

```bash
# Clone the repository
git clone https://github.com/yourusername/forklift-rental-agent.git
cd forklift-rental-agent

# Using Docker
docker-compose up -d
```
