import aiohttp
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    base_url: str = "http://192.168.1.206:11439/v1"
    timeout: int = 60

class LocalModelClient:
    """Client for interacting with local exo cluster models."""
    
    def __init__(self, config: ModelConfig = ModelConfig()):
        self.config = config
        self.session = None
        
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
        
    async def list_models(self) -> List[Dict[str, Any]]:
        """Get available models from the local cluster."""
        try:
            session = await self.get_session()
            async with session.get(f"{self.config.base_url}/models") as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Get a chat completion from the local model."""
        try:
            session = await self.get_session()
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            async with session.post(
                f"{self.config.base_url}/chat/completions",
                json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            return {
                "error": str(e),
                "choices": [{
                    "message": {
                        "content": "I seem to be having trouble connecting to my thoughts... 🎭"
                    }
                }]
            }

    async def completion(
        self,
        prompt: str,
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Get a text completion from the local model."""
        try:
            session = await self.get_session()
            payload = {
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            async with session.post(
                f"{self.config.base_url}/completions",
                json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Error in completion: {e}")
            return {
                "error": str(e),
                "choices": [{
                    "text": "I seem to be having trouble connecting to my thoughts... 🎭"
                }]
            }

    async def get_embeddings(
        self,
        texts: List[str],
        model: str = "default"
    ) -> Dict[str, Any]:
        """Get embeddings for the provided texts."""
        try:
            session = await self.get_session()
            payload = {
                "model": model,
                "input": texts
            }
            
            async with session.post(
                f"{self.config.base_url}/embeddings",
                json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Error getting embeddings: {e}")
            return {
                "error": str(e),
                "data": []
            }

    def format_cheshire_response(self, response: Dict[str, Any]) -> str:
        """Format model response in Cheshire's style."""
        try:
            if "error" in response:
                return (
                    "Oh my... The mist clouds my vision! 🎭\n"
                    f"Error: {response['error']}"
                )
            
            if "choices" in response:
                if isinstance(response["choices"][0].get("message"), dict):
                    # Chat completion
                    content = response["choices"][0]["message"]["content"]
                else:
                    # Regular completion
                    content = response["choices"][0]["text"]
                
                # Add Cheshire's style if not present
                if not any(emoji in content for emoji in ["😸", "✨", "🎭"]):
                    content += " 😸"
                
                return content
            
            return "Curiouser and curiouser... The response seems to have vanished! 🎭"
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "Something curious happened while processing my thoughts... ✨"

    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close()

# Example usage
async def main():
    client = LocalModelClient()
    try:
        # List available models
        models = await client.list_models()
        print("Available Models:", json.dumps(models, indent=2))
        
        # Test chat completion
        chat_response = await client.chat_completion([
            {"role": "user", "content": "Tell me about Solana in Cheshire cat style"}
        ])
        print("\nChat Response:", client.format_cheshire_response(chat_response))
        
    finally:
        await client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
