<!-- Reference Links -->
[1]:	https://usp-data-models.broadband-forum.org/ "Device Data Model"
[2]: https://www.broadband-forum.org/technical/download/TR-069.pdf	"TR-069 Amendment 6	CPE WAN Management Protocol"
[3]:	https://www.broadband-forum.org/technical/download/TR-106_Amendment-8.pdf "TR-106 Amendment 8	Data Model Template for TR-069 Enabled Devices and USP Agents"
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
[24]: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) "MQ Telemetry Transport 5.0"
[Conventions]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"


<h1>Broadband Forum TR-369: User Services Platform (USP)</h1>
<h2>Issue 1 Amendment 1</h2>
<h4>USP Version 1.1</h4>

You can find a pdf version of this document **[here](https://www.broadband-forum.org/technical/download/TR-369.pdf)**.

**Table of Contents**

Main Specification

1. [Introduction](#introduction)
2. [Architecture](./architecture)
3. [Discovery and Advertisement](./discovery)
4. [Message Transfer Protocols](./mtp)
5. [Message Encoding](./encoding)
6. [End to End Message Exchange](./e2e-message-exchange)
7. [Messages](./messages)
8. [Authentication and Authorization](./security)

Extensions

Annex A. [HTTP Bulk Data Transfer](./extensions/http-bulk-data-collection)

Appendix I. [Software Module Management](./extensions/software-module-management)

Appendix II. [Firmware Management](./extensions/firmware-management)

Appendix III. [Device Proxy](./extensions/device-proxy)

Appendix IV. [Proxying (Other)](./extensions/proxying/)

Appendix V. [IoT Data Model Theory of Operation](./extensions/iot/)


# Introduction

<a id="introduction" />

## Legal Notice

  The Broadband Forum is a non-profit corporation organized to create
  guidelines for broadband network system development and deployment.
  This Technical Report has been approved by members of the Forum.
  This Technical Report is subject to change.  This Technical Report
  is copyrighted by the Broadband Forum, and all rights are reserved.
  Portions of this Technical Report may be copyrighted by Broadband
  Forum members.

### Intellectual Property

  Recipients of this Technical Report are requested to submit, with
  their comments, notification of any relevant patent claims or other
  intellectual property rights of which they may be aware that might
  be infringed by any implementation of this Technical Report, or use
  of any software code normatively referenced in this Technical Report,
  and to provide supporting documentation.

### Terms of Use

#### License

  Broadband Forum hereby grants you the right, without charge, on a
  perpetual, non-exclusive and worldwide basis, to utilize the Technical
  Report for the purpose of developing, making, having made, using,
  marketing, importing, offering to sell or license, and selling or
  licensing, and to otherwise distribute, products complying with the
  Technical Report, in all cases subject to the conditions set forth
  in this notice and any relevant patent and other intellectual
  property rights of third parties (which may include members of
  Broadband Forum).  This license grant does not include the right to
  sublicense, modify or create derivative works based upon the
  Technical Report except to the extent this Technical Report includes
  text implementable in computer code, in which case your right under
  this License to create and modify derivative works is limited to
  modifying and creating derivative works of such code.  For the
  avoidance of doubt, except as qualified by the preceding sentence,
  products implementing this Technical Report are not deemed to be
  derivative works of the Technical Report.

#### NO WARRANTIES

  THIS TECHNICAL REPORT IS BEING OFFERED WITHOUT ANY WARRANTY WHATSOEVER,
  AND IN PARTICULAR, ANY WARRANTY OF NONINFRINGEMENT IS EXPRESSLY
  DISCLAIMED. ANY USE OF THIS TECHNICAL REPORT SHALL BE MADE ENTIRELY AT
  THE IMPLEMENTER'S OWN RISK, AND NEITHER THE BROADBAND FORUM, NOR ANY
  OF ITS MEMBERS OR SUBMITTERS, SHALL HAVE ANY LIABILITY WHATSOEVER TO
  ANY IMPLEMENTER OR THIRD PARTY FOR ANY DAMAGES OF ANY NATURE WHATSOEVER,
  DIRECTLY OR INDIRECTLY, ARISING FROM THE USE OF THIS TECHNICAL REPORT.

#### THIRD PARTY RIGHTS

  Without limiting the generality of Section 2 above, BROADBAND FORUM
  ASSUMES NO RESPONSIBILITY TO COMPILE, CONFIRM, UPDATE OR MAKE PUBLIC
  ANY THIRD PARTY ASSERTIONS OF PATENT OR OTHER INTELLECTUAL PROPERTY
  RIGHTS THAT MIGHT NOW OR IN THE FUTURE BE INFRINGED BY AN IMPLEMENTATION
  OF THE TECHNICAL REPORT IN ITS CURRENT, OR IN ANY FUTURE FORM. IF ANY
  SUCH RIGHTS ARE DESCRIBED ON THE TECHNICAL REPORT, BROADBAND FORUM
  TAKES NO POSITION AS TO THE VALIDITY OR INVALIDITY OF SUCH ASSERTIONS,
  OR THAT ALL SUCH ASSERTIONS THAT HAVE OR MAY BE MADE ARE SO LISTED.

  The text of this notice must be included in all copies of this
  Technical Report.

## Revision History

### Release 1.1

* Release contains specification for the User Services Platform 1.1.
  * Adds MQTT support as a Message Transfer Protocol
  * Adds a theory of operations for IoT control using USP Agents
  * Clarifications on protocol functions, error messages, and updates to examples

Valid versions for USP Agents as of this release include "1.1" and "1.0".

### Release 1.0.2

* Typographical and example fixes

### Release 1.0.1

* Added examples and clarifications to end-to-end messaging, use of endpoint ID,
typographical fixes

### Release 1.0

* Release contains specification for the User Services Platform 1.0.


## Editors

| Name  | Company | Email | Role |
| ------ | :-----: | :---: | :--- |
| Barbara Stark | AT&T | barbara.stark@att.com | Editor/USP Project Lead
| Tim Spets | Green Wave Systems | tim.spets@greenwavesystems.com | Editor/USP Project Lead
| Jason Walls | QA Cafe, LLC | jason@qacafe.com | Editor/Broadband User Services Work Area Director
| John Blackford | Arris | john.blackford@arris.com | Editor/Broadband User Services Work Area Director

## Acknowledgements

The following individuals are being acknowledged for their efforts in the testing and
development of this specification.

| Name  | Company | Email |
| ------ | :-----: | :---: |
| Jean-Didier Ott | Orange | jeandidier.ott@orange.com |
| Timothy Carey | Nokia | timothy.carey@nokia.com |
| Steven Nicolai | Arris | Steven.Nicolai@arris.com |
| Apostolos Papageorgiou | NEC | apostolos.Papageorgiou@neclab.eu |
| Mark Tabry  | Google | mtab@google.com |
| Klaus Wich | Huawei | klaus.wich@huawei.com |
| Daniel Egger | Axiros | daniel.egger@axiros.com |
| Bahadir Danisik | Nokia | bahadir.danisik@nokia.com |

## Executive Summary

<a id="executive_summary" />

This document describes the architecture, protocol, and data model that builds an intelligent User Services Platform. It is targeted towards application developers, application service providers, CPE vendors, consumer electronics manufacturers, and broadband and mobile network providers who want to expand the value of the end user’s network connection and their connected devices.

The term "connected device" is a broad one, applying to the vast array of network connected CPE, consumer electronics, and computing resources that today’s consumers are using at an increasing rate. With the advent of "smart" platforms (phones, tablets, and wearables) plus the emerging Internet of Things, the number of connected devices the average user or household contains is growing by several orders of magnitude.

In addition, users of the fixed and mobile broadband network are hungry for advanced broadband and intelligent cloud services. As this desire increases, users are turning towards over-the-top providers to consume the entertainment, productivity, and storage applications they want.

These realities have created an opportunity for consumer electronics vendors, application developers, and broadband and mobile network providers. These connected devices and services need to be managed, monitored, troubleshot, and controlled in an easy to develop and interoperable way. A unified framework for these is attractive if we want to enable providers, developers, and vendors to create value for the end user. The goal should be to create system for developing, deploying, and supporting these services for end users on the platform created by their connectivity and components, that is, to be able to treat the connected user herself as a platform for applications.

To address this opportunity, use cases supported by USP include:

* Management of IoT devices through re-usable data model objects.
* Allowing the user to interact with their devices and services using customer portals or control points on their own smart devices.
* The ability to have both the application and network service provider manage, troubleshoot, and control different aspects of the services they are responsible for, and enabling provider partnerships.
* Providing a consistent user experience from mobile to home.
* Simple migration from the [CPE WAN Management Protocol][2] (CWMP) - commonly known by its document number, "TR-069" - through use of the same data model and data modeling tools.

## Purpose and Scope

<a id="purpose_scope" />

### Purpose

This document provides the normative requirements and operational description of the User Services Platform (USP). USP is designed for consumer electronics/IoT, home network/gateways, smart WiFi systems, and virtual services (though could theoretically be used for any connected device in many different verticals). It is targeted towards developers, application providers, and network service providers looking to deploy those products.

### Scope

This document identifies the USP:

* Architecture
* Record structure, syntax, and rules
* Message structure, syntax, and rules
* Bindings that allow specific protocols to carry USP Records in their payloads
* Discovery and advertisement mechanisms
* Security credentials and logic
* Encryption mechanisms

Lastly, USP makes use of and expands the [Device:2 Data Model][1]. While particular Objects and parameters necessary to the function of USP are mentioned here, their normative description can be found in that XML document.

## References and Terminology

<a id="references_terminology" />

### Conventions

<a id="conventions" />

In this specification, several words are used to signify the requirements of the specification. These words are always capitalized. More information can be found be in [RFC 2119][Conventions].

**MUST**

This word, or the term "REQUIRED", means that the definition is an absolute requirement of the specification.

**MUST NOT**

This phrase means that the definition is an absolute prohibition of the specification.

**SHOULD**

This word, or the term "RECOMMENDED", means that there could exist valid reasons in particular circumstances to ignore this item, but the full implications need to be understood and carefully weighed before choosing a different course.

**SHOULD NOT**

This phrase, or the phrase "NOT RECOMMENDED" means that there could exist valid reasons in particular circumstances when the particular behavior is acceptable or even useful, but the full implications need to be understood and the case carefully weighed before implementing any behavior described with this label.

**MAY**

This word, or the term "OPTIONAL", means that this item is one of an allowed set of alternatives. An implementation that does not include this option MUST be prepared to inter-operate with another implementation that does include the option.

### References

<a id="references" />

The following references are of relevance to this Technical Report. At the time of publication, the editions indicated were valid. All references are subject to revision; users of this Technical Report are therefore encouraged to investigate the possibility of applying the most recent edition of the references listed below.

A list of currently valid Broadband Forum Technical Reports is published at
[www.broadband-forum.org](https://www.broadband-forum.org).

1. [Broadband Forum TR-181 Issue 2: *Device Data Model*][1]
2. [Broadband Forum TR-069 Amendment 6:	*CPE WAN Management Protocol*][2]
3. [Broadband Forum TR-106 Amendment 8: *Data Model Template for CWMP Endpoints and USP Agents*][3]
4. [IETF RFC 7228:	*Terminology for Constrained-Node Networks*][4]
5. [IETF RFC 2136:	*Dynamic Updates in the Domain Name System*][5]
6. [IETF RFC 3007:	*Secure Domain Name System Dynamic Update*][6]
7. [IETF RFC 6763:	*DNS-Based Service Discovery*][7]
8. [IETF RFC 6762:	*Multicast DNS*][8]
9. [IETF RFC 7252:	*The Constrained Application Protocol (CoAP)*][9]
10. [IETF RFC 7390:	*Group Communication for the Constrained Application Protocol (CoAP)*][10]
11.	[IETF RFC 4033:	*DNS Security Introduction and Requirements*][11]
12.	[*Protocol Buffers v3	Protocol Buffers Mechanism for Serializing Structured Data Version 3*][12]
13. [IEEE Registration Authority][13]
14. [IETF RFC 4122 A Universally Unique IDentifier (UUID) URN Namespace][14]
15. [IETF RFC 5290: *Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile*][15]
16. [IETF RFC 6818: *Updates to the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile*][16]
17. [IETF RFC 2234 Augmented BNF for Syntax Specifications: ABNF][17]
18. [IETF RFC 3986 Uniform Resource Identifier (URI): Generic Syntax][18]
19. [IETF RFC 2141 URN Syntax][19]
20. [IETF RFC 6455 The WebSocket Protocol][20]
21. [Simple Text Oriented Message Protocol][21]
22. [The Transport Layer Security (TLS) Protocol Version 1.2][22]
23. [Datagram Transport Layer Security Version 1.2][23]
24. [MQ Telemetry Transport 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)[24].

# Definitions

<a id="definitions" />

The following terminology is used throughout this specification.

**Agent**

An Agent is an Endpoint that exposes Service Elements to one or more Controllers.

**Binding**

A Binding is a means of sending Messages across an underlying Message Transfer Protocol.

**Command**

The term used to define and refer to an Object-specific Operation in the Agent’s Instantiated or Supported Data Model.

**Connection Capabilities**

Connection Capabilities are information related to an Endpoint that describe how to communicate with that Endpoint, and provide a very basic idea of what sort of function the Endpoint serves.

**User Services Platform**

The User Services Platform consists of a data model, architecture, and communications protocol to transform consumer broadband networks into a platform for the development, deployment, and support of broadband enabled applications and services.

**Controller**

A Controller is an Endpoint that manipulates Service Elements through one or more Agents.

**Device Type (DT) Definition**

A Device Type Definition (DT) is a description of the Service Elements an Agent is able to support, defining its Supported Data Model.  

**Discovery**

Discovery is the process by which Controllers become aware of Agents and Agents become aware of Controllers.

**Endpoint**

An Endpoint is a termination point for a Message.

**Endpoint Identifier**

The Endpoint Identifier is a globally unique USP layer identifier of an Endpoint.

**End to End Message Exchange**

USP feature that allows for message integrity protection through the creation of
a session context.

**Error**

An Error is a Message that contains failure information associated with a Request.

**Event**

An Event is a set of conditions that, when met, triggers the sending of a Notification.

**Expression**

See also Search Expression

**Expression Component**

An Expression Component is the part of a Search Expression that gives the matching Parameter criteria for the search. It is comprised of an Expression Parameter followed by an Expression Operator followed by an Expression Constant.

**Expression Constant**

The Expression Constant is the value used to compare against the Expression Component to determine if a search matches a given Object.

**Expression Operator**

The Expression Operator is the operator used to determine how the Expression Component will be evaluated against the Expression Constant, i.e., equals (==), not equals (!=), less than (<), greater than (>), less than or equal (<=), and greater than or equal (>=).

**Expression Parameter**

The Expression Parameter is a Parameter relative to the path where an Expression Variable occurs that will be used with the Expression Constant to evaluate the Expression Component.

**Expression Variable**

The Expression Variable is an identifier used to allow relative addressing when building an Expression Component.

**Instantiated Data Model**

The Instantiated Data Model of an Agent represents the current set of Service Elements (and their state) that are exposed to one or more Controllers.

**Instance Identifier**

A term used to identify to an Instance of a Multi-Instance Object (also called a Row of a Table). While all Multi-Instance Objects have an Instance Number that can be used as an Instance Identifier, an Object Instance can also be referenced using that Object’s Unique Key.

**Instance Number**

An Instance Number is a numeric Instance Identifier assigned by the Agent to instances of Multi-Instance Objects in an Agent’s Instantiated Data Model.

**Instance Path**

An Instance Path is a Path Name that addresses an Instance of a Multi-Instance Object (also called a Row of a Table). It includes the Object Path followed by an Instance Identifier.

**Message**

A Message refers to the contents of a USP layer communication including exactly one Message Header and at most one Message Body.

**Message Body**

The Message Body is the portion of a Message that contains one of the following: Request, Response, or Error.

**Message Header**

The portion of a Message that contains elements that provide information about the message, including the Endpoint Identifier of the sender and receiver, message type, and Message ID elements.

**Message ID**

A Message ID is an identifier used to associate a Response or Error with a Request.

**Message Transfer Protocol**

A Message Transfer Protocol (MTP) is the protocol at a layer below USP that carries a Message, i.e., CoAP.

**Multi-Instance Object**

A Multi-Instance Object refers to an Object that can be created or deleted in the Agent’s Instantiated Data Model. Also called a Table.

**Notification**

A Notification is a Request from an Agent that conveys information about an Event to a Controller that has a Subscription to that event.

**Object**

An Object refers to a defined type that an Agent represents and exposes. A Service Element may be comprised of one or more Objects and Sub-Objects.

**Object Instance**

An Object Instance refers to a single instance Object of a type defined by a Multi-Instance Object in the Agent’s Instantiated Data Model. Also called a Row of a Table.

**Object Path**

An Object Path is a Path Name that addresses an Object. In the case of Multi-Instance Objects, an Object Path addresses the Object type itself rather than instances of that Object, which are addressed by Instance Paths

**Operation**

A method defined for a particular Service Element that can be invoked with the Operate message.

**Parameter**

A Parameter is a variable or attribute of an Object. Parameters have both type and value.

**Parameter Path**

A Parameter Path is a Path Name that addresses a Parameter of an Object or Object Instance.

**Path Name**

A Path Name is a fully qualified reference to an Object, Object Instance, or Parameter in an Agent’s instantiated or Supported Data Model.

**Path Reference**

A Path Reference is a Parameter data type that contains a Path Name to an Object or Parameter that may be automatically followed by using certain Path Name syntax.

**Record**

The Record is defined as the Message Transfer Protocol (MTP) payload, encapsulating a sequence of datagrams that comprise the Message as well as providing additional metadata needed for providing integrity protection, payload protection and delivery of fragmented Messages.

**Relative Path**

A Relative Path is the remaining path information necessary to form a Path Name given a parent Object Path. It is used for message efficiency when addressing Path Names.

**Request**

A Request is a type of Message that either requests the Agent perform some action (create, update, delete, operate, etc.), requests information about an Agent or one or more Service Elements, or acts as a means to deliver Notifications from the Agent to the Controller. A Request usually requires a Response.

**Response**

A Response is a type of Message that provides return information about the successful processing of a Request.

**Row**

The term Row refers to an Instance of a Multi-Instance Object in the Agent’s Instantiated Data Model.

**Search Expression**

A Search Expression is used in a Search Path to apply specified search criteria to address a set of Multi-Instance Objects and/or their Parameters.

**Search Path**

A Search Path is a Path Name that contains search criteria for addressing a set of Multi-Instance Objects and/or their Parameters. A Search Path may contain a Search Expression or Wildcard.

**Service Element**

A Service Element represents a piece of service functionality that is exposed by an Agent, usually represented by one or more Objects.

**Source Endpoint**

An Endpoint that was the sender of a message.

**Subscription**

A Subscription is a set of logic that tells an Agent which Notifications to send to a particular Controller.

**Supported Data Model**

The Supported Data Model of an Agent represents the complete set of Service Elements it is capable of exposing to a Controller. It is defined by the union of all of the Device Type Definitions the Agent exposes to the Controller.

**Table**

The term Table refers to a Multi-Instance Object in an Agent’s Instantiated or Supported Data Model.

**Target Endpoint**

An Endpoint that was the intended receiver of a message.

**Trusted Broker**

An intermediary that either (1) ensures the Endpoint ID in all brokered Endpoint's USP Record `from_id` matches the Endpoint ID of those Endpoint's certificates or credentials, before sending on a USP Record to another Endpoint, or (2) is part of a closed ecosystem that "knows" (certain) Endpoints can be trusted not to spoof the Endpoint ID.

**Unique Key**

The Unique Key of a Multi-Instance Object is a set of Parameters that uniquely identify the instance of an Object in the Agent’s Instantiated Data Model and can be used as an Instance Identifier.

**Wildcard**

A Wildcard is used in a Search Path to address all Object Instances of a Multi-Instance Object.

## Abbreviations

This specification uses the following abbreviations:

| abbreviation | term |
| :----------- | :-------------- |
|ABNF | Augmented Backus-Naur Form |
|CoAP |	Constrained Application Protocol |
|USP	| User Services Platform |
|CWMP	| CPE WAN Management Protocol|
|DNS	| Domain Name Service |
|DNS-SD	| Domain Name Service - Service Definition |
|DT	| Device Type Definition |
|E2E | End to End (Message Exchange) |
|HMAC | Hash Message Authentication Code |
|HTTP	| Hypertext Transport Protocol |
|mDNS	| Multicast Domain Name Service |
|IPv4/v6 |	Internet Protocol (version 4 or version 6) |
|LAN	| Local Area Network |
|MAC | Message Authentication Code |
|MTP	| Message Transfer Protocol |
|OUI | Organizationally Unique Identifier |
|PSS | Probabilistic Signature Scheme |
|SAR | Segmentation And Reassembly |
|SMM | Software Module Management |
|TLS | Tranport Layer Security |
|TR	| Technical Report |
|URI | Uniform Resource Identifier |
|URL | Uniform Resource Locator |
|UUID | Universally Unique Identifier |
|WAN |	Wide Area Network|

# Specification Impact

## Energy efficiency

The User Services Platform reaches into more and newer connected devices, and expands on the management of physical hardware, including power management. In addition, USP directly enables smart home, smart building, and other smart energy applications.

## Security

Any solution that provides a mechanism to manage, monitor, diagnose, and control a connected user’s network, devices, and applications must prioritize security to protect user data and prevent malicious use of the system. This is especially important with certain high-risk smart applications like medicine or emergency services.

However reliable the security of communications protocols, in a platform that enables interoperable components that may or may not be connected with protocols outside the scope of the specification, security must be considered from end-to-end. To realize this, USP contains its own security mechanisms.

## Privacy

**Privacy** is the right of an individual or group to control or influence what information related to them may be collected, processed, and stored and by whom, and to whom that information may be disclosed.

**Assurance of privacy** depends on whether stakeholders expect, or are legally required, to have information protected or controlled from certain uses. As with security, the ability for users to control who has access to their data is of primary importance in the world of the connected user, made clear by users as well as regulators.

USP contains rigorous access control and authorization mechanisms to ensure that data is only used by those that have been enabled by the user.

[Architecture -->](/specification/architecture/)
