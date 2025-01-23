from exo.api.astra_api import AstraLangflowClient

def main():
    # Initialize the client with your API token
    client = AstraLangflowClient(
        "AstraCS:hJxvZgaWKsMfuxsvDlWcLyCD:7e1a25f2abc17024141bc1cc95af5c221a68cd95f2e51a0c69369ff44d6cf4b9"
    )
    
    # Define the default tweaks
    tweaks = {
        "Agent-YDVUV": {},
        "ChatInput-KIX8A": {},
        "ChatOutput-uB3vz": {},
        "URL-qeVXs": {},
        "CalculatorTool-mw90V": {}
    }
    
    # Example messages to test
    messages = [
        "What's 2 + 2?",
        "Tell me about the weather",
        "What's the capital of France?"
    ]
    
    # Run each message through the flow
    for message in messages:
        print(f"\nSending message: {message}")
        try:
            result = client.run_flow(
                flow_id="9412ef3b-4d94-4559-b761-0afcf10040b4",
                message=message,
                tweaks=tweaks
            )
            print("Response:", result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
