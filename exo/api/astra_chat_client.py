import requests
import json
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AstraChatClient:
    """Client for interacting with Astra's chat endpoint with Cheshire's personality."""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.langflow.astra.datastax.com"
        self.flow_id = "9412ef3b-4d94-4559-b761-0afcf10040b4"
        
    def format_cheshire_response(self, message: str) -> str:
        """Format the response in Cheshire's style."""
        # Add Cheshire's signature elements
        if not message.startswith(("Ahh", "Hmm", "Purr")):
            message = "Ahh... " + message
        
        # Add emojis if none present
        if "😸" not in message and "✨" not in message and "🎭" not in message:
            message += " 😸"
            
        return message
        
    def chat(self, message: str) -> Dict[str, Any]:
        """Send a chat message and receive a response."""
        url = f"{self.base_url}/lf/{self.flow_id}/api/v1/run/cheshireterminal"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        
        # Simplified payload focusing on just the chat interaction
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        try:
            logger.debug(f"Sending chat message: {message}")
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                params={"stream": "false"}
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Format the response in Cheshire's style
            if isinstance(result, dict) and "response" in result:
                result["response"] = self.format_cheshire_response(result["response"])
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Chat request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Error response: {json.dumps(error_detail, indent=2)}")
                except json.JSONDecodeError:
                    logger.error(f"Raw error response: {e.response.text}")
            raise

def get_chat_client() -> AstraChatClient:
    """Factory function to create a chat client with the default API token."""
    return AstraChatClient(
        "AstraCS:hJxvZgaWKsMfuxsvDlWcLyCD:7e1a25f2abc17024141bc1cc95af5c221a68cd95f2e51a0c69369ff44d6cf4b9"
    )

# Example usage
if __name__ == "__main__":
    client = get_chat_client()
    
    try:
        # Test with some blockchain-related questions
        test_messages = [
            "How do smart contracts work?",
            "What are the benefits of DeFi?",
            "Can you explain NFTs?"
        ]
        
        for msg in test_messages:
            print(f"\nUser: {msg}")
            response = client.chat(msg)
            print(f"Cheshire: {response.get('response', 'No response')}")
            
    except Exception as e:
        print(f"Error: {e}")
