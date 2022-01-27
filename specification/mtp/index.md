# Message Transfer Protocols {#sec:mtp}

USP messages are sent between Endpoints over one or more Message Transfer Protocols.

*Note: Message Transfer Protocol was a term adopted to avoid confusion with the term "Transport", which is often overloaded to include both application layer (e.g. WebSocket) and the actual OSI Transport layer (e.g. TCP). Throughout this document, Message Transfer Protocol (MTP) refers to application layer transport.*

## Generic Requirements

The requirements in this section are common to all MTPs.

### Supporting Multiple MTPs

Agents and Controllers may support more than one MTP. When an Agent supports multiple MTPs, the Agent may be configured with Parameters for reaching a particular Controller across more than one MTP. When an Agent needs to send a Notification to such a Controller, the Agent can be designed (or possibly configured) to select a particular MTP, to try sending the Notification to the Controller on all MTPs simultaneously, or to try MTPs sequentially. USP has been designed to allow Endpoints to recognize when they receive a duplicate Message and to discard any duplicates. Endpoints will always send responses on the same MTP where the Message was received.

### Securing MTPs {#sec:securing-mtps}

This specification places the following requirement for encrypting MTP headers and payloads on USP implementations that are intended to be used in environments where USP Messages will be transported across the Internet:

**[R-MTP.0]{}** – The Message Transfer Protocol MUST use secure transport when USP Messages cross inter-network boundaries.

For example, it may not be necessary to use MTP layer security when within an end-user’s local area network (LAN). It is necessary to secure transport to and from the Internet, however. If the device implementer can reasonably expect Messages to be transported across the Internet when the device is deployed, then the implementer needs to ensure the device supports encryption of all MTP protocols.

MTPs that operate over UDP will be expected to implement, at least, DTLS 1.2 as defined in [@RFC6347].

MTPs that operate over TCP will be expected to implement, at least, TLS 1.2 as defined in [@RFC5246].

Specific requirements for implementing these are provided in the individual MTP sections.

**[R-MTP.1]{}** – When TLS or DTLS is used to secure an MTP, an Agent MUST require the MTP peer to provide an X.509 certificate.

**[R-MTP.2]{}** - An Agent capable of obtaining absolute time SHOULD wait until it has accurate absolute time before establishing TLS or DTLS encryption to secure MTP communication.  If an Agent for any reason is unable to obtain absolute time, it can establish TLS or DTLS without waiting for accurate absolute time. If an Agent chooses to establish TLS or DTLS before it has accurate absolute time (or if it does not support absolute time), it MUST ignore those components of the received X.509 certificate that involve absolute time, e.g. not-valid-before and not-valid-after certificate restrictions.

**[R-MTP.3]{}** - An Agent that has obtained an accurate absolute time MUST validate those components of the received X.509 certificate that involve absolute time.

**[R-MTP.4]{}** - When an Agent receives an X.509 certificate while establishing TLS or DTLS encryption of the MTP, the Agent MUST execute logic that achieves the same results as in the mandatory decision flow elements (identified with "MUST") from @fig:receiving-a-x509-certificate.

**[R-MTP.4a]{}** - When an Agent receives an X.509 certificate while establishing TLS or DTLS encryption of the MTP, the Agent SHOULD execute logic that achieves the same results as in the optional decision flow elements (identified with "OPT") from @fig:receiving-a-x509-certificate.

![Receiving a X.509 Certificate](validate-cert.png){#fig:receiving-a-x509-certificate}

*Note: The .local and .home.arpa domains are defined by the IETF as "Special-Use Domains" for use inside any LAN.  It is not possible for an external Certificate Authority (CA) to vouch for whether a LAN device "owns" a particular name in one of these domains (inside a particular LAN) and these LAN networks have no internal CA.  Therefore, it is not possible to validate FQDNs within these domains.  The Internet Assigned Numbers Authority (IANA) maintains a registry of [Special Use Domains](https://www.iana.org/assignments/special-use-domain-names/special-use-domain-names.xhtml).*

### USP Record Encapsulation {#sec:usp-record-encapsulation}

The USP Record Message is defined as the Message Transfer Protocol (MTP) payload, encapsulating a sequence of datagrams that comprise the USP Message as well as providing additional metadata needed for integrity protection, payload protection and delivery of fragmented USP Messages. Additional metadata fields are used to identify the E2E session context, determine the state of the segmentation and reassembly function, acknowledge received datagrams, request retransmissions, and determine the type of encoding and security mechanism used to encode the USP Message.

Following are the fields contained within a USP Record. When not explicitly set or included in the Record, the fields have a default value based on the type of field. For strings, the default value is an empty byte string. For numbers (uint64) and enumerations, the default value is 0. For repeated bytes, the default value is an empty byte string. The term "Optional" means it is not necessary to include the field in a sent Record. The receiving Endpoint will use default values for fields not included in a received Record. "Required" fields are always included. A Record without a "Required" field will fail to be processed by a receiving Endpoint. "Repeated" fields can be included any number of times, including zero.

#### Record Definition {#sec:record-definition}

*Note: This version of the specification defines Record in [Protocol Buffers v3](#sec:encoding). This part of the specification may change to a more generic description (normative and non-normative) if further encodings are specified in future versions.*

`string version`

Required. Version (Major.Minor) of the USP Protocol (i.e., "1.0" or "1.1").

`string to_id`

Required. Receiving/Target USP Endpoint Identifier.

`string from_id`

Required. Originating/Source USP Endpoint Identifier.

`enum PayloadSecurity payload_security`

Optional. An enumeration of type PayloadSecurity. When the payload is present,
this indicates the protocol or mechanism used to secure the payload (if any) of the USP Message.
The value of `TLS12` means TLS 1.2 or later (with backward compatibility to TLS 1.2) will be
used to secure the payload (see [](#sec:tls-payload-encapsulation) for more information).

Valid values are:

```
PLAINTEXT (0)
TLS12 (1)
```

`bytes mac_signature`

Optional. When integrity protection of non-payload fields is performed, this is the message authentication code or signature used to ensure the integrity of the non-payload fields of the USP Record.

`bytes sender_cert`

Optional. The PEM encoded certificate, or certificate chain, of the sending USP Endpoint used to provide the signature in the `mac_signature` field, when integrity protection is used and the payload security mechanism doesn’t provide the mechanism to generate the `mac_signature`.

`oneof record_type`

Required. This field contains one of the types given below:

`NoSessionContextRecord no_session_context`

`SessionContextRecord session_context`

`WebSocketConnectRecord websocket_connect`

`MQTTConnectRecord mqtt_connect`

`STOMPConnectRecord stomp_connect`

`DisconnectRecord disconnect`

##### NoSessionContextRecord fields

The following describe the fields included if `record_type` is `no_session_context`.

`bytes payload`

Required. The USP Message.

##### SessionContextRecord fields

The following describe the fields included if `record_type` is `session_context`.

`uint64 session_id`

Required. This field is the Session Context identifier.

`uint64 sequence_id`

Required. Datagram sequence identifier. Used only for exchange of USP Records with an E2E Session Context. The field is initialized to 1 when starting a new Session Context and incremented after each sent USP Record.

*Note: Endpoints maintain independent values for received and sent sequence_id for a Session Context, based respectively on the number of received and sent Records.*

`uint64 expected_id`

Required. This field contains the next `sequence_id` the sender is expecting to receive, which implicitly acknowledges to the recipient all transmitted datagrams less than `expected_id`. Used only for exchange of USP Records with an E2E Session Context.

`uint64 retransmit_id`

Optional. Used to request a USP Record retransmission by a USP Endpoint to request a missing USP Record using the missing USP Record's anticipated `sequence_id`. Used only for exchange of USP Records with an E2E Session Context. Will be received as `0` when no retransmission is requested.

`enum PayloadSARState payload_sar_state`

Optional. An enumeration of type PayloadSARState. When payload is present, indicates the segmentation and reassembly state represented by the USP Record. Valid values are:

```
NONE (0)
BEGIN (1)
INPROCESS (2)
COMPLETE (3)
```

`enum PayloadSARState payloadrec_sar_state`

Optional. An enumeration of type PayloadSARState. When payload segmentation is being performed, indicates the segmentation and reassembly state represented by an instance of the payload datagram. If `payload_sar_state` = `0` (or is not included or not set), then `payloadrec_sar_state` will be `0` (or not included or not set). Valid values are:

```
NONE (0)
BEGIN (1)
INPROCESS (2)
COMPLETE (3)
```

`repeated bytes payload`

Optional. This repeated field is a sequence of zero, one, or multiple datagrams. It contains the Message, in either `PLAINTEXT` or encrypted format. When using `TLS12` payload security, this contains the encrypted TLS records, either sequentially in a single `payload` field, or divided into multiple `payload` fields. When using `PLAINTEXT` payload security there will be a single `payload` field for any Message being sent.

##### WebSocketConnectRecord fields

This Record type has no fields.

##### MQTTConnectRecord fields

The following describe the fields included if `record_type` is `mqtt_connect`.

`enum MQTTVersion version`

Required. The MQTT protocol version used by the USP Endpoint to send this Record. Valid values are:

```
V3_1_1 (0)
V5 (1)
```

`string subscribed_topic`

Required. A MQTT Topic where the USP Endpoint sending this Record can be reached (i.e. a MQTT Topic it is subscribed to).

##### STOMPConnectRecord fields

The following describe the fields included if `record_type` is `stomp_connect`.

`enum STOMPVersion version`

Required. The STOMP protocol version used by the USP Endpoint to send this Record. Valid values are:

```
V1_2 (0)
```

`string subscribed_destination`

Required. A STOMP Destination where the USP Endpoint sending this Record can be reached (i.e. a STOMP Destination it is subscribed to).

##### DisconnectRecord fields

The following describe the fields included if `record_type` is `disconnect`.

`fixed32 reason_code`

Optional. A code identifying the reason of the disconnect.

`string reason`

Optional. A string describing the reason of the disconnect.

### USP Record Errors {#sec:usp-record-errors}

A variety of errors can occur while establishing and during a USP communication flow. In order to signal such problems to the other Endpoint while processing an incoming E2E Session Context Record or a Record containing a Message of the type Request, an Endpoint encountering such a problem can create a USP Record containing a Message of type Error and transmit it over the same MTP and connection which was used when the error was encountered.

For this mechanism to work and to prevent information leakage, the sender causing the problem needs to be able to create a valid USP Record containing a valid source Endpoint ID and a correct destination Endpoint ID. In addition a MTP specific return path needs to be known so the error can be delivered.

**[R-MTP.5]{}** - A recipient of an erroneous USP Record MUST create a Record with a Message of type Error and deliver it to sender if the source Endpoint ID is valid, the destination Endpoint ID is its own, and a MTP-specific return path is known. If any of those criteria on the erroneous Record are not met or the Record is known to contain a USP Message of types Response or Error, it MUST be ignored.

The following error codes (in the range 7100-7199) are defined to allow the Error to be more specifically indicated. Additional requirements for these error codes are included in the specific MTP definition, where appropriate.

| Code | Name | Description
| :----- | :------------ | :---------------------- |
| `7100` | Record could not be parsed	| This error indicates the received USP Record could not be parsed. |
| `7101` | Secure session required | This error indicates USP layer [](#sec:secure-message-exchange) is required.|
| `7102` | Secure session not supported | This error indicates USP layer [](#sec:secure-message-exchange) was indicated in the received Record but is not supported by the receiving Endpoint. |
| `7103` | Segmentation and reassembly not supported | This error indicates segmentation and reassembly was indicated in the received Record but is not supported by the receiving Endpoint. |
| `7104` | Invalid Record value | This error indicates the value of at least one Record field was invalid. |
| `7105` | Session Context terminated | This error indicates an existing Session Context [](#sec:establishing-an-e2e-session-context) is being terminated. |
| `7106` | Session Context not allowed | This error indicates use of Session Context [](#sec:establishing-an-e2e-session-context) is not allowed or not supported. |

### Connect and Disconnect Record Types

A Connect Record is a subgroup of Record types (`record_type`), there is one Record type per USP MTP in this subgroup. These Records are used to assert the USP Agent presence and exchange needed information for proper start of communication between Agent and Controller, the presence information is specifically useful when using brokered MTPs.

**[R-MTP.6]{}** - If a USP Agent has the necessary information to create a Connect Record, it MUST send the associated Connect Record, specific for the MTP in use, after it has successfully established an MTP communications channel to a USP Controller.

The `DisconnectRecord` is a Record type used by a USP Agent to indicate it wishes to end an on-going communication with a USP Controller. It can be used for presence information, for sending supplemental information about the disconnect event and to force the remote USP Endpoint to purge some cached information about the current session.

**[R-MTP.7]{}** - The USP Agent SHOULD send a `DisconnectRecord` to the USP Controller before disconnecting from an MTP communications channel. Upon receiving a `DisconnectRecord`, a USP Controller MUST clear all cached information relative to an existing E2E Session Context with that Endpoint, including the information that a previous E2E Session Context was established.

It is not mandatory for a USP Endpoint to close its MTP connection after sending or receiving a `DisconnectRecord`.

**[R-MTP.8]{}** - After sending or receiving a `DisconnectRecord` and maintaining the underlying MTP communications channel or after establishing a new MTP communications channel, the USP Endpoint MUST send or receive the correct Connect Record type before exchanging any other USP Records.

**[R-MTP.9]{}** - A `DisconnectRecord` SHOULD include the `reason_code` and `reason` fields with an applicable code from [](#sec:usp-record-errors).
