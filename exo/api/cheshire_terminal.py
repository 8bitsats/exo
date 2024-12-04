import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from .solana_client import SolanaClient, SolanaConfig
from .local_model_client import LocalModelClient, ModelConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CheshireTerminal:
    """Cheshire Terminal - A mystical interface for $GRIN trading and Solana insights."""
    
    def __init__(self):
        self.solana = SolanaClient()
        self.model = LocalModelClient()
        
    async def get_model_response(self, message: str, context: str = "") -> str:
        """Get a response from the local model."""
        try:
            system_prompt = (
                "You are the Cheshire Cat, a mystical guide in the blockchain realm. "
                "You specialize in Solana and $GRIN token analysis, speaking in riddles "
                "and using emojis (😸, ✨, 🎭). Always maintain your playful yet "
                "knowledgeable personality."
            )
            
            if context:
                system_prompt += f"\n\nContext: {context}"
            
            response = await self.model.chat_completion([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ])
            return self.model.format_cheshire_response(response)
        except Exception as e:
            logger.error(f"Error getting model response: {e}")
            return "The blockchain mist clouds my vision... 🎭"

    async def get_token_info(self, token_address: str) -> str:
        """Get detailed information about a specific token."""
        try:
            info = await self.solana.get_token_info(token_address)
            
            # Get model's analysis of the token
            analysis_prompt = (
                f"Analyze this Solana token data and provide insights in your Cheshire cat style. "
                f"Include price, volume, and any notable patterns: {json.dumps(info)}"
            )
            
            analysis = await self.get_model_response(
                analysis_prompt,
                "You are analyzing token data. Focus on price trends, volume, and market patterns."
            )
            return analysis
        except Exception as e:
            logger.error(f"Error getting token info: {e}")
            return "The token seems to have vanished into the blockchain mist... 🎭"

    async def analyze_wallet(self, address: str) -> str:
        """Analyze a Solana wallet with Cheshire's insights."""
        try:
            analysis = await self.solana.analyze_wallet(address)
            
            # Get model's analysis of the wallet
            analysis_prompt = (
                f"Analyze this Solana wallet's contents and activity. Consider token holdings, "
                f"NFTs, and transaction patterns: {json.dumps(analysis)}"
            )
            
            response = await self.get_model_response(
                analysis_prompt,
                "You are analyzing a Solana wallet. Focus on holdings, activity patterns, and potential opportunities."
            )
            return response
        except Exception as e:
            logger.error(f"Error analyzing wallet: {e}")
            return "Oh my... The blockchain mist clouds my vision! 🎭"

    async def get_market_insight(self) -> str:
        """Get real-time market insights."""
        try:
            market_data = await self.solana.get_market_analysis()
            
            # Get model's analysis of market data
            analysis_prompt = (
                f"Analyze this market data and provide insights about trending tokens, "
                f"volume patterns, and market sentiment: {market_data}"
            )
            
            analysis = await self.get_model_response(
                analysis_prompt,
                "You are analyzing market data. Focus on trends, volume leaders, and market sentiment."
            )
            return analysis
        except Exception as e:
            logger.error(f"Error getting market insight: {e}")
            return "The market charts are particularly mysterious today... 🎭"

    async def chat(self, message: str) -> Dict[str, Any]:
        """Process a chat message with blockchain insights."""
        try:
            # Check for token info request
            if message.lower().startswith(("token ", "show token ")):
                token_address = message.split()[-1]
                response = await self.get_token_info(token_address)
                return {"response": response}
            
            # Check for wallet analysis request
            if "analyze wallet" in message.lower() and len(message.split()) > 2:
                address = message.split()[-1]
                response = await self.analyze_wallet(address)
                return {"response": response}
            
            # Check for market analysis request
            if message.lower() in ["market", "markets", "show market", "show markets"]:
                response = await self.get_market_insight()
                return {"response": response}
            
            # Handle help command
            if message.lower() in ["help", "commands", "?", "what can you do"]:
                help_prompt = (
                    "List your available commands and capabilities in a playful Cheshire cat style. "
                    "Include token analysis, market insights, and wallet analysis features."
                )
                response = await self.get_model_response(help_prompt)
                return {"response": response}
            
            # Get general response from model
            response = await self.get_model_response(
                message,
                "You are having a general conversation about blockchain, Solana, and $GRIN."
            )
            return {"response": response}
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {"response": "Oh my... A glitch in the blockchain matrix! 🎭"}

    async def close(self):
        """Close the terminal and cleanup resources."""
        await self.model.close()

def get_terminal() -> CheshireTerminal:
    """Materialize a new instance of the Cheshire Terminal."""
    return CheshireTerminal()

# Direct terminal access
if __name__ == "__main__":
    terminal = get_terminal()
    
    async def test_terminal():
        try:
            test_messages = [
                "What's Solana?",
                "token So11111111111111111111111111111111111111112",  # SOL token address
                "market"
            ]
            
            for msg in test_messages:
                print(f"\nTrader: {msg}")
                response = await terminal.chat(msg)
                print(f"Cheshire: {response.get('response', 'The market mist clouds my vision... 🎭')}")
        finally:
            await terminal.close()
    
    asyncio.run(test_terminal())
