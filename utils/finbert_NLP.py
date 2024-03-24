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
    If 'news' is populated, this function returns the highest probability and it's associated sentiment.
    If not, this function returns 0 and 'neutral' as default values.

    Args:
        news (list): Most recent financial news related to a particular asset

    Returns:
        probability (float): Highest probability for the sentiments (classes) for the input texts
        sentiment (string): The label associated with the probability
    """
    # check if news populated
    if news:
        # tokenization
        tokens = tokenizer(news, return_tensors='pt', padding=True).to(device)
        # model prediction; returns raw, unnormalized scores for each class (logits)
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
        # apply softmax and summation
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        # get the probability (highest probability)
        probability = result[torch.argmax(result)]
        # get the correspodning sentiment (highest sentiment)
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]

if __name__ == "__main__":
    tensor, sentiment = sentiment_estimate(['markets responded negatively to the news!','traders were displeased!'])
    print(tensor, sentiment)
    print(torch.cuda.is_available())