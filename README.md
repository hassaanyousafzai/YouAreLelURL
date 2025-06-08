# YouAreLeL (URL) Reader

A powerful chatbot that reads and analyzes content from multiple URLs, allowing you to have interactive conversations about the information contained within them. Perfect for research and content analysis.

## Features

- Process multiple URLs simultaneously
- Interactive chat interface
- Export chat history
- Clear chat functionality
- Real-time URL content analysis
- AI-powered question answering

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd URL_Read_Chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your-api-key-here
```

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Enter up to 3 URLs in the sidebar
3. Click "Process URLs" to analyze the content
4. Start chatting and asking questions about the URLs' content

## Note

First-time processing may take a few moments as the AI components are being set up.

## Requirements

See `requirements.txt` for a full list of dependencies. 