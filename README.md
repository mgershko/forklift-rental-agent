# Forklift Rental Inquiry Agent

A Python-based web application that processes natural language forklift rental requests, asks qualifying questions, matches requirements to suitable forklift models, and generates detailed quotes.

## Features

- **Natural Language Processing**: Understand and process rental requests in natural language
- **Conversational Interface**: Ask relevant qualifying questions to gather necessary information
- **Smart Matching**: Match customer requirements to the appropriate forklift model
- **Quote Generation**: Create detailed quotes with specifications, rates, and availability
- **Brochure Integration**: Provide detailed information from forklift brochures
- **User-Friendly Web Interface**: Built with Streamlit for an intuitive user experience
- **No External API Keys Required**: Fully self-contained application

## Project Structure

```
forklift_rental_agent/
├── app.py                 # Main Streamlit application
├── run_tests.py           # Test runner script
├── requirements.txt       # Project dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── run_app.sh             # Shell script to run app in venv (Unix)
├── run_app.bat            # Batch script to run app in venv (Windows)
├── .gitignore             # Git ignore file
├── data/                  # Data files
│   ├── Schedule of Rates Example - Sheet1.csv
│   ├── Bobcat D35-40-45-50-55-S+SC-5.pdf
│   └── Bobcat D60-70-80-90S-5 Brochure.pdf
├── src/                   # Source code
│   ├── __init__.py        # Package marker
│   ├── data_loader.py     # Functions to load and process data
│   ├── matcher.py         # Logic to match requirements to forklifts
│   ├── conversation.py    # Conversation flow and qualifying questions
│   ├── quote.py           # Quote generation logic
│   └── ui_components.py   # Reusable UI components
└── tests/                 # Unit tests
    ├── __init__.py        # Package marker 
    ├── test_data_loader.py
    ├── test_matcher.py
    ├── test_conversation.py
    └── test_quote.py
```

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
docker-compose up
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

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Future Enhancements

- Integration with inventory management systems
- Email functionality to send quotes to customers
- Calendar integration for scheduling rentals
- PDF generation for quotes
- More advanced natural language processing
- Integration with payment gateways

## License

This project is licensed under the MIT License - see the LICENSE file for details.
