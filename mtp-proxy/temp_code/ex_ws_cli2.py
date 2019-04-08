from lomond import WebSocket


websocket = WebSocket('ws://132.177.126.112:8080')
print("Connected to: ws://132.177.126.112:8080")

for event in websocket:
    if event.name == "connecting":
        print("Connecting...")
    elif event.name == "connected":
        print("Connected!")
    elif event.name == "ready":
        print("And... Ready!")
    elif event.name == "binary":
        print("Received a Binary Message; maybe it is a USP Record")
        print("Binary Message Contents: %s", str(event.data))
    elif event.name == "text":
        print("Received a Text Message; Discarding...")
        print("Text Message Contents: %s", event.text)
    elif event.name == "poll":
        websocket.send_text('Hello, World')
        print("Sent a message")
    elif event.name == "pong":
        print("Received Pong")
    elif event.name == "closed":
        print("Closed!")
    elif event.name == "disconnected":
        print("Disconnected!")
    else:
        print("Unknown event received: [" + event.name + "]")
