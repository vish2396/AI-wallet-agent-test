from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import json

class NLPModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.intents_list = [
            "greeting", "goodbye", "connect_wallet", "check_balance", "predict_transactions",
            "show_transactions", "show_spending", "show_income", "show_savings", 
            "show_investments", "show_debts", "show_net_worth", "show_budget", 
            "show_trends", "show_forecast", "show_summary", "show_all"
        ]


    def load_model(self, model_path, tokenizer_path):
        self.model = load_model(model_path)
        
        # Load the tokenizer configuration
        with open(tokenizer_path, 'r') as file:
            tokenizer_data = json.load(file)

        # Recreate the tokenizer
        self.tokenizer = Tokenizer()
        self.tokenizer.word_index = tokenizer_data.get('word_index', {})

    def predict_intent(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        padded_sequence = pad_sequences(sequence, padding='post', maxlen=20)
        predictions = self.model.predict(padded_sequence)

        # Print predictions shape for debugging
        print("Predictions shape:", predictions.shape)
    
        # Get the index of the highest probability intent
        intent_index = predictions.argmax()
        probability = predictions[0][intent_index]

        # Make sure intent_index is within range of self.intents_list
        if intent_index >= len(self.intents_list):
            raise IndexError(f"Predicted intent index {intent_index} is out of range.")
    
        intent = self.intents_list[intent_index]
        return intent, probability

