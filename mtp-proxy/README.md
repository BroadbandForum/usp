# mtp-proxy
A Python implementation of a USP MTP Proxy.


To Do List:
~~1. CoAP reply-to header~~ :: DONE
~~2. STOMP reply-to-dest header~~ :: DONE
3. WebSockets
4. More testing
5. Handle the STOMP subscribe-dest header
6. TLS / DTLS
7. mDNS :: could be used to discover the EndpointURL/EndpointDestination
    instead of using the values from proxy.json, but then we would need
    to know the EndpointID in proxy.json (which wouldn't change as often
    as the Endpoint's IP Address)
8. Get the IP Address from the environment instead of using "localhost"
    for CoAP
