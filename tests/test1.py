from eew_client import EEWClient

client = EEWClient(client_type="axis", debug=True)


@client.on_message
def handle_message(message):
    print(f"Received message: {message}")


client.trigger_message("This is a test message.")
