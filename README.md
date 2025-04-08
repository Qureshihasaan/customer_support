# Customer Support Chatbot

A sophisticated customer support chatbot system built with Chainlit and OpenAI Agent SDK, designed to handle various types of customer inquiries for an internet service provider.

## Features

- **Multi-Agent System**: Intelligent routing of customer queries to specialized agents
- **Specialized Support Areas**:
  - Billing Support
  - Complaint Handling
  - Plan/Package Information
  - Connection Troubleshooting
  - General Queries
- **Natural Language Processing**: Powered by Gemini AI for intelligent responses
- **Interactive Chat Interface**: User-friendly web interface built with Chainlit

## Prerequisites

- Python 3.12 or higher
- Gemini API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Qureshihasaan/customer_support_agent
cd customer-support
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv add openai-agents python-dotenv chainlit
```

4. Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
uv run chainlit run main.py -w
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8000)

3. Start chatting with the customer support bot!

## Project Structure

```
customer-support/
├── src/
│   └── customer_support/
│       ├── main.py           # Main application logic
│       ├── chainlit.md       # Chainlit configuration
│       └── .chainlit/        # Chainlit assets
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Available Agents

- **Triage Agent**: Routes queries to appropriate specialized agents
- **Billing Agent**: Handles payment, charges, and billing inquiries
- **Complaint Agent**: Manages customer complaints and grievances
- **Plan Agent**: Provides information about internet plans and packages
- **Connection Agent**: Assists with technical support and connection issues
- **General Query Agent**: Handles miscellaneous questions and account information

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Qureshihasaan (hasaanqureshi150@gmail.com)
