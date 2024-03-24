from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load the pre-trained model and Tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

# Sentiment Anaysis
def sentiment_estimate(news):
    """Performs sentiment analysis on financial news, based on pre-trained NLP model 'finBERT'.

    Args:
        news (list): Most recent financial news related to a particular asset
    """
    # check if news populated
    if news:
        # tokenization
        tokens = tokenizer(news, return_tensors='pt', padding=True).to(device)
        # model prediction; returns raw, unnormalized scores for each class (logits)
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]