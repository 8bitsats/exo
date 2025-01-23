import requests
import json
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AstraLangflowClient:
    def __init__(self, api_token: str):
        """Initialize the Astra Langflow API client.
        
        Args:
            api_token: The Astra API token for authentication
        """
        self.api_token = api_token
        self.base_url = "https://api.langflow.astra.datastax.com"
        
    def run_flow(self, 
                 flow_id: str,
                 message: str,
                 input_type: str = "chat",
                 output_type: str = "chat",
                 tweaks: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a flow with the given parameters.
        
        Args:
            flow_id: The ID of the flow to run
            message: The input message
            input_type: Type of input (default: "chat")
            output_type: Type of output (default: "chat")
            tweaks: Optional flow-specific parameters
            
        Returns:
            The API response as a dictionary
        """
        url = f"{self.base_url}/lf/{flow_id}/api/v1/run/cheshireterminal"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        
        # Match exact payload structure from curl command
        payload = {
            "input_value": message,
            "output_type": output_type,
            "input_type": input_type,
            "tweaks": tweaks or {
                "Agent-YDVUV": {},
                "ChatInput-KIX8A": {},
                "ChatOutput-uB3vz": {},
                "URL-qeVXs": {},
                "CalculatorTool-mw90V": {}
            }
        }
        
        # Log request details for debugging
        logger.debug(f"Making request to URL: {url}")
        logger.debug(f"Headers: {json.dumps(headers, indent=2)}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                params={"stream": "false"}
            )
            
            # Log response details
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            try:
                response_json = response.json()
                logger.debug(f"Response body: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.debug(f"Raw response text: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Error response: {json.dumps(error_detail, indent=2)}")
                except json.JSONDecodeError:
                    logger.error(f"Raw error response: {e.response.text}")
            raise

# Example usage:
if __name__ == "__main__":
    # Initialize client with your API token
    client = AstraLangflowClient(
        "AstraCS:hJxvZgaWKsMfuxsvDlWcLyCD:7e1a25f2abc17024141bc1cc95af5c221a68cd95f2e51a0c69369ff44d6cf4b9"
    )
    
    # Example tweaks matching the curl command
    default_tweaks = {
        "Agent-YDVUV": {},
        "ChatInput-KIX8A": {},
        "ChatOutput-uB3vz": {},
        "URL-qeVXs": {},
        "CalculatorTool-mw90V": {}
    }
    
    # Run a flow
    try:
        result = client.run_flow(
            flow_id="9412ef3b-4d94-4559-b761-0afcf10040b4",
            message="Hello from CheshireTerminal!",
            tweaks=default_tweaks
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error running flow: {e}")
