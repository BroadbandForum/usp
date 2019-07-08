<!-- Reference Links -->
[1]:	https://broadbandforum.github.io/usp-data-models/ "TR-181 Issue 2 Device:2 Data Model"
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

# STOMP Binding

1. [Handling of the STOMP Session](#handling_of_the_stomp_session)
    1. [Connecting a USP Endpoint to the STOMP Server](#connecting_a_usp_endpoint_to_the_stomp_server)
    2. [Handling the STOMP Heart Beat Mechanism](#handling_the_stomp_heart_beat_mechanisms)
2. [Mapping USP Endpoints to STOMP Destinations](#mapping_usp_endpoints_to_stomp_destinations)
    1. [Subscribing a USP Endpoint to a STOMP Destination](#subscribing_a_usp_endpoint_to_a_stomp_destination)
3. [Mapping USP Records to STOMP Frames](#mapping_usp_records_to_stomp_frames)
    1. [Handling ERROR Frames](#handling_error_frames)
    2. [Handling Other STOMP Frames](#handling_other_stomp_frames)
4. [Discovery Requirements](#discovery_requirements)
5. [STOMP Server Requirements](#stomp_server_requirements)
6. [MTP Message Encryption](#mtp_message_encryption)


The STOMP MTP transfers USP Records between USP endpoints using [version 1.2 of the STOMP protocol](https://stomp.github.io/stomp-specification-1.2.html) (further referred to as "STOMP Specification"), or the Simple Text Oriented Message Protocol. Messages that are transferred between STOMP clients utilize a message bus interaction model where the STOMP server is the messaging broker that routes and delivers messages based on the destination included in the STOMP header.

The following figure  depicts the transfer of the USP Records between USP Agents and Controllers.

<img src="STOMP-architecture.jpg"/>

Figure STOMP.1 - USP over STOMP Architecture

The basic steps for any USP Endpoint that utilizes a STOMP MTP are:

1. Negotiate TLS (if required/configured)
2. Connect to the STOMP Server
3. Maintain Heart Beats (if configured)
4. Subscribe to a Destination
5. Send USP Records

**R-STOMP.0** - USP Agents utilizing STOMP clients for message transport MUST support the `STOMPConn:1` and `STOMPController:1` data model profiles.

**R-STOMP.1** - USP Agents utilizing STOMP clients for message transport SHOULD support the `STOMPAgent:1` and `STOMPHeartbeat:1` data model profile.

<a id='handling_of_the_stomp_session' />

## Handling of the STOMP Session

When exchanging USP Records across STOMP MTPs, each USP Endpoint establishes a communications session with a STOMP server. These STOMP communications sessions are expected to be long lived and are reused for subsequent exchange of USP Records. A STOMP communications session is established using a handshake procedure as described in "Connecting a USP Endpoint to the STOMP Server" section below. A STOMP communications session is intended to be established as soon as the USP Endpoint becomes network-aware and is capable of sending TCP/IP messages.

When a STOMP communications session is no longer necessary, the STOMP connection is closed by the STOMP client, preferably by sending a `DISCONNECT` frame (see "Handling Other STOMP Frames" section below).

<a id='connecting_a_usp_endpoint_to_the_stomp_server' />

### Connecting a USP Endpoint to the STOMP Server

**R-STOMP.2** - USP Endpoints utilizing STOMP clients for message transport MUST send a `STOMP` frame to the STOMP server to initiate the STOMP communications session as defined in the "Connecting" section of the STOMP Specification.

**R-STOMP.3** - USP Endpoints that DO NOT utilize client certificate authentication MUST include the login and passcode STOMP headers in the STOMP frame.  For a USP Agent, if the `.STOMP.Connection.{i}.Username` parameter is implemented then its value will be the source for the `login` STOMP header, and if the `.STOMP.Connection.{i}.Password` parameter is implemented then its value will be the source for the `passcode` STOMP header.

**R-STOMP.4** - USP Endpoints sending a `STOMP` frame MUST include (in addition to other mandatory STOMP headers) an `endpoint-id` STOMP header containing the Endpoint ID of the USP Endpoint sending the frame.
NOTE: According to the STOMP Specification, the `STOMP` frame requires that "C style literal escapes" need to be used to encode any carriage return, line feed, or colon characters that are found within the UTF-8 encoded headers, and R-STOMP.4 requires the Endpoint ID to be included in those headers.  Since the Endpoint ID always contains colon characters, those will need to be escaped.

**R-STOMP.5** - USP Endpoints sending a STOMP frame MUST include a host STOMP header, if configured to do so. For a USP Agent the value MUST contain the value from the appropriate `.STOMP.Connection.{i}.VirtualHost` parameter if supported and not empty.

**R-STOMP.6** - If the USP Endpoint receives a `subscribe-dest` STOMP header in the `CONNECTED` frame, it MUST use the associated value when Subscribing to its destination (see "Subscribing a USP Endpoint to a STOMP Destination" section for more details).

**R-STOMP.7** - If the connection to the STOMP server is NOT successful then the USP Endpoint MUST enter a connection retry state. For a USP Agent the retry mechanism is based on the `STOMP.Connection.{i}.` retry parameters: `ServerRetryInitialInterval`, `ServerRetryIntervalMultiplier`, and `ServerRetryMaxInterval`.

<a id='handling_the_stomp_heart_beat_mechanisms' />

### Handling the STOMP Heart Beat Mechanism

The STOMP Heart Beat mechanism can be used to periodically send data between a STOMP client and a STOMP server to ensure that the underlying TCP connection is still available.  This is an optional STOMP mechanism and is negotiated when establishing the STOMP connection.

**R-STOMP.8** - If the `STOMP.Connection` instance's `EnableHeartbeats` parameter value is `True` then the USP Agent MUST negotiate the STOMP Heart Beat mechanism within the `STOMP` frame during the process of establishing the STOMP connection as is defined in the "Heart-beating" section of the STOMP Specification.

**R-STOMP.9** - If the `STOMP.Connection` instance's `EnableHeartbeats` parameter value is either `False` or not implemented then the USP Agent MUST either not send the `heart-beat` STOMP header in the `STOMP` frame or send "0,0" as the value of the `heart-beat` STOMP header in the `STOMP` frame.

**R-STOMP.10** - USP Agents negotiating the STOMP Heart Beat mechanism MUST use the `STOMP.Connection.{i}.OutgoingHeartbeat` and `STOMP.Connection.{i}.IncomingHeartbeat` parameter values within the `heart-beat` STOMP header as defined in the "Heart-beating" section of the STOMP Specification.

**R-STOMP.11** - USP Agents that have negotiated a STOMP Heart Beat mechanism with a STOMP server MUST adhere to the heart beat values (as defined in the "Heart-beating" section of the STOMP Specification) as returned in the `CONNECTED` frame.

<a id='mapping_usp_endpoints_to_stomp_destinations' />

## Mapping USP Endpoints to STOMP Destinations

USP Agents will have one STOMP destination per STOMP MTP independent of whether those STOMP MTPs use the same `STOMP.Connection` instance or a different one. The STOMP destination is either configured by the STOMP server via the USP custom `subscribe-dest` STOMP Header received in the `CONNECTED` frame (exposed in the `Device.LocalAgent.MTP.{i}.STOMP.DestinationFromServer` parameter) or taken from the `Device.LocalAgent.MTP.{i}.STOMP.Destination` parameter if there wasn't a `subscribe-dest` STOMP Header received in the `CONNECTED` frame. The USP custom `subscribe-dest` STOMP Header is helpful in scenarios where the USP Agent doesn't have a pre-configured destination as it allows the USP Agent to discover the destination.

A USP Controller will subscribe to a STOMP destination for each STOMP server that it is associated with. The USP Controller's STOMP destination needs to be known by the USP Agent (this is configured in the `Device.LocalAgent.Controller.{i}.MTP.{i}.STOMP.Destination` parameter) as it is used when sending a USP Record containing a Notification.

<a id='subscribing_a_usp_endpoint_to_a_stomp_destination' />

### Subscribing a USP Endpoint to a STOMP Destination

**R-STOMP.12** - USP Endpoints utilizing STOMP clients for message transport MUST subscribe to their assigned STOMP destination by sending a `SUBSCRIBE` frame to the STOMP server as defined in the "SUBSCRIBE" section of the STOMP Specification.

**R-STOMP.13** - USP Endpoints sending a `SUBSCRIBE` frame MUST include (in addition to other mandatory STOMP headers) a `destination` STOMP header containing the STOMP destination associated with the USP Endpoint sending the frame.

**R-STOMP.14** - USP Agents that receive a `subscribe-dest` STOMP Header in the `CONNECTED` frame MUST use that STOMP destination in the `destination` STOMP header when sending a `SUBSCRIBE` frame.

**R-STOMP.15** - USP Agents that have NOT received a `subscribe-dest` STOMP Header in the `CONNECTED` frame MUST use the STOMP destination found in the `Device.LocalAgent.MTP.{i}.STOMP.Destination` parameter in the `destination` STOMP header when sending a `SUBSCRIBE` frame.

**R-STOMP.16** - USP Agents that have NOT received a `subscribe-dest` STOMP Header in the `CONNECTED` frame and do NOT have a value in the `Device.LocalAgent.MTP.{i}.STOMP.Destination` parameter MUST terminate the STOMP communications session (via the `DISCONNECT` frame) and consider the MTP disabled.

**R-STOMP.17** - USP Endpoints sending a `SUBSCRIBE` frame MUST use an `ack` value of "auto".

<a id='mapping_usp_records_to_stomp_frames' />

## Mapping USP Records to STOMP Frames

A USP Record is sent from a USP Endpoint to a STOMP Server within a `SEND` frame. The STOMP Server delivers that USP Record to the destination STOMP Endpoint within a `MESSAGE` frame. When a USP Endpoint responds to the USP request, the USP Endpoint sends the USP Record to the STOMP Server within a `SEND` frame, and the STOMP Server delivers that USP Record to the destination USP Endpoint within a `MESSAGE` frame.

**R-STOMP.18** - USP Endpoints utilizing STOMP clients for message transport MUST send USP Records in a `SEND` frame to the STOMP server as defined in the "SEND" section of the STOMP Specification.

**R-STOMP.19** - USP Endpoints sending a `SEND` frame MUST include (in addition to other mandatory STOMP headers) a `content-length` STOMP header containing the length of the body included in the `SEND` frame.

**R-STOMP.20** - USP Endpoints sending a `SEND` frame MUST include (in addition to other mandatory STOMP headers) a `content-type` STOMP header with a value of "`application/vnd.bbf.usp.msg`", which signifies that the body included in the `SEND` frame contains a [Protocol Buffer][12] binary encoding message.

**R-STOMP.21** - USP Endpoints sending a `SEND` frame with content-type of `application/vnd.bbf.usp.msg` MUST include (in addition to other mandatory STOMP headers) a `reply-to-dest` STOMP header containing the STOMP destination that indicates where the USP Endpoint that receives the USP Record should send any response (if required).

**R-STOMP.22** - USP Endpoints sending a `SEND` frame with content-type of `application/vnd.bbf.usp.msg` MUST include the [Protocol Buffer][12] binary encoding of the USP Record as the body of the `SEND` frame.

**R-STOMP.23** - When a USP Endpoint receives a `MESSAGE` frame it MUST use the `reply-to-dest` included in the STOMP headers as the STOMP destination of the USP response (if a response is required by the incoming USP request).

<a id='handling_error_frames' />

### Handling USP Record errors and ERROR Frames

If a USP Endpoint receives a `MESSAGE` frame containing a USP Record that cannot be extracted for processing (e.g., text frame instead of a binary frame, malformed USP Record or USP Message, bad encoding), the receiving USP Endpoint will drop the USP Record if the STOMP  MESSAGE frame does not have a `usp-err-id` header or if the receiving Endpoint does not support the `application/vnd.bbf.usp.error` content-type value. If the receiving Endpoint does support the `application/vnd.bbf.usp.error` content-type value and the received STOMP MESSAGE frame had a `usp-err-id` header, the receiving Endpoint will issue a STOMP SEND frame of `application/vnd.bbf.usp.error` content-type value.

**R-STOMP.23a** - USP Endpoints MUST support STOMP content-type header value of `application/vnd.bbf.usp.error`.

**R-STOMP.23b** - A USP Endpoint MUST include a `usp-err-id` STOMP header in `SEND` frames of content-type `application/vnd.bbf.usp.msg`. The value of this header is:  `<USP Record to-id  > + "/" + <USP Message msg_id>`. Since the colon "`:`" is a reserved character in STOMP headers, all instances of "`:`" in the USP Record to-id MUST be expressed using an encoding of `\c`.

**R-STOMP.24** - When a USP Endpoint receives a `MESSAGE` frame containing a USP Record or an encapsulated USP Message within a USP Record that cannot be extracted for processing, the receiving USP Endpoint MUST ignore the USP Record if the received STOMP MESSAGE frame did not include a `usp-err-id` header.

**R-STOMP.24a** - When a USP Endpoint receives a MESSAGE frame containing a USP Record or an encapsulated USP Message within a USP Record that cannot be extracted for processing, the receiving USP Endpoint MUST send a STOMP SEND frame with an `application/vnd.bbf.usp.error` content-type header value if the received STOMP MESSAGE frame included a `usp-err-id` header.

**R-STOMP.24b** - A STOMP SEND frame with `application/vnd.bbf.usp.error` content-type MUST contain the received `usp-err-id` header, the destination header value set to the received `reply-to-dest` header, and a message body (formatted using UTF-8 encoding) with the following 2 lines:

* `err_code:<numeric code indicating the type of error that caused the overall message to fail>`

* `err_msg:<additional information about the reason behind the error>`

The specific error codes are listed in the MTP [Brokered USP Record Errors](/specification/mtp#brokered-usp-record-errors) section.  

The following is an example message. This example uses "`^@`" to represent the NULL octet that follows a STOMP body.

```
SEND
destination:/usp/the-reply-to-dest
content-type:application/vnd.bbf.usp.error
usp-err-id:cid\c3AA3F8\cusp-id-42/683

err_code:7100
err_msg:Field n is not recognized.^@
```

**R-STOMP.25** - If an `ERROR` frame is received by the USP Endpoint, the STOMP server will terminate the connection. In this case the USP Endpoint MUST enter a connection retry state. For a USP Agent the retry mechanism is based on the `STOMP.Connection.{i}.` retry parameters: `ServerRetryInitialInterval`, `ServerRetryIntervalMultiplier`, and `ServerRetryMaxInterval`.

<a id='handling_other_stomp_frames' />

### Handling Other STOMP Frames

**R-STOMP.26** - USP Endpoints utilizing STOMP clients for message transport MUST NOT send the transactional STOMP frames including: `BEGIN`, `COMMIT`, and `ABORT`.

**R-STOMP.27** - USP Endpoints utilizing STOMP clients for message transport MUST NOT send the acknowledgement STOMP frames including: `ACK` and `NACK`.

**R-STOMP.28** - USP Endpoints utilizing STOMP clients for message transport MAY send the following STOMP frames when shutting down a STOMP connection: `UNSUBSCRIBE` (according to the rules defined in the UNSUBSCRIBE section of the STOMP Specification) and `DISCONNECT` (according to the rules defined in the DISCONNECT section of the STOMP Specification).

**R-STOMP.29** - USP Endpoints utilizing STOMP clients for message transport that DID NOT receive a `subscribe-dest` STOMP Header in the `CONNECTED` frame when establishing the STOMP communications session MUST update their STOMP subscription when their destination is altered by sending the `UNSUBSCRIBE` STOMP frame (according to the rules defined in the UNSUBSCRIBE section of the STOMP Specification) and then re-subscribing as detailed in the "Subscribing a USP Endpoint to a STOMP Destination" section.

**R-STOMP.30** - USP Endpoints utilizing STOMP clients for message transport MAY receive a `RECEIPT` frame in which case the STOMP server is acknowledging that the corresponding client frame has been processed by the server.

<a id='discovery_requirements' />

## Discovery Requirements

The USP [discovery section](/specification/discovery) details requirements about the general usage of DNS, mDNS, and DNS-SD records as it pertains to the USP protocol.  This section provides further requirements as to how a USP Endpoint advertises discovery information when a STOMP MTP is being utilized.

**R-STOMP.31** - When creating a DNS-SD record, an Endpoint MUST set the DNS-SD "`path`" attribute equal to the value of the destination that it has subscribed to.

**R-STOMP.32** - When creating a DNS-SD record, an Endpoint MUST utilize the STOMP server's address information in the A and AAAA records instead of the USP Endpoint's address information.

<a id='stomp_server_requirements' />

## STOMP Server Requirements

**R-STOMP.33** - A STOMP server implementation MUST adhere to the requirements defined in the STOMP Specification.

**R-STOMP.34** - A STOMP server implementation MUST perform authentication of the STOMP client and ensure that a Remote USP Endpoint is only allowed to subscribe to the destination that is associated with the USP Endpoint.

**R-STOMP.35** - A STOMP server implementation SHOULD support both Client Certification Authentication and Username/Password Authentication mechanisms.

<a id='mtp_message_encryption' />

## MTP Message Encryption

STOMP MTP message encryption is provided using TLS certificates.

**R-STOMP.36** - USP Endpoints utilizing STOMP clients for message transport MUST implement TLS 1.2 [RFC 5246][22] or later with backward compatibility to TLS 1.2.

**R-STOMP.37** - STOMP server certificates MAY contain domain names and those domain names MAY contain domain names with wildcard characters per [RFC 6125](https://tools.ietf.org/html/rfc6125) guidance.

[<-- Message Transfer Protocols](/specification/mtp/)
[--> Message Encoding](/specification/encoding/)
