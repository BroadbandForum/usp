<!-- Reference Links -->
[1]:	https://github.com/BroadbandForum/usp/tree/master/data-model "TR-181 Issue 2 Device:2 Data Model"
[2]: https://www.broadband-forum.org/technical/download/TR-069.pdf	"TR-069 Amendment 6	CPE WAN Management Protocol"
[3]:	https://www.broadband-forum.org/technical/download/TR-106_Amendment-8.pdf "TR-106 Amendment 8	Data Model Template for TR-069 Enabled Devices"
[4]:	https://tools.ietf.org/html/rfc7228 "RFC 7228	Terminology for Constrained-Node Networks"
[5]:	https://tools.ietf.org/html/rfc2136	"RFC 2136 Dynamic Updates in the Domain Name System"
[6]:	https://tools.ietf.org/html/rfc3007	"RFC 3007 Secure Domain Name System Dynamic Update"
[7]:	https://tools.ietf.org/html/rfc6763	"RFC 6763 DNS-Based Service Discovery"
[8]:	https://tools.ietf.org/html/rfc6762	"RFC 6762 Multicast DNS"
[9]:	https://tools.ietf.org/html/rfc7252	"RFC 7252 The Constrained Application Protocol (CoAP)"
[10]:	https://tools.ietf.org/html/rfc7390	"RFC 7390 Group Communication for the Constrained Application Protocol (CoAP)"
[11]:	https://tools.ietf.org/html/rfc4033	"RFC 4033 DNS Security Introduction and Requirements"
[12]:	https://developers.google.com/protocol-buffers/docs/proto3 "Protocol Buffers v3	Protocol Buffers Mechanism for Serializing Structured Data Version 3"
[13]: https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries "IEEE Registration Authority"
[14]: https://tools.ietf.org/html/rfc4122 "RFC 4122 A Universally Unique IDentifier (UUID) URN Namespace"
[15]: https://tools.ietf.org/html/rfc5280 "RFC 5290 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[16]: https://tools.ietf.org/html/rfc6818 "RFC 6818 Updates to the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[17]: https://tools.ietf.org/html/rfc2234 "RFC 2234 Augmented BNF for Syntax Specifications: ABNF"
[18]: https://tools.ietf.org/html/rfc3986 "RFC 3986 Uniform Resource Identifier (URI): Generic Syntax"
[19]: https://tools.ietf.org/html/rfc2141 "RFC 2141 URN Syntax"
[20]: https://tools.ietf.org/html/rfc6455 "RFC 6455 The WebSocket Protocol"
[21]: https://stomp.github.io/stomp-specification-1.2.html "Simple Text Oriented Message Protocol"
[22]: https://tools.ietf.org/html/rfc5246 "The Transport Layer Security (TLS) Protocol Version 1.2"
[23]: https://tools.ietf.org/html/rfc6347 "Datagram Transport Layer Security Version 1.2"
[Conventions]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"


# Appendix III - Device Proxy

This Annex describes a Theory of Operations for the `Device.ProxiedDevice.` object
defined in the [Device:2 Data Model][1].

The `Device.ProxiedDevice` table is defined as:

> "Each entry in the table is a ProxiedDevice object that is a mount point. Each ProxiedDevice represents distinct hardware Devices. ProxiedDevice objects are virtual and abstracted representation of functionality that exists on hardware other than that which the Agent is running."

An implementation of the `Device.ProxiedDevice.` object may be used in an IoT Gateway that proxies devices that are connected to it via technologies other tha USP such as Z-Wave, ZigBee, Wi-Fi, etc. By designating a table of `ProxiedDevice` objects, each defined as a mount point, this allows a data model with objects that are mountable to be used to represent the capabilities of each of the `ProxiedDevice` table instances.

For example, if `Device.Wifi.` and `Device.TemperatureSensor.` objects modeled by the Agent, the `Device.ProxiedDevice.1.Wifi.Radio.1.` models a distinctly separate hardware device and has no relationship with `Device.Wifi.Radio.1.`. The `ProxiedDevice` objects may each represent entirely different types of devices each with a different set of objects. The `ProxiedDevice.1.TemperatureSensor.1.` object has no physical relationship to `ProxiedDevice.2.TemperatureSensor.1.` as they represent temperature sensors that exist on separate hardware. The mount point allows `Device.ProxiedDevice.1.WifiRadio.` and `Device.ProxiedDevice.1.TemperatureSensor.` to represent the full set of capabilities for the device being proxied. This provides a Controller a distinct path to each `ProxiedDevice` object.
