def generate_response(intent, intents):
    # Debugging: Check if intent is a string
    print(f"Intent: {intent}")
    print(f"Intents structure: {intents}")

    # Check if 'intents' is a dictionary and has the 'intents' key
    if not isinstance(intents, dict) or 'intents' not in intents:
        return "Sorry, I don't understand that."

    # Debugging: Print all available intents
    for i in intents['intents']:
        print(f"Available intent tag: {i.get('tag')}")
        if i.get('tag') == intent:
            # Debugging: Check if responses exist
            print(f"Found matching intent: {intent}, responses: {i.get('responses')}")
            if isinstance(i.get('responses'), list) and len(i['responses']) > 0:
                return i['responses'][0]  # Return the first response (you can randomize it if needed)
            else:
                return "Sorry, I don't have a response for that."

    return "Sorry, I don't understand that."
