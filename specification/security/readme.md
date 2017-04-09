<!-- Reference Links -->
[1]:	https://www.broadband-forum.org/technical/download/TR-181_Issue-2_Amendment-12.pdf "TR-181 Issue 2 Device Data Model for TR-069"
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
[Conventions]: https://www.ietf.org/rfc/rfc2119.txt "Key words for use in RFCs to Indicate Requirement Levels"

# Security

USP provides an end-to-end security mechanism in addition to any security provided by the Message Transfer Protocol.

**R-SEC.0** – All USP endpoints MUST implement the USP end-to-end security mechanism.

**R-SEC.1** – All USP messages MUST be secured by the USP end-to-end security mechanism.

The current discussion on the structure and requirements for the USP end-to-end security mechanism is available for Broadband Forum members to view on the BBF wiki at:

https://wiki.broadband-forum.org/display/BBF/Security+Discussion

## Authentication

Authentication of USP Endpoints to establish trust with each other *at the USP layer* is handled via the information and requirements in the `.ControllerTrust.` object of the data model.

**R.SEC.2** - USP Agents and Controllers MUST adhere to the Authentication requirements defined for the `.ControllerTrust.` object defined in the [Device:2 Data Model for TR-069 Devices and USP Agents][1].

## Access Control

Access Control covers the permission scheme that Controllers and Agents apply to each other. Access Control can be applied to single objects or parameters, or a set of object parameters, based on these schemes. The mechanism for adding, removing, and modifying schemes is defined in the USP data model.

**R.SEC.3** - USP Agents and Controllers MUST adhere to the Access Control requirements defined for the `.ControllerTrust.` object defined in the [Device:2 Data Model for TR-069 Devices and USP Agents][1].
