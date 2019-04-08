# mtp-proxy
A Python example implementation of a USP MTP Proxy.


## To Do List:
1. More testing
2. TLS / DTLS
3. mDNS :: could be used to discover the EndpointURL/EndpointDestination
    instead of using the values from proxy.json, but then we would need
    to know the EndpointID in proxy.json (which wouldn't change as often
    as the Endpoint's IP Address)
4. Debug/Fix incompatibility with Californium (Eclipse CoAP library)
    when exchanging large messages (ones that require blockwise 
    communications). 

## What is working:
1. STOMP Controller to WebSocket Client
2. CoAP Controller to WebSocket Client
    
## Things that aren't working:
1. STOMP Controller to a CoAP Agent (defect in CoAP library that prevents
    dynamic addition of resources, which are needed to bind to the STOMP
    reply-to-dest addresses)
2. WebSocket Controller to any Agent (defect in the WebSocket Client library
    that corrupts the outgoing message)
3. Any Controller to a STOMP Agent (no STOMP Broker)

## What's up with WebSocket Client Support:
* I've tried 3 separate WebSocket Client libraries and each of them result
   in item 2 from "Things that aren't working"
* I've decided to submit the lomond-based websocket_client.py code as the
   default solution as it seems like the simplest code base to debug
* Other solutions (websocket-client and websockets) both have implementations
   in websocket_client2.py and websocket_client3.py, but those files have
   been moved to another directory (temp_code) for safe keeping until one of
   the solutions can be fixed 

## Problems with the aiocoap library:
* Versions 0.2 and 0.3 result in the following error (probably a MacOS issue
   with IPv6 Options):
```
asyncio ERROR    Task exception was never retrieved
future: <Task finished coro=<Context.create_server_context() done, defined at /Users/jblackford/Development/mtpProxyEnv/lib/python3.7/site-packages/aiocoap/protocol.py:515> exception=AttributeError("module 'socket' has no attribute 'IPV6_RECVPKTINFO'")>
Traceback (most recent call last):
  File "/Users/jblackford/Development/mtpProxyEnv/lib/python3.7/site-packages/aiocoap/protocol.py", line 531, in create_server_context
    self.transport_endpoints.append((yield from TransportEndpointUDP6.create_server_transport_endpoint(new_message_callback=self._dispatch_message, new_error_callback=self._dispatch_error, log=self.log, loop=loop, dump_to=dump_to, bind=bind)))
  File "/Users/jblackford/Development/mtpProxyEnv/lib/python3.7/site-packages/aiocoap/transports/udp6.py", line 113, in create_server_transport_endpoint
    return (yield from cls._create_transport_endpoint(new_message_callback, new_error_callback, log, loop, dump_to, bind))
  File "/Users/jblackford/Development/mtpProxyEnv/lib/python3.7/site-packages/aiocoap/transports/udp6.py", line 87, in _create_transport_endpoint
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_RECVPKTINFO, 1)
AttributeError: module 'socket' has no attribute 'IPV6_RECVPKTINFO'
2019-04-04 14:47:54,011 stomp.py INFO     Received frame: 'MESSAGE', headers={'content-length': '313', 'destination': '/usp/agent/451de528-1c5a-4d6d-babc-3695a0c754f6', 'message-id': '73d0b21a-c269-4c5c-8064-cb6bc5fb0a59', 'content-type': 'application/vnd.bbf.usp.msg', 'subscription': '1', 'reply-to-dest': 'usp_ctl-rpc-response-127.0.1.1#1554303284460'}, len(body)=313
```
* The latest aiocoap library resolves this IPv6 issue, but causes issue 1
   (from "Things that aren't working" section)
* The latest version of aiocoap (0.4a1.post0) can be retrieved via the following command:
```commandline
> pip3 install --upgrade "git+https://github.com/chrysn/aiocoap#egg=aiocoap"
```

