<!-- Reference Links -->
[1]:	https://github.com/BroadbandForum/usp/tree/master/data-model "TR-181 Issue 2 Device Data Model for TR-069"
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
[17]: https://www.ietf.org/rfc/rfc2234.txt "RFC 2234 Augmented BNF for Syntax Specifications: ABNF"
[18]: https://www.ietf.org/rfc/rfc3986.txt "RFC 3986 Uniform Resource Identifier (URI): Generic Syntax"
[19]: https://www.ietf.org/rfc/rfc2141.txt "RFC 2141 URN Syntax"
[Conventions]: https://www.ietf.org/rfc/rfc2119.txt "Key words for use in RFCs to Indicate Requirement Levels"


# Message Transfer Protocols

USP messages are sent between Endpoints over one or more Message Transfer Protocols.

Note: Message Transfer Protocol was a term adopted to avoid confusion with the term “Transport”, which is often overloaded to include both application layer (i.e. CoAP) and the actual OSI Transport layer (i.e. UDP). Throughout this document, Message Transfer Protocol (MTP) refers to application layer transport.

The requirements for each individual Message Transfer Protocol is covered in a section of this document. This version of the specification includes definitions for:

*	The [Constrained Application Protocol (CoAP)](./coap/).
* WebSockets

*Note: In this DRAFT version of the specification, the binding definition for WebSockets is TBD. It will be fully defined in the final 1.0 release.*

## Securing MTPs

<a id="securing_mtps" />

<!--
USP contains its own [application layer security mechanism](/specification/security/). While use of this security is necessary, it may not always be sufficient for certain deployment scenarios.
-->

USP recommends the following requirement on use of MTP security:

**R-MTP.0** – The Message Transfer Protocol MUST use secure transport when USP messages cross inter-network boundaries.

For example, it may not be necessary to use MTP layer security when within an end-user’s local area network (LAN). It is necessary to secure transport to and from the Internet, however.

[<-- Discovery](/specification/discovery/)
[--> CoAP as a Message Transfer Protocol](/specification/mtp/coap/)

<!--
### MTP Message Protection

In USP, a trust relationship is established between controllers and agents using the end-to-end security mechanism. This section provides additional security functions specific to the transfer of USP messages between USP endpoints which can include intermediate points such as MTP proxies.

The purpose of MTP message protection is to ensure the confidentiality and integrity of the payload that is transferred between USP endpoints. While the protocol (e.g., TLS, DTLS) used by the MTP is dependent on the type of MTP and are further described in the section associated with the MTP, the following requirements in this section are relevant to each type of MTP.

**R-MTP.1** – MTP endpoints MUST implement the capability to provide for the confidentiality and integrity of MTP payloads using MTP message encryption.

**R-MTP.2** – MTP endpoints MUST provide the capability to enable and disable MTP message encryption. The default setting is to enable MTP message encryption.

Because not all MTP endpoints will have MTP message encryption enabled, an MTP that establishes a communication with another MTP endpoint will need to adapt to the MTP message encryption capability of the other MTP endpoint.

**R-MTP.3** – When initiating an MTP session, the initiating MTP endpoint MUST attempt to initiate the session using MTP message encryption unless the MTP message encryption capability has been disabled for the initiating MTP endpoint.

**R-MTP.4** – If the MTP session cannot be initiated using the MTP message encryption, the initiating MTP endpoint MUST attempt to initiate the session without using MTP message encryption unless the capability to communicate with an MTP by not using MTP message encryption has been disabled for the initiating MTP endpoint.

#### Use of Certificate Validation in MTP Message Encryption

For MTP endpoints that use certificates in the establishment of the MTP message encryption function, the certificates that are presented by the MTP endpoints can be validated in order to establish a trust relationship between the MTP endpoints. The validation of the certificate can be performed by the MTP endpoint that initiated the session and/or by the MTP endpoint that is accepting the request for the session.

**R-MTP.5** – When initiating an MTP session that uses certificates, the initiating MTP endpoint MUST validate the certificate presented by the accepting MTP endpoint.

**R-MTP.6** – When initiating an MTP session that uses certificates, the accepting MTP endpoint MUST provide the capability to validate the certificate presented by the initiating MTP endpoint.

**R-MTP.7** – MTP endpoints that accept communication session requests MUST provide the capability to enable and disable MTP certificate validation. The default setting is to disable MTP certificate validation by accepting MTP endpoints of certificates presented by initiating MTP endpoints.

#### Use of Identity Validation in MTP Message Encryption

In some deployment scenarios validation of the identity of MTP endpoints is needed to ensure that the MTP endpoints that are involved in the transfer of messages have been validated. This is especially important when two MTP endpoints communicate across the Wide Area Network or Internet. However, within a Local Area Network or Customer Premises, validation of MTP endpoints is not necessary to provide the MTP message confidentiality and integrity via MTP message encryption.

**R-MTP.8** – MTP endpoints MUST implement the capability to provide for the validation of identities of the MTP endpoints involved in the transfer of messages using MTP message encryption.

**R-MTP.9** – MTP endpoints MUST provide the capability to enable and disable MTP validation of MTP identities. The default setting is to enable MTP validation of MTP identities.  
-->
