from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load the pre-trained model and Tokenizer
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
