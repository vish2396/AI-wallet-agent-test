from src.config import Config
from src.coinbase_client import CoinbaseClient  # Assuming you have this class to interact with Coinbase API
from src.nlp_model import NLPModel
from src.responses import generate_response
import json

def main():
    # Load intents once when the server starts
    def load_intents():
        with open(Config.INTENTS_FILE) as file:
            return json.load(file)

    # Load intents and model once at the start
    intents = load_intents()
    model = NLPModel()
    model.load_model("models/chatbot_model.keras", "models/tokenizer.json")  # Load Keras model and tokenizer
    coinbase_client = CoinbaseClient()  # Create an instance to interact with Coinbase API

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting chat...")
            break

        # Predict the user's intent
        intent, probability = model.predict_intent(user_input)

        # Handle different intents based on user input
        if intent == 'connect_wallet':
            response = "Connecting to your wallet..."
            # Implement wallet connection logic here (e.g., coinbase_client.connect_wallet())
        elif intent == 'check_balance':
            balance = coinbase_client.get_account_balance()  # Fetch balance from Coinbase API
            response = f"Your balance is {balance} BTC."
        elif intent == 'predict_transactions':
            response = "Predicting your transactions..."
            # Implement transaction prediction logic here
        else:
            # If it's a generic intent, generate response from the intents JSON
            response = generate_response(intent, intents)

        # Output the bot's response
        print(f"Bot: {response}")

if __name__ == '__main__':
    main()
