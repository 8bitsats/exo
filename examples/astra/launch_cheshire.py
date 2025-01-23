import asyncio
import sys
import os
import ssl
import certifi
from exo.api.web_server import CheshireWebServer
from exo.api.cheshire_terminal import CheshireTerminal
import webbrowser

async def run_terminal():
    """Run the terminal interface."""
    terminal = CheshireTerminal()
    
    try:
        while True:
            user_input = input("\nTrader: ").strip()
            
            if user_input.lower() == 'exit':
                print("\nCheshire: The market never sleeps, but I must fade away... Until next time! ✨")
                break
                
            response = await terminal.chat(user_input)
            print(f"\nCheshire: {response.get('response', 'The market mist clouds my vision... 🎭')}\n")
            
    except KeyboardInterrupt:
        print("\nCheshire: Caught by surprise! Fading into the mist... ✨")
    finally:
        await terminal.close()

async def main():
    """Launch both the terminal and web dashboard."""
    print("🎭 Launching Cheshire Terminal & Dashboard... ✨")
    
    # Disable SSL verification warnings for development
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Start the web server with SSL verification disabled for development
    server = CheshireWebServer(verify_ssl=False)
    runner, site = await server.start()
    
    # Open the dashboard in the default browser
    print("Opening dashboard in your browser...")
    webbrowser.open('http://localhost:8080')
    
    print("\n🌟 Available Commands:")
    print("• 'token <address>' - Get detailed token information")
    print("• 'market' - View trending tokens and volume leaders")
    print("• 'analyze wallet <address>' - Examine Solana wallets")
    print("• 'help' - Show all available commands")
    print("• 'exit' - Close both terminal and dashboard")
    print("\nThe dashboard provides additional features for:")
    print("• Token Analysis & Charts")
    print("• NFT Management")
    print("• Solana Code Analysis")
    print("• Contract Generation")
    
    try:
        # Run the terminal interface
        await run_terminal()
    finally:
        # Cleanup
        print("\nClosing dashboard...")
        await runner.cleanup()

def setup_ssl_context():
    """Setup SSL context for the application."""
    try:
        # Create SSL context with system certificates
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        return ssl_context
    except Exception as e:
        print(f"Warning: Could not setup SSL context: {e}")
        # Fallback to unverified context for development
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

if __name__ == "__main__":
    try:
        # Kill any existing instances
        os.system('pkill -f "python3 examples/astra/cheshire_terminal.py"')
        os.system('pkill -f "python3 examples/astra/launch_cheshire.py"')
        
        # Setup SSL context
        ssl_context = setup_ssl_context()
        
        # Start new instance
        asyncio.run(main())
    except Exception as e:
        print(f"Fatal error in the trading wonderland: {e}")
        sys.exit(1)
