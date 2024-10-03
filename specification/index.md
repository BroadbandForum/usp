---
comment: |
 common.yaml contains common definitions shared by specification, resources
 and faq
...

!include cover-page.md

!include %notice%-notice.md

!include METADATA-%bbfMajor%.md

# Introduction {.new-page}

## Executive Summary

This document describes the architecture, protocol, and data model that build an intelligent User Services Platform. It is targeted towards application developers, application service providers, vendors, consumer electronics manufacturers, and broadband and mobile network providers who want to expand the value of the end user's network connection and their connected devices.

The term "connected device" is a broad one, applying to the vast array of network connected devices, consumer electronics, and computing resources that today's consumers are using at an increasing rate. With the advent of "smart" platforms (phones, tablets, and wearables) plus the emerging Internet of Things, the number of connected devices the average user or household contains is growing by several orders of magnitude.

In addition, users of the fixed and mobile broadband network are hungry for advanced broadband and intelligent cloud services. As this desire increases, users are turning towards over-the-top providers to consume the security, entertainment, productivity, and storage applications they want.

These realities have created an opportunity for consumer electronics vendors, application developers, and broadband and mobile network providers. These connected devices and services need to be managed, monitored, troubleshot, and controlled in an easy to develop and interoperable way. A unified framework for these is attractive if we want to enable providers, developers, and vendors to create value for the end user. The goal should be to create a system for developing, deploying, and supporting these services for end users on the platform created by their connectivity and components, that is, to be able to treat the connected user herself as a platform for applications.

To address this opportunity, use cases supported by USP include:

* Management of IoT devices through re-usable data model objects.
* Allowing the user to interact with their devices and services using customer
  portals or control points on their own smart devices.
* The ability to deploy and manage containerized microservices for end-users via software modulization and USP-enabled applications."
* The ability to have both the application and network service provider manage,
  troubleshoot, and control different aspects of the services they are
  responsible for, and enabling provider partnerships.
* Providing a consistent user experience from mobile to home.
* Simple migration from the CPE WAN Management Protocol [@TR-069] (CWMP) --
  commonly known by its document number, "TR-069" -- through use of the same
  data model and data modeling tools.

## Purpose and Scope

### Purpose

This document provides the normative requirements and operational description of the User Services Platform (USP). USP is designed for consumer electronics/IoT, home network/gateways, smart Wi-Fi systems, and deploying and managing other value-added services and applications. It is targeted towards developers, application providers, and network service providers looking to deploy those products.

### Scope

This document identifies the USP:

* Architecture
* Data model interaction
* Record structure, syntax, and rules
* Message structure, syntax, and rules
* Bindings that allow specific protocols to carry USP Records in their payloads
* Discovery and advertisement mechanisms
* Extensions for proxying, software module management, device modularization, firmware lifecycle management, bulk data collection, device-agent association, and an IoT theory of operations.
* Security credentials and logic
* Encryption mechanisms

Lastly, USP makes use of and expands the Device:2 Data Model [@TR-181]. While
particular Objects and Parameters necessary to the function of USP are
mentioned here, their normative description can be found in that document.

## References and Terminology

### Conventions

In this specification, several words are used to signify the requirements of
the specification. These words are always capitalized. More information can be
found in RFC 2119 [@RFC2119] for key words defined there. Additional key words
defined in the context of this specification are DEPRECATED and OBSOLETED.

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

**DEPRECATED**

This word refers to a requirement or section of this specification that is defined and valid in the current version of this specification but is not strictly necessary. This may be done for various reasons, such as irreparable problems being discovered or another more useful method being defined to accomplish the same purpose. When this word is applied to a requirement, it takes precedence over any normative language in the DEPRECATED requirement. DEPRECATED requirements SHOULD NOT be implemented. When this word is used on a section, it means the entirety of the section SHOULD NOT be implemented -- but if it is implemented the requirements in the section are to be implemented as written. Note that DEPRECATED requirements and sections might be removed from the next major version of this specification.

**OBSOLETED**

This word refers to a requirement or section of this specification that meets the definition of DEPRECATED, but which has also been declared obsolete. Such requirements or entire sections MUST NOT be implemented; they might be removed from a later minor version of this specification.


### References

The following references are of relevance to this %bbfType%. At the time of publication, the editions indicated were valid. All references are subject to revision; users of this %bbfType% are therefore encouraged to investigate the possibility of applying the most recent edition of the references listed below.

A list of currently valid Broadband Forum %bbfType%s is published at
[www.broadband-forum.org](https://www.broadband-forum.org).

::: {#refs}
:::

## Definitions

The following terminology is used throughout this specification.

**Agent**

An Agent is an Endpoint that exposes Service Elements to one or more Controllers.

**Binding**

A Binding is a means of sending Messages across an underlying Message Transfer Protocol.

**Command**

The term used to define and refer to an Object-specific Operation in the Agent's Instantiated or Supported Data Model.

**Command Path**

A Command Path is a Path Name that addresses a Command of an Object or Object Instance. See [](#sec:path-names).

**Connection Capabilities**

Connection Capabilities are information related to an Endpoint that describe how to communicate with that Endpoint, and provide a very basic idea of what sort of function the Endpoint serves.

**Controller**

A Controller is an Endpoint that manipulates Service Elements through one or more Agents.

**Discovery**

Discovery is the process by which Controllers become aware of Agents and Agents become aware of Controllers.

**Endpoint**

An Endpoint is a termination point for a Message.

**Endpoint Identifier**

The Endpoint Identifier is a globally unique USP layer identifier of an Endpoint.

**End to End Message Exchange**

USP feature that allows for message integrity protection through the creation
of a session context.

**Error**

An Error is a Message that contains failure information associated with a Request.

**Event**

An Event is a set of conditions that, when met, triggers the sending of a Notification.

**Event Path**

An Event Path is a Path Name that addresses an Event of an Object or Object Instance. See [](#sec:path-names).

**Expression**

See also Search Expression.

**Expression Component**

An Expression Component is the part of a Search Expression that gives the matching Parameter criteria for the search. It is comprised of an Expression Parameter followed by an Expression Operator followed by an Expression Constant.

**Expression Constant**

The Expression Constant is the value used to compare against the Expression Component to determine if a search matches a given Object.

**Expression Operator**

The Expression Operator is the operator used to determine how the Expression Component will be evaluated against the Expression Constant, i.e., equals (==), not equals (!=), contains (~=), less than (<), greater than (>), less than or equal (<=) and greater than or equal (>=).

**Expression Parameter**

The Expression Parameter is a Parameter relative to the Path Name where an Expression Variable occurs that will be used with the Expression Constant to evaluate the Expression Component.

**Expression Variable**

The Expression Variable is an identifier used to allow relative addressing when building an Expression Component.

**Instantiated Data Model**

The Instantiated Data Model of an Agent represents the current set of Service Elements (and their state) that are exposed to one or more Controllers.

**Instance Identifier**

A term used to identify an Instance of a Multi-Instance Object (also called a Row of a Table). While all Multi-Instance Objects have an Instance Number that can be used as an Instance Identifier, an Object Instance can also be referenced using any of that Object's Unique Keys.

**Instance Number**

An Instance Number is a numeric Instance Identifier assigned by the Agent to instances of Multi-Instance Objects in an Agent's Instantiated Data Model.

**Message**

A Message refers to the contents of a USP layer communication including exactly one Message Header and exactly one Message Body.

**Message Body**

The Message Body is the portion of a Message that contains one of the following: Request, Response, or Error.

**Message Header**

The portion of a Message that contains elements that provide information about the Message, including the Message type, and Message ID elements.

**Message ID**

A Message ID is an identifier used to associate a Response or Error with a Request.

**Message Transfer Protocol**

A Message Transfer Protocol (MTP) is the protocol at a layer below USP that carries a Message, e.g., WebSocket.

**Multi-Instance Object**

A Multi-Instance Object refers to an Object that can be created or deleted in the Agent's Instantiated Data Model. Also called a Table.

**Notification**

A Notification is a Request from an Agent that conveys information about an Event to a Controller that has a Subscription to that event.

**Object**

An Object refers to a defined type that an Agent represents and exposes. A Service Element may be comprised of one or more Objects and Sub-Objects.

**Object Instance**

An Object Instance refers to a single instance Object of a type defined by a Multi-Instance Object in the Agent's Instantiated Data Model. Also called a Row of a Table.

**Object Instance Path**

An Object Instance Path is a Path Name that addresses an Instance of a Multi-Instance Object (also called a Row of a Table). It includes the Object Path followed by an Instance Identifier. See [](#sec:path-names).

**Object Path**

An Object Path is a Path Name that addresses an Object. In the case of Multi-Instance Objects, an Object Path addresses the Object type itself rather than instances of that Object, which are addressed by Object Instance Paths. See [](#sec:path-names).

**Operation**

A method defined for a particular Service Element that can be invoked with the Operate Message.

**Parameter**

A Parameter is a variable or attribute of an Object. Parameters have both type and value.

**Parameter Path**

A Parameter Path is a Path Name that addresses a Parameter of an Object or Object Instance. See [](#sec:path-names).

**Path Name**

A Path Name is a fully qualified reference to an Object, Object Instance, Command, Event, or Parameter in an Agent's Instantiated or Supported Data Model. See [](#sec:path-names).

**Path Reference**

A Path Reference is a Parameter data type that contains a Path Name to an Object or Parameter that may be automatically followed by using certain Path Name syntax.

**Record**

The Record is defined as the Message Transfer Protocol (MTP) payload, encapsulating a sequence of datagrams that comprise of the Message as well as essential protocol information such as the USP version, the source Endpoint ID, and the target Endpoint ID. It can also contain additional metadata needed for providing integrity protection, payload protection and delivery of fragmented Messages.

**Register**

To Register means to use the Register message to inform a Controller of Service Elements that this Agent represents.

**Registered**

Registered Service Elements are those elements represented by an Agent that have been the subject of a Register message.

**Relative Path**

A Relative Path is the remaining Path Name information necessary to form a Path Name given a parent Object Path. It is used for message efficiency when addressing Path Names.

**Request**

A Request is a type of Message that either requests the Agent perform some action (create, update, delete, operate, etc.), requests information about an Agent or one or more Service Elements, or acts as a means to deliver Notifications and Register Messages from the Agent to the Controller. A Request usually requires a Response.

**Response**

A Response is a type of Message that provides return information about the successful processing of a Request.

**Role**

A Role refers to the set of permissions (i.e., an access control list) that a Controller is granted by an Agent to interact with objects in its Instantiated Data Model.

**Row**

The term Row refers to an Instance of a Multi-Instance Object in the Agent's Instantiated Data Model.

**Search Expression**

A Search Expression is used in a Search Path to apply specified search criteria to address a set of Multi-Instance Objects and/or their Parameters.

**Search Path**

A Search Path is a Path Name that contains search criteria for addressing a set of Multi-Instance Objects and/or their Parameters. A Search Path may contain a Search Expression or Wildcard.

**Service Element**

A Service Element represents a piece of service functionality that is exposed by an Agent, usually represented by one or more Objects.

**Source Endpoint**

The Endpoint that was the sender of a message.

**Subscription**

A Subscription is a set of logic that tells an Agent which Notifications to send to a particular Controller.

**Supported Data Model**

The Supported Data Model of an Agent represents the complete set of Service Elements it is capable of exposing to a Controller. It is defined by the union of all of the Device Type Definitions the Agent exposes to the Controller.

**Table**

The term Table refers to a Multi-Instance Object in an Agent's Instantiated or Supported Data Model.

**Target Endpoint**

The Endpoint that was the intended receiver of a message.

**Trusted Broker**

An intermediary that either (1) ensures the Endpoint ID in all brokered Endpoint's USP Record `from_id` matches the Endpoint ID of those Endpoint's certificates or credentials, before sending on a USP Record to another Endpoint, or (2) is part of a closed ecosystem that "knows" (certain) Endpoints can be trusted not to spoof the Endpoint ID.

**Unique Key**

A Unique Key of a Multi-Instance Object is a set of one or more Parameters that uniquely identify the instance of an Object in the Agent's Instantiated Data Model and can therefore be used as an Instance Identifier.

**Unique Key Parameter**

A Parameter that is a member of any of a Multi-Instance Object's Unique Keys.

**User Services Platform**

The User Services Platform consists of a data model, architecture, and communications protocol to transform consumer broadband networks into a platform for the development, deployment, and support of broadband enabled applications and services.

**USP Domain**

The USP Domain is a set of all Controllers and Agents that are likely to communicate with each other in a given network or internetwork with the goal of supporting a specific application or set of applications.

**USP Relationship**

A Controller and Agent are considered to have a USP Relationship when they are capable of sending and accepting messages to/from each other. This usually means the Controller is added to the Agent's Controller table in its Instantiated Data Model.

**Wildcard**

A Wildcard is used in a Search Path to address all Object Instances of a Multi-Instance Object.

## Abbreviations

This specification uses the following abbreviations:

| abbreviation | term |
| :----------- | :-------------- |
|ABNF | Augmented Backus-Naur Form |
|CID  | Company Identifier |
|CSV | Comma-Separated Values |
|CWMP	| CPE WAN Management Protocol|
|DNS	| Domain Name Service |
|DNS-SD	| Domain Name Service - Service Discovery |
|DU | Deployment Unit |
|E2E | End to End (Message Exchange) |
|EE | Execution Environment |
|EU | Execution Unit |
|FIFO | First-In-First-Out |
|FQDN | Fully-Qualified Domain Name |
|GSDM | Get Supported Data Model (informal of GetSupportedDM message) |
|HMAC | Hash Message Authentication Code |
|HTTP	| Hypertext Transport Protocol |
|IPv4/v6 |	Internet Protocol (version 4 or version 6) |
|JSON | Java Script Object Notation |
|LAN	| Local Area Network |
|MAC | Message Authentication Code |
|mDNS	| Multicast Domain Name Service |
|MTP	| Message Transfer Protocol |
|MQTT | Message Queue Telemetry Transport |
|OUI | Organizationally Unique Identifier |
|PEN | Private Enterprise Number |
|Protobuf | Protocol Buffers |
|PSS | Probabilistic Signature Scheme |
|SAR | Segmentation And Reassembly |
|SMM | Software Module Management |
|SOAP| Simple Object Access Protocol |
|SSID | Service Set Identifier |
|STOMP | Simple Text-Oriented Messaging Protocol |
|TLS | Tranport Layer Security |
|TLV | Type-Length-Value |
|TOFU	| Trust on First Use |
|TR	| Technical Report |
|UDS | UNIX Domain Socket |
|URI | Uniform Resource Identifier |
|URL | Uniform Resource Locator |
|USP	| User Services Platform |
|UUID | Universally Unique Identifier |
|WAN |	Wide Area Network|
|XML | eXtensible Markup Language |

## Specification Impact

### Energy efficiency

The User Services Platform reaches into more and newer connected devices, and expands on the management of physical hardware, including power management. In addition, USP directly enables smart home, smart building, and other smart energy applications.

### Security

Any solution that provides a mechanism to manage, monitor, diagnose, and control a connected user's network, devices, and applications must prioritize security to protect user data and prevent malicious use of the system. This is especially important with certain high-risk smart applications like medicine or emergency services.

However reliable the security of communications protocols, in a platform that enables interoperable components that may or may not be connected with protocols outside the scope of the specification, security must be considered from end-to-end. To realize this, USP contains its own security mechanisms.

### Privacy

**Privacy** is the right of an individual or group to control or influence what information related to them may be collected, processed, and stored and by whom, and to whom that information may be disclosed.

**Assurance of privacy** depends on whether stakeholders expect, or are legally required, to have information protected or controlled from certain uses. As with security, the ability for users to control who has access to their data is of primary importance in the world of the connected user, made clear by users as well as regulators.

USP contains rigorous access control and authorization mechanisms to ensure that data is only used by those that have been enabled by the user.
