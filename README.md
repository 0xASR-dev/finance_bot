# Holdings & Trades Analysis Chatbot

This project implements an AI-powered financial analyst chatbot that answers questions based on holdings and trades data from CSV files. It offers both a command-line interface and a modern web-based UI.

## Features

- **Data Analysis**: detailed analysis of holdings and trades from `holdings.csv` and `trades.csv`.
- **Natural Language Queries**: Ask questions in plain English (e.g., "Total number of holdings", "Which funds performed better?", "YTD P&L for Ytum").
- **Dual Interface**:
  - **CLI Chatbot**: Simple terminal-based interaction.
  - **Web Chatbot**: Modern, responsive web UI with suggestion chips and typing indicators.
- **Performance Metrics**: Calculates P&L (YTD, MTD, QTD), market values, and identifies top performing funds.
- **Fallback Handling**: Gracefully handles unknown queries without ensuring accuracy by not hallucinating external data.

## Project Structure

- `chatbot.py`: Core logic and CLI implementation.
- `web_chatbot.py`: Flask-based web application with modern UI.
- `holdings.csv`: Source data for portfolio holdings.
- `trades.csv`: Source data for trade execution.

## Setup & Usage

### Prerequisites
- Python 3.8+
- `pandas`
- `flask`

### Installation

1. Clone the repository (or download the files).
2. Install dependencies:
   ```bash
   pip install pandas flask
   ```

### Running the Chatbot

**Option 1: Web Interface (Recommended)**
1. Run the web app:
   ```bash
   python web_chatbot.py
   ```
2. Open your browser and navigate to `http://localhost:5000`.

**Option 2: Command Line Interface**
1. Run the CLI script:
   ```bash
   python chatbot.py
   ```

## Example Questions

- **Holdings**: "Total number of holdings for Garfield", "How many holdings are there?"
- **Trades**: "Total number of trades for HoldCo 1", "Trade types summary"
- **Performance**: "Which funds performed better?", "Best performing funds", "YTD P&L for Ytum"
- **Market Value**: "Market value for Garfield", "Total market value"
- **General**: "List all funds", "What are the custodians?"

## Notes
- The chatbot strictly uses local CSV data and does not fetch information from the internet.
- Ensure `holdings.csv` and `trades.csv` are in the same directory as the scripts.
