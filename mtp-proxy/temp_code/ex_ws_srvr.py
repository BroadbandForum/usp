from simple_websocket_server import WebSocketServer, WebSocket

class SimpleEcho(WebSocket):

    def handle(self):
        # echo message back to client
        print("Received a message")
        self.send_message(self.data)
        print("Responding to a message")

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

server = WebSocketServer('', 8080, SimpleEcho)
server.serve_forever()