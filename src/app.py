from flask import Flask
from config import config
from routes import Trip
import asyncio
import websockets
import threading

app = Flask(__name__)

def page_not_found(error):
    return "Not found page", 404

#Variable to store the clients connected through websocket 
clients = set()

#Method create and configure the websocket.
def background_socket_worker():
    #Inner method to handle the connections to the websocket and broadcast to all connected clients, the messages received
    async def handler(websocket, path):
        global clients
        clients.add(websocket)
        try:
            while True:
                message = await websocket.recv()
                for client in clients:
                    if client != websocket:
                        await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            clients.remove(websocket)
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(lambda websocket, path: handler(websocket, path), "localhost", 5564)
    loop.run_until_complete(start_server)
    loop.run_forever()

#Start the websocket in a different thread from the restapi.
background_thread = threading.Thread(target=background_socket_worker, daemon=True).start()

#Start the RestAPI
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.register_blueprint(Trip.main, url_prefix='/trips')
    app.run()

