# finvestAI
AI based Trading Algorithmic platform.

## Project Overview
This AI platform leverages the power of finBERT, a BERT-based Natural Language Processing (NLP) model pre-trained for financial sentiment analysis, to make trading decisions based on the sentiment derived from financial news articles. The AI strategy is designed to analyze the sentiment of recent news articles related to a particular stock or financial asset and make buy or sell decisions based on the aggregated sentiment.

## Technologies and Libraries Used
- Python 3
- [PyTorch](https://pytorch.org/): An open-source machine learning library.
- [Transformers](https://huggingface.co/transformers/): A library by Hugging Face offering pre-trained NLP models.
- [Alpaca Trade API](https://alpaca.markets/): A commission-free trading platform that offers an API for algorithmic trading.
- [lumibot](https://lumibot.lumiwealth.com/): A framework for creating trading bots with Python.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.6 or later.
- You have an Alpaca account and have obtained your API key and secret. Sign up [here](https://app.alpaca.markets/signup) if you haven't already.

## Setup and Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```
2. **Create and Activate a Virtual Environment (optional but recommended)**:
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS and Linux
    source venv/bin/activate
    ````
3. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Running the Trading Platoform**:
    ```bash
    python TradingAlgo.py
    ````
**!** Make sure to update the `API_KEY`, `API_SECRET`, and `API_ENDPOINT` in `TradingAlgo.py` with your actual Alpaca credentials.

## Project Structure
- `utils/finbert_NLP.py`: Contains the NLP model and sentiment analysis function.
- `TradingAlgo.py`: Main script that integrates sentiment analysis into trading logic with the Alpaca API and lumibot strategy.

## Contact
If you have any questions or feedback, please contact me at moiezhsyed@gmail.com.


