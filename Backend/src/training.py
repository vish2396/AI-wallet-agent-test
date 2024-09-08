from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences  # Add this import
from src.data_preprocessing import DataPreprocessing
import numpy as np

def create_model(vocab_size, input_length, num_classes):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=64, input_length=input_length))
    model.add(LSTM(64))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model():
    preprocessing = DataPreprocessing()
    data = preprocessing.load_data("data/\\intents.json")
    X_raw, y = preprocessing.preprocess_data(data, return_raw_text=True)

    # Tokenize the raw text
    preprocessing.tokenizer.fit_on_texts(X_raw)
    X = preprocessing.tokenizer.texts_to_sequences(X_raw)
    X = pad_sequences(X, padding='post', maxlen=20)  # This line should now work

    # Convert labels to categorical (one-hot encoding)
    unique_labels = list(set(y))
    y = np.array([unique_labels.index(label) for label in y])
    y = to_categorical(y, num_classes=len(unique_labels))

    vocab_size = X.max() + 1
    input_length = X.shape[1]

    model = create_model(vocab_size=vocab_size, input_length=input_length, num_classes=len(unique_labels))
    model.fit(X, y, epochs=10, batch_size=8)

    model.save("models/chatbot_model.keras")
    preprocessing.save_tokenizer("models/tokenizer.json")

if __name__ == "__main__":
    train_model()
