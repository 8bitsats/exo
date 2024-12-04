from exo.api.astra_chat_client import get_chat_client

def main():
    # Get the Cheshire-styled chat client
    client = get_chat_client()
    
    print("🐱 Cheshire Chat Interface 🌟")
    print("Type 'exit' to end the conversation\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit command
            if user_input.lower() == 'exit':
                print("\nCheshire: Fading away into the blockchain mist... Until we meet again! ✨")
                break
                
            # Get response from Astra
            response = client.chat(user_input)
            print(f"\nCheshire: {response.get('response', 'Hmm... *mysterious silence*')}\n")
            
        except Exception as e:
            print(f"\nOh my... A glitch in the matrix! 🎭 ({str(e)})")
            continue

if __name__ == "__main__":
    main()
