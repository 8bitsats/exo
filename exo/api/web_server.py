import asyncio
import json
import logging
import aiohttp
import ssl
import certifi
from aiohttp import web
from pathlib import Path
from typing import Dict, Any
from .cheshire_terminal import CheshireTerminal
from .solana_client import SolanaClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CheshireWebServer:
    def __init__(self, verify_ssl=False):
        self.terminal = CheshireTerminal()
        self.solana = SolanaClient()
        # Use the existing dashboard directory
        self.dashboard_path = Path("/Users/8bit/Desktop/CheshireTerminal/exo/cheshireterminal2/dashboard")
        self.verify_ssl = verify_ssl
        
        if not self.dashboard_path.exists():
            raise FileNotFoundError(f"Dashboard directory not found: {self.dashboard_path}")
        
        logger.info(f"Using dashboard path: {self.dashboard_path}")
        
    async def handle_token_analysis(self, request):
        """Handle token analysis requests."""
        try:
            data = await request.json()
            token_address = data.get('address')
            if not token_address:
                return web.Response(
                    text=json.dumps({"error": "Token address required"}),
                    content_type='application/json',
                    status=400
                )
            
            info = await self.solana.get_token_info(token_address)
            return web.Response(
                text=json.dumps(info),
                content_type='application/json'
            )
        except Exception as e:
            logger.error(f"Error in token analysis: {e}")
            return web.Response(
                text=json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )

    async def handle_market_data(self, request):
        """Handle market data requests."""
        try:
            analysis = await self.solana.get_market_analysis()
            return web.Response(
                text=json.dumps({"analysis": analysis}),
                content_type='application/json'
            )
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return web.Response(
                text=json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )

    async def handle_chat(self, request):
        """Handle chat messages."""
        try:
            data = await request.json()
            message = data.get('message')
            if not message:
                return web.Response(
                    text=json.dumps({"error": "Message required"}),
                    content_type='application/json',
                    status=400
                )
            
            response = await self.terminal.chat(message)
            return web.Response(
                text=json.dumps(response),
                content_type='application/json'
            )
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return web.Response(
                text=json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )

    async def handle_index(self, request):
        """Serve the index.html file."""
        try:
            index_path = self.dashboard_path / 'index.html'
            if not index_path.exists():
                logger.error(f"Index file not found: {index_path}")
                return web.Response(text="Dashboard not found", status=404)
            
            logger.info(f"Serving index file: {index_path}")
            return web.FileResponse(index_path)
        except Exception as e:
            logger.error(f"Error serving index: {e}")
            return web.Response(text=str(e), status=500)

    async def handle_static(self, request):
        """Serve static files from the dashboard directory."""
        try:
            path = request.match_info.get('path', '')
            file_path = self.dashboard_path / path
            
            logger.debug(f"Attempting to serve: {file_path}")
            
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return web.Response(status=404)
            
            return web.FileResponse(file_path)
        except Exception as e:
            logger.error(f"Error serving static file: {e}")
            return web.Response(text=str(e), status=500)

    @web.middleware
    async def cors_middleware(self, request, handler):
        """Handle CORS."""
        if request.method == 'OPTIONS':
            return await self.handle_preflight(request)
            
        response = await handler(request)
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Cache-Control': 'no-cache'
        })
        return response

    @web.middleware
    async def error_middleware(self, request, handler):
        """Handle errors gracefully."""
        try:
            response = await handler(request)
            return response
        except web.HTTPException as ex:
            return web.json_response(
                {'error': str(ex)},
                status=ex.status
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return web.json_response(
                {'error': str(e)},
                status=500
            )

    def setup_routes(self, app):
        """Setup server routes."""
        # API routes
        app.router.add_post('/api/token/analyze', self.handle_token_analysis)
        app.router.add_get('/api/market/data', self.handle_market_data)
        app.router.add_post('/api/chat', self.handle_chat)
        
        # Static files
        app.router.add_get('/', self.handle_index)
        app.router.add_static('/static', self.dashboard_path)
        app.router.add_get('/{path:.*}', self.handle_static)

    async def handle_preflight(self, request):
        """Handle CORS preflight requests."""
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600',
            'Cache-Control': 'no-cache'
        }
        return web.Response(headers=headers)

    async def start(self, host='localhost', port=8080):
        """Start the web server."""
        # Setup middleware
        middlewares = [
            self.cors_middleware,
            self.error_middleware
        ]
        
        app = web.Application(middlewares=middlewares)
        self.setup_routes(app)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info(f"🎭 Cheshire Terminal Dashboard running at http://{host}:{port}")
        return runner, site

async def main():
    server = CheshireWebServer(verify_ssl=False)
    runner, site = await server.start()
    
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
