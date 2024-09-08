import json
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class DataPreprocessing:
    def __init__(self):
        self.tokenizer = Tokenizer()

    def load_data(self, file_path):
        """Loads data from a JSON file."""
        with open(file_path) as file:
            data = json.load(file)
        return data

    def preprocess_data(self, data, return_raw_text=False):
        """Preprocesses the data and returns padded sequences and labels.

        Args:
            data (dict): The data loaded from the JSON file.
            return_raw_text (bool): If True, returns the raw text patterns instead of tokenized sequences.

        Returns:
            If return_raw_text is False:
                padded_sequences (np.ndarray): Padded tokenized sequences.
                labels (list): Corresponding labels for each pattern.
            If return_raw_text is True:
                patterns (list): Raw text patterns.
                labels (list): Corresponding labels for each pattern.
        """
        patterns = []
        labels = []
        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                patterns.append(pattern)
                labels.append(intent["tag"])

        if return_raw_text:
            return patterns, labels  # Return raw text patterns for tokenization

        # Tokenize the patterns
        self.tokenizer.fit_on_texts(patterns)
        sequences = self.tokenizer.texts_to_sequences(patterns)
        padded_sequences = pad_sequences(sequences, padding='post', maxlen=20)
        
        return padded_sequences, labels

    def save_tokenizer(self, file_path):
        """Saves the tokenizer to a JSON file."""
        tokenizer_json = self.tokenizer.to_json()
        with open(file_path, "w") as file:
            file.write(tokenizer_json)

    def load_tokenizer(self, file_path):
        """Loads the tokenizer from a JSON file."""
        from tensorflow.keras.preprocessing.text import tokenizer_from_json
        with open(file_path) as file:
            tokenizer_json = file.read()
            self.tokenizer = tokenizer_from_json(tokenizer_json)
