import asyncio
import os
import sys
from datetime import datetime
from exo.api.cheshire_terminal import get_terminal

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡖⠁⠀⠀⠀⠀⠀⠀⠈⢲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣸⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣇⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⢀⣀⣤⣤⣤⣤⣀⡀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣔⢿⡿⠟⠛⠛⠻⢿⡿⣢⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣷⣤⣀⡀⢀⣀⣤⣾⣿⣿⣿⣷⣶⣤⡀⠀⠀⠀⠀
    ⠀⠀⢠⣾⣿⡿⠿⠿⠿⣿⣿⣿⣿⡿⠏⠻⢿⣿⣿⣿⣿⠿⠿⠿⢿⣿⣷⡀⠀⠀
    ⠀⢠⡿⠋⠁⠀⠀⢸⣿⡇⠉⠻⣿⠇⠀⠀⠸⣿⡿⠋⢰⣿⡇⠀⠀⠈⠙⢿⡄⠀
    ⠀⡿⠁⠀⠀⠀⠀⠘⣿⣷⡀⠀⠰⣿⣶⣶⣿⡎⠀⢀⣾⣿⠇⠀⠀⠀⠀⠈⢿⠀
    ⠀⡇⠀⠀⠀⠀⠀⠀⠹⣿⣷⣄⠀⣿⣿⣿⣿⠀⣠⣾⣿⠏⠀⠀⠀⠀⠀⠀⢸⠀
    ⠀⠁⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⢇⣿⣿⣿⣿⡸⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠈⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠐⢤⣀⣀⢀⣀⣠⣴⣿⣿⠿⠋⠙⠿⣿⣿⣦⣄⣀⠀⠀⣀⡠⠂⠀⠀⠀
    ⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀
    
    🎭 C H E S H I R E  T E R M I N A L 🎭
    Your mystical gateway to $GRIN trading insights ✨
    Now with real-time Solana blockchain vision! 🔮
    """
    print(banner)

def print_help():
    help_text = """
    🌟 Mystical Commands 🌟
    
    • analyze wallet <address> - Peer into any Solana wallet's secrets
    • market - Get real-time market insights and trends
    • help - Show this magical guide
    • clear - Clear the mist from your screen
    • exit - Fade away into the blockchain mist
    
    Ask me anything about $GRIN, Solana, or the market! ✨
    """
    print(help_text)

def print_timestamp():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now}] Market time... 🕰️\n")

async def main():
    terminal = get_terminal()
    
    clear_screen()
    print_banner()
    print_timestamp()
    print_help()
    
    while True:
        try:
            # Get trader's inquiry
            user_input = input("\nTrader: ").strip()
            
            # Handle special commands
            if user_input.lower() == 'exit':
                print("\nCheshire: The market never sleeps, but I must fade away... Until next time! ✨")
                break
            elif user_input.lower() == 'clear':
                clear_screen()
                print_banner()
                print_timestamp()
                continue
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif not user_input:
                continue
                
            # Get mystical market insights with blockchain data
            response = await terminal.chat(user_input)
            print(f"\nCheshire: {response.get('response', 'The market mist clouds my vision... 🎭')}\n")
            
        except KeyboardInterrupt:
            print("\nCheshire: Caught by surprise! Fading into the mist... ✨")
            break
        except Exception as e:
            print(f"\nOh my... A glitch in the market matrix! 🎭 ({str(e)})")
            continue

if __name__ == "__main__":
    try:
        # Kill any existing instances
        os.system('pkill -f "python3 examples/astra/cheshire_terminal.py"')
        # Start new instance
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error in the trading wonderland: {e}")
        sys.exit(1)
