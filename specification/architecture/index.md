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


# Architecture

<a id="architecture" />

The User Services Platform consists of a collection of Endpoints (Agents and Controllers) that allow applications to manipulate Service Elements. These Service Elements are made up of a set of Objects and parameters that model a given service, such as network interfaces, software modules, device firmware, remote elements proxied through another interface, virtual elements, or other managed services.

USP is made up of several architectural components:

* Mechanisms for discovery and trust establishment
* A method for encoding messages for transport
* A system for end-to-end confidentiality, integrity and identity authentication
* Transport of messages over one or more Message Transfer Protocols (MTPs) with associated MTP security
* A set of standardized messages based on the CRUD model (create, read, update, delete), plus an object defined operations mechanism and an notification mechanism (CRUD-ON)
* Authorization and access control on a per element basis
* A method for modeling service elements using a set of objects, parameters, operations, and events (supported and instantiated data models)

## Endpoints  

<a id="endpoints" />

A USP endpoint can act as Agent or a Controller. Controllers only send messages to Agents, and Agents send messages to Controllers. A USP Endpoint communicates over a secure session between other endpoints, over one or more Message Transfer Protocols (MTP) that may or may not be secured.

<img src="usp_architecture.png">

Figure ARC.1 - USP Agent and Controller Architecture

### Agents

<a id="Agents" />

A USP Agent exposes (to Controllers) one or more Service Elements that are represented in its data model. It contains or references both an Instantiated Data Model (representing the current state of Service Elements it represents) and a Supported Data Model.

### Controllers

<a id="controllers" />

A USP Controller manipulates (through Agents) a set of Service Elements that are represented in Agent data models. It may maintain a database of Agents, their capabilities, and their states, in any combination. A Controller usually acts as an interface to a user application or policy engine that uses the User Services Platform to address particular use cases.

### Endpoint Identifier

<a id="endpoint-id" />

Endpoints are identified by an Endpoint Identifier.

The Endpoint Identifier is a locally or globally unique USP layer identifier of an Endpoint. Whether it is globally or locally unique depends on the scheme used for assignment.

The Endpoint Identifier (ID) is used in the USP Record and various Parameters in a USP Message to uniquely identify Controller and Agent Endpoints. It can be globally or locally unique, either among all Endpoints or among all Controllers or all Agents, depending on the scheme used for assignment.

The Endpoint ID is comprised of two mandatory and one optionally mandatory components: `authority-scheme`, `authority-id`, and `instance-id`.

These three components are combined as:

`authority-scheme ":"  [authority-id]  ":" instance-id`

The format of the authority-id is dictated by the authority-scheme. The format of the instance-id is dictated either by the authority-scheme or by the entity identified by the authority-id.

An Endpoint ID can be expressed as a urn in the bbf namespace as

`"urn:bbf:usp:id:" authority-scheme ":" [authority-id] ":" instance-id`

#### authority-scheme and authority-id

The authority-scheme follows the following syntax:

`authority-scheme = "oui" | "cid" | "pen" | "self"  | "user" | "os" | "ops" | "uuid" | "imei" | "proto" | "doc"`

How these authority-scheme values impact the format and values of authority-id and instance-id is described below.

The authority defined by an OUI, CID, or Private Enterprise Number (including OUI used in "ops" and "os" authority scheme) is responsible for ensuring the uniqueness of the resulting Endpoint ID. Uniqueness can be global, local, unique across all Endpoints, or unique among all Controllers or all Agents. For the "user" authority scheme, the assigning user or machine is responsible for ensuring uniqueness. For the "self" authority scheme, the Endpoint is responsible for ensuring uniqueness.

**R-ARC.0** - A Controller and Agent within the same ecosystem MAY use the same Endpoint ID.

**R-ARC.1** - Endpoints MUST tolerate the same Endpoint ID being used by an Agent and a Controller in the same ecosystem.

**R-ARC.2** - Endpoints that share the same Endpoint ID MUST NOT communicate with each other via USP.

No conflict identification or resolution process is defined in USP to deal with a situation where an Endpoint ID is not unique among either all Agents or all Controllers in whatever ecosystem it operates. Therefore, a non-unique Endpoint ID will result in unpredictable behavior. An Endpoint ID that changes after having been used to identify an Endpoint can also result in unpredictable behavior.

Unless the authority responsible for assigning an Endpoint ID assigns meaning to an Agent and Controller having the same Endpoint ID, no meaning can be construed. That is, unless the assigning authority specifically states that an Agent and Controller with the same Endpoint ID are somehow related, no relationship can be assumed to exist.

| authority-scheme | usage and rules for authority-id and instance-id |
| ---------------: | :----------------------------------------------- |
|`oui` | `authority-id` MUST be an OUI assigned and registered by the [IEEE Registration Authority](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries) to the entity responsible for this Endpoint. authority-id MUST use hex encoding of the 24-bit ID (resulting in 6 hex characters). `instance-id` syntax is defined by this entity, who is also responsible for determining instance-id assignment mechanisms and for ensuring uniqueness of the instance-id within the context of the OUI. Example:` oui:00256D:my-unique-bbf-id-42`|
| `cid` | `authority-id` MUST be a CID assigned and registered by the [IEEE Registration Authority](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries) to the entity responsible for this Endpoint. `authority-id` MUST use hex encoding of the 24-bit ID (resulting in 6 hex characters).<br><br>`instance-id` syntax is defined by this entity, who is also responsible for determining instance-id assignment mechanisms and for ensuring uniqueness of the instance-id within the context of the CID.<br><br>Example: cid:3AA3F8:my-unique-usp-id-42 |
| `pen` | `authority-id` MUST be a Private Enterprise Number assigned and registered by the [IANA](http://pen.iana.org/pen/PenApplication.page) to the entity responsible for this Endpoint. `authority-id` MUST use decimal encoding of the IANA-assigned number.<br><br>`instance-id` syntax is defined by this entity, who is also responsible for determining instance-id assignment mechanisms and for ensuring uniqueness of the instance-id within the context of the Private Enterprise Number.<br><br>Example: `pen:3561:my-unique-bbf-id-42`|
| `self` | An `authority-id` for "`self`" MUST be between 0 and 6 non-reserved characters in length. When authority-id is 1 or more characters, it is generated by the Endpoint.<br><br>The Endpoint ID, including `instance-id`, is generated by the Endpoint.<br><br>The Endpoint MUST change its Endpoint ID if it ever encounters another Endpoint using the identical Endpoint ID.<br><br>Example: `self::my-Agent` |
| `user` | An `authority-id` for "`user`" MUST be between 0 and 6 non-reserved characters in length.<br><br>The Endpoint ID, including `instance-id`, is assigned to the Endpoint via a user or management interface. |
| `os` | `authority-id` MUST be zero-length.<br><br>`instance-id `is `<OUI> "-"<SerialNumber>`, as defined in TR-069[2], Section 3.4.4. Example: `os::00256D-0123456789` |
| `ops` | `authority-id` MUST be zero-length.<br><br>`instance-id` is `<OUI> "-" <ProductClass> "-" <SerialNumber>`, as defined in [TR-069][2], Section 3.4.4.<br><br>Example: `ops::00256D-STB-0123456789` |
| `uuid` | `authority-id` MUST be zero-length.<br><br>`instance-id` is a [UUID](https://tools.ietf.org/html/rfc4122)<br><br>Example:`uuid::f81d4fae-7dec-11d0-a765-00a0c91e6bf6`
| `imei` | `authority-id` MUST be zero-length.<br><br>`instance-id` is an IMEI as defined by GSMA(https://imeidb.gsma.com/imei/index).<br><br>Example: `imei::990000862471854` |
| `proto` | `authority-id` MUST be between 0 and 6 non-reserved characters (except ".") in length.<br><br>"`proto`" is used for prototyping purposes only. Any `authority-id` and `instance-id` value (or scheme for creating the value) is left to the prototyper.<br><br>Example: `proto::my-Agent` |
| `doc` | `authority-id` MUST be between 0 and 6 non-reserved characters in length.<br><br>"`doc`" is used for documentation purposes only (for creating examples in slide decks, tutorials, and other explanatory documents). Any `authority-id` and `instance-id` value (or scheme for creating the value) is left to the document creator. |

**R-ARC.3** - BBF OUI (`00256D`) and Private Enterprise Number (`3561`) are reserved for use in BBF documentation and BBF prototyping and MUST NOT be used by any entity other than BBF.

**R-ARC.4** - The "`proto`" and "`doc`" authority-scheme values MUST NOT be used in production environments.

The "`proto`" and "`doc`" values are intended only for prototyping and documentation (tutorials, examples, etc.), respectively.

#### instance-id

**R-ARC.5** - `instance-id` MUST be encoded using only the following characters:
```
    instance-id = unreserved / pct-encoded
    unreserved = ALPHA / DIGIT / "-" / "." / "_"
    pct-encoded = "%" HEXDIG HEXDIG
```
The above expression uses the Augmented Backus-Naur Form (ABNF) notation of [RFC2234](https://tools.ietf.org/html/rfc2234), including the following core ABNF syntax rules defined by that specification: ALPHA (letters), DIGIT (decimal digits), HEXDIG (hexadecimal). It is taken from [RFC3986](https://tools.ietf.org/html/rfc3986) as the set of unreserved characters and percent-encoded characters that are acceptable for all components of a URI. This set is also allowed for use in URNs [RFC2141](https://tools.ietf.org/html/rfc2141), and all MTP headers.

**R-ARC.6** - An instance-id value MUST be no more than 50 characters in length.

Shorter values are preferred, as end users could be exposed to Endpoint IDs. Long values tend to create a poor user experience when users are exposed to them.

## Service Elements
<a id="service_elements" />

"Service Element" is a general term referring to the set of Objects, sub-Objects, commands, events, and parameters that comprise a set of functionality that is manipulated by a Controller on an Agent. An Agent’s Service Elements are represented in a Data Model - the data model representing an Agent’s current state is referred to as its Instantiated Data Model, and the data model representing the Service Elements it supports is called its Supported Data Model. The Supported Data Model is described in a Device Type Definition (DT). An Agent’s Data Model is referenced using Path Names.

### Data Models
<a id="data_models" />

USP is designed to allow a Controller to manipulate Service Elements on an Agent using a standardized description of those Service Elements. This standardized description is known as an information model, and an information model that is further specified for use in a particular protocol is known as a "Data Model".

*Note: This should be understood by those familiar with CWMP. For those unfamiliar with that protocol, a Data Model is similar to a Management Information Base (MIB) used in the Simple Network Management Protocol (SNMP) or YANG definitions used in NETCONF.*

This version of the specification defines support for the following Data Model(s):

* The [Device:2 Data Model][1]

This Data Model is specified in XML. The schema and normative requirements for defining Objects, Parameters, Events, and Commands for the Device:2 Data Model for [CWMP][1], and for creating Device Type Definitions based on that Data Model, are defined in [Broadband Forum TR-106, "Data Model Template for TR-069 Enabled Devices"][3].

The use of USP with any of the above data models creates some dependencies on specific Objects and Parameters that must be included for base functionality.

#### Instantiated Data Model
<a id="instantiated_data_model" />

An Agent’s Instantiated Data Model represents the Service Elements (and their state) that are currently represented by the Agent. The Instantiated Data Model includes a set of Objects, and the sub-Objects ("children"), Parameters, Events, and Commands associated with those objects.

#### Supported Data Model
<a id="supported_data_model" />

An Agent’s Support Data Model represents the Service Elements that an Agent understands. It includes references to the Data Model(s) that define the Objects, Parameters, Events, and Commands implemented by the Service Elements the Agent represents. A Supported Data Model consists of the union of all Device Type Definitions used by the Agent.

#### Objects
<a id="objects" />

Objects are data structures that are defined by their sub-Objects, Parameters, Events, Commands, and creation criteria. They are used to model resources represented by the Agent. Objects may be static (single-instance) or dynamic (a multi-instance Object, or "table").

##### Single-Instance Objects
<a id="single-instance_objects" />

Static Objects, or "single instance" Objects, are not tables and do not have more than one instance of them in the Agent. They are usually used to group Service Element functionality together to allow for easy definition and addressing.

##### Multi-Instance Objects
<a id="multi-instance_objects" />

Dynamic Objects, or "multi-instance" Objects, are those Objects that can be the subject of "create" and "delete" operations (using the Add and Delete messages, respectively), with each instance of the Object represented in the Instantiated Data Model with an Instance Identifier (see below). A Multi-Instance Object is also referred to as a "Table", with each instance of the Object referred to as a "Row". Multi-Instance Objects can be also the subject of a search.

#### Parameters
<a id="parameters" />

Parameters define the attributes or variables of an Object. They are retrieved by a Controller using the read operations of USP and configured using the update operations of USP (the Get and Set messages, respectively). Parameters have data types and are used to store values.

#### Commands
<a id="commands" />

Commands define Object specific methods within the Data Model. A Controller can invoke these methods using the "Operate" message in USP (i.e., the Operate message). Commands have associated input and output arguments that are defined in the Data Model and used when the method is invoked and returned.

#### Events
<a id="events" />

Events define Object specific notifications within the Data Model. A Controller can subscribe to these events by creating instances of the Subscription table, which are then sent in a [Notify Request by the Agent](/specification/messages/notify/). Events may also have information associated with them that are delivered in the Notify Request - this information is defined with the Event in the Data Model.

#### Path Names
<a id="path_names" />

A Path Name is a fully qualified reference to an Object, Object Instance, or Parameter in an Agent’s instantiated or Supported Data Model. The syntax for Path Names is defined in [TR-106][3].

**R-ARC.7** - All USP endpoints MUST support the Path Name syntax as defined in [TR-106][3].

Path Names are represented by a hierarchy of Objects ("parents") and sub-Objects ("children"), separated by the dot "." character, ending with a parameter if referencing a parameter path. There are six different types of Path Names used to address the data model of an Agent:

1.	Object Path - This is a Path Name of either a single-instance ("static") Object, or the Path Name to a Data Model Table (i.e., a Multi-Instance Object). An Object Path ends in a "." Character (as specified in [TR-106][3]), except when used in a [reference parameter](#reference_following). When addressing a Table in the Agent’s Supported Data Model that contains one or more Multi-Instance Objects in the Path Name, the sequence "{i}" is used as a placeholder (see the [GetSupportedDM message](/specification/messages/getsupporteddm/)).

2.	Object Instance Path - This is a Path Name to a Row in a Table in the Agent’s Instantiated Data Model (i.e., an Instance of a Multi-Instance Object). It uses an Instance Identifier to address a particular Instance of the Object.  An Object Instance Path ends in a "." Character (as specified in [TR-106][3]), except when used in a [reference parameter](#reference_following).

3.	Parameter Path - This is a Path Name of a particular Parameter of an Object.

4.	Command Path - This is a Path Name of an Object defined [Operation](#operation_command_path_names).

5.	Event Path - This is a Path Name of an Object defined [Event](#event_path_names).

6.	Search Path - This is a Path Name that contains search criteria for addressing a set of Multi-Instance Objects and/or their Parameters. A Search Path may contain a Search Expression or Wildcard.

This creates two functions of Path Names: Addressing and Searching. The first five paths are used for addressing a particular Object, Parameter, Command, or Event. A Search Path uses Searching to return a set of Object Instances and/or their Parameters. When addressing, the expectation is that the Path Name will resolve to either 0 or 1 instance (and depending on the context, 0 instances could be an error).  When searching, the expectation is that the Search Path will resolve to 0, 1, or many instances (and depending on the context, 0 instances is often not an error).

*NOTE: When resolving a Path Name, the Agent is expected to use locally cached information and/or information that can be obtained rapidly and cheaply. Specifically, there is no expectation that the Agent would issue a network request in order to resolve a Path Name.*

*NOTE: Obviously only one form of addressing or searching can be used for a given Instance Identifier in a Path Name, but different forms of addressing can be used if more than one Instance Identifier needs to be specified in a Path Name.*

For example, the following Path Name uses Unique Key Addressing for the Interface table but a Search Expression for the IPv4Address table to select Enabled IPv4 Addresses associated with the "eth0" IP Interface:

`Device.IP.Interface.[Name=="eth0"].IPv4Address.{Status=="Enabled"}.IPAddres`

#### Relative Paths

<a id="relative_paths" />

Several USP messages make use of relative paths to address Objects or Parameters. A relative path is used to address the child Objects and parameters of a given Object Path or Object Instance Path. To build a Path Name using a Relative Path, a USP endpoint uses a specified Object Path or Object Instance Path, and concatenates the Relative Path. This allows some efficiency in Requests and Responses when passing large numbers of repetitive Path Names. This relative path may include [instance identifiers](#using_instance_identifiers_in_path_names) to Multi-Instance Objects.

For example, for an Object Path of:

`Device.Wifi.Radio.1.`

Relative paths would include parameters:

`Status`

`SupportedStandards`

`OperatingStandards`

Etc., as well as the following sub-Object and its parameters:

`Stats.BytesSent`

`Stats.BytesReceived`

Etc.

#### Using Instance Identifiers in Path Names
<a id="using_instance_identifiers_in_path_names" />

##### Addressing by Instance Number
<a id="addressing_by_instance_number" />

Instance Number Addressing allows an Object Instance to be addressed by using its Instance Number in the Path Name. An Instance Number is expressed in the Path Name as a positive integer (>=1) with no additional surrounding characters. The Instance Number assigned by the Agent is arbitrary.

**R-ARC.8** - The assigned Instance Number MUST persist unchanged until the Object Instance is subsequently deleted (either by the USP Delete message or through some external mechanism). This implies that the Instance Number MUST persist across a reboot of the Agent, and that the Agent MUST NOT allow the Instance Number of an existing Object Instance to be modified by an external source.

For example, the `Device.IP.Interface` table entry with an Instance Number of 3 would be addressed with the following Path Name: `Device.IP.Interface.3`.

##### Addressing by Unique Key

<a id="addressing_by_unique_key" />

Key-based addressing allows an Object Instance to be addressed by using a Unique Key (as defined in [Device:2][1]) in the Path Name. This is possible since once a Parameter that is part of a unique key has its value set, then that value is immutable for the life of the Object that contains the Parameter.

For example, the `Device.IP.Interface` table has 2 separate unique keys; `Name` and `Alias`.

Unique Keys used for addressing are expressed in the Path Name by using square brackets surrounding a string that contains the name and value of the Unique Key parameter using the equivalence operator (==).

If an Object has a compound unique key (multiple parameters included within the same unique key), then all keys must be present in the Instance Identifier and separated by a comma (,) character (the order of the parameters does not have to follow the order of the parameters as defined in the unique key element as defined in [Device:2][1]).

For example, the `Device.NAT.PortMapping` table has a compound unique key consisting of RemoteHost, ExternalPort, and Protocol, which would be addressed with the following Path Name:  

`Device.NAT.PortMapping.[RemoteHost=="",ExternalPort==0,Protocol=="TCP"].`

##### Searching with Expressions

<a id="search" />

Searching is a means of matching 0, 1 or many instances of a Multi-Instance Object by using the properties of Object.   Search Paths use an Expression Variable enclosed in curly braces as the Instance Identifier within a Path Name and then appends a "::" to the end of the Path Name, followed by an Expression enclosed in another set of curly braces.

**R-ARC.9** - An Agent MUST return Path Names that include all Object Instances that match the criteria of a given Search Path.

**R-ARC.10** - An Expression Variable MUST be a valid identifier, which means that it MUST follow the same syntax as used for naming Parameters as defined in [TR-106][3].

The basic format of a Search Path is:

`Device.IP.Interface.{expression>}.Status`

An Expression consists of one or more Expression Components that are concatenated by the AND (&&) logical operator (NOTE: the OR logical operator is not supported).  

The basic format of a Search Path with the Expression element expanded is:

`Device.IP.Interface.{<expression component>&&<expression component>}.Status`

An Expression Component is a combination of an Expression Parameter followed by an Expression Operator followed by an Expression Constant.

The basic format of a Search Path with the Expression Component element expanded is:

`Device.IP.Interface.{<expression parameter><expression operator><expression constant>}.Status`

For example, `Device.IP.Interface.{intf}.IPv4Address.{addr}.IPAddress` means that "`intf`" inside the Expression Parameter represents the instances of the `Device.IP.Interface.{i}` Object whereas "`addr`" inside the Expression Parameter represents the instances of the `Device.IP.Interface.{i}.IPv4Address.{i}` Object.

Further, this relative path can’t include any child tables. *(NOTE: this is never necessary because any child tables that need to be referenced in the Expression can and should have their own Expression Variables)*

An Expression Operator dictates how the Expression Component will be evaluated. The supported operators include: equals (==), not equals (!=), less than (<), greater than (>), less than or equal (<=), and greater than or equal (>=).

An Expression Parameter will always be of the type defined in the data model. Expression operators will only evaluate for appropriate data types. The literal value representations for all data types are found in [TR-106][3]. **For string, boolean and enumeration types, only the '==' and '!=' operators are valid.**

The Expression Constant is the value that the Expression Parameter is being evaluated against; Expression Parameters must match the type as defined for the associated Parameter in [TR-181][1].

*NOTE: String values are enclosed in double quotes. In order to allow a string value to contain double quotes, quote characters can be percent-escaped as %22 (double quote). Therefore, a literal percent character has to be quoted as %25.*



##### Search Examples

<a id="search_examples" />

*Valid Searches:*

- Status for all IP Interfaces with a "Normal" type:

  `Device.IP.Interface.{Type=="Normal"}.Status`

- Ipv4 Addresses for all IP Interfaces with a Normal type and a Static addressing type:

  `Device.IP.Interface.{Type=="Normal"}.IPv4Address.{AddressingType=="Static"}.IPAddress`

- Ipv4 Addresses for all IP Interfaces with a Normal type and Static addressing type that have at least 1 Error Sent

  `Device.IP.Interface.{Type=="Normal"&&intf.Stats.ErrorsSent>0}.Ipv4Address.{AddressingType=="Static"}.IPAddress`

*Searches that are NOT VALID:*

- Invalid because the Expression is empty:

  `Device.IP.Interface.{}.`

- Invalid because the Expression Component has an Expression Parameter that descends into a child table (always need to use a separate Expression Variable for each child table instance):

  `Device.IP.Interface.{Type=="Normal"&&IPv4Address.*.AddressingType=="Static"}.Status`

#### Searching by Wildcard

<a id="searching_by_wildcard" />

Wildcard-based searching is a means of matching all currently existing Instances (whether that be 0, 1 or many instances) of a Multi-Instance Object by using a wildcard character "\*" in place of the Instance Identifier.

**R-ARC.11** - An Agent MUST return Path Names that include all Object Instances that are matched by the use of a Wildcard.

Examples:

All parameters for all IP Interfaces that currently exist

`Device.IP.Interface.*.`

Type of each IP Interface that currently exists

`Device.IP.Interface.*.Type`

#### Other Path Decorators
<a id="other_path_decorators" />

##### Reference Following
<a id="reference_following" />

[Device:2][1] contains Parameters that reference other Parameters or Objects. The Reference Following mechanism allows references to Objects (not Parameters) to be followed from inside a single Path Name. Reference Following is indicated by a "+" character after the name of the Parameter that is referencing the Object followed by a ".", followed by Objects or Parameters that are children of the Referenced Object.

For example, `Device.NAT.PortMapping.{i}.Interface` references an IP Interface Object (`Device.IP.Interface.{i}.`) and that Object has a Parameter called "`Name`". With Reference Following, a Path Name of `Device.NAT.PortMapping.1.Interface+.Name` references the "`Name`" Parameter of the `Interface` Object that the `PortMapping` is associated with (i.e. it is the equivalent of using `Device.IP.Interface.1.Name` as the Path Name.

The steps that are executed by the Agent when following the reference in this example would be:

1.	Retrieve the appropriate instance of the `PortMapping` Object based on the Instance Number Addressing information

2.	Retrieve the value of the reference parameter Parameter that contains the reference, Interface, which in this case has the value "`Device.IP.Interface.1`"

3.	Replace the preceding path (`Device.NAT.PortMapping.1.Interface+`) with the value retrieved in Step 2

4.	Append the remainder of the Path Name (`.Name`), which builds the Path Name: `Device.IP.Interface.1.Name`

5.	Use `Device.IP.Interface.1.Name` as the Path Name for the action

*Note: It should be noted that according to the [Device:2 Schema][3], reference parameters:

* Always contain Path Names (not Search Expressions)
* When configured, can be configured using Path Names using Instance Number Addressing or Unique-Key Addressing, however:
* When the value of a reference parameter is read, all Instance Identifiers are returned as Instance Numbers.*

**R-ARC.12** - A USP Agent MUST support the ability to use Key-based addressing in reference values.

For example, the following paths might illustrate a reference to the same object (defined as having the KeyParam parameter as unique key) instance using an Instance Number and then a key value:

  * Object.SomeReferenceParameter = "Object.FooObject.5"
  * Object.SomeReferenceParameter = "Object.FooObject.[KeyParam=="KeyValueForInstance5"]"

In the first example, the reference points to the FooObject with Instance Number 5. In the second example, the reference points to the FooObject with a KeyParam value of "KeyValueForInstance5".

**R-ARC.13** - The following requirements relate to reference types and the associated Agent behavior:

  * An Agent MUST reject an attempt to set a strong reference parameter if the new value does not reference an existing parameter or object.
  * An Agent MUST NOT reject an attempt to set a weak reference parameter because the new value does not reference an existing parameter or object.
  * An Agent MUST change the value of a non-list-valued strong reference parameter to a null reference when a referenced parameter or object is deleted.
  * An Agent MUST remove the corresponding list item from a list-valued strong reference parameter when a referenced parameter or object is deleted.
  * An Agent MUST NOT change the value of a weak reference parameter when a referenced parameter or object is deleted.

##### List of References
<a id="list_of_references" />

The USP data models have Parameters whose values contain a list of references to other Parameters or Objects.  This section explains how the Reference Following mechanism allows those references to be followed from inside a single Path Name.  The Reference Following syntax as defined above still applies, but it is preceded by a means of referencing a specific instance within the list.  The additional syntax consists of a "`#`" character followed by list item number (1-indexed), which is placed between the name of the Parameter that contains the list of references and the "`+`" that indicates that the reference should be followed. To follow *all* references in the list, the endpoint can specify a "`#`" character followed by a wildcard ("`*`") character and the "`+`" character to follow the reference (i.e., "`ReferenceParameter#*+`").

For example, `Device.WiFi.SSID.{i}.LowerLayers` references a list of WiFi Radio Object (defined as `Device.WiFi.Radio.{i}.`) Instances that are associated with the SSID. This Object has a `Name` Parameter; so when following the first reference in the list of references a Path Name of `Device.WiFi.SSID.1.LowerLayers#1+.Name` references the Name of the WiFi Radio associated with this SSID Object Instance.

The steps that are executed by the Agent when following the reference in this example would be:

1.	Retrieve the appropriate `Device.Wifi.SSID.{i}` instance based on the Instance Number Addressing information

2.	Retrieve the value of the LowerLayers Parameter, which in this case has a value of "`Device.WiFi.Radio.1, Device.WiFi.Radio.2`"

3.	Retrieve the first list item within the value retrieved in Step 2 (i.e., "`Device.WiFi.Radio.1`")

4.	Replace the preceding path (`Device.WiFi.SSID.1.LowerLayers#1+`) with the value retrieved in Step 3

5.	Append the remainder of the Path Name (`.Name`), resulting in a Path Name of: `Device.WiFi.Radio.1.Name`

6.	Use `Device.WiFi.Radio.1.Name` as the Path Name for the action

##### Search Expressions and Reference Following
<a id="search_expressions_and_reference_following" />

The Reference Following and Search Expression mechanisms can be combined.

For example, reference the Signal Strength of all WiFi Associated Devices using the "ac" Operating Standard on the "MyHome" SSID, you would use the Path Name:

`Device.WiFi.AccessPoint.[SSIDReference+.SSID=="MyHome"].AssociatedDevice.{OperatingStandard=="ac"}.SignalStrength`

##### Operations/Commands
<a id="operation_command_path_names" />

The [Operate message](/messages/operate/) allows a USP Controller to execute Commands defined in the USP data models.  Commands are synchronous or asynchronous operations that don’t fall into the typical REST-based concepts of CRUD-N that have been incorporated into the protocol as specific messages. Commands are addressed like Parameter Paths that end with parentheses "()" to symbolize that it is a Command.  

For example: `Device.IP.Interface.[Name=="eth0"].Reset()`

##### Events
<a id="event_path_names" />

The Notify request allows a type of generic event (called Event) message that allows a USP Agent to emit events defined in the USP data models. Events are defined in and related to Objects in the USP data models like commands. Events are addressed like Parameter Paths that end with an exclamation point "!" to symbolize that it is an Event.

For example: `Device.LocalAgent.Boot!`

#### Instantiated Data Model Path Grammer
Expressed as a [Backus-Naur Form (BNF)](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) for context-free grammars, the path lexical rules for referencing the Instantiated Data Model are:

```
idmpath ::= objpath | parampath | cmdpath | evntpath | searchpath
objpath ::= name '.' (name (('.' inst)|(reffollow '.' name) )? '.')*
parampath ::= objpath name
cmdpath ::= objpath  name '()'
evntpath ::= objpath  name '!'
inst ::= posnum | keyref | expr | '*'
keyref ::= '[' keyexpr ( ',' keyexpr )* ']'
keyexpr ::= relpath '==' value
expr ::= '{' (exprcomp ( '&&' exprcomp )*) '}'
exprcomp ::= relpath oper value
relpath ::= name (reffollow? '.' name )*
reffollow ::=  ( '#' (posnum | '*') '+' )|  '+'
oper ::= '==' | '!=' | '<' | '>' | '<=' | '>='
value ::= literal | number
name ::= [A-Za-z_] [A-Za-z_0-9]*
literal ::= '"' [^"]* '"'
posnum ::= [1-9] [0-9]*
number ::= '0' | ( '-'? posnum )
```

The path lexical rules for referencing the Supported Data Model are:

```
sdmpath ::= name ‘.’ ( name ‘.’ ( ( posnum | ‘{i}’ ) ‘.’ )? )* name?
name ::= [A-Za-z_] [A-Za-z_0-9]*
posnum ::= [1-9] [0-9]*
```

##### BNF Diagrams for Instantiated Data Model
<a name="idmpath">**idmpath**:</a>

![](diagram/idmpath.png) <map name="idmpath.map"><area shape="rect" coords="49,1,115,33" href="#objpath" title="objpath"> <area shape="rect" coords="49,45,133,77" href="#parampath" title="parampath"> <area shape="rect" coords="49,89,121,121" href="#cmdpath" title="cmdpath"> <area shape="rect" coords="49,133,121,165" href="#evntpath" title="evntpath"> <area shape="rect" coords="49,177,135,209" href="#searchpath" title="searchpath"></map>

<div class="ebnf">

<code>[idmpath](#idmpath "idmpath")  ::= [objpath](#objpath "objpath")
           | [parampath](#parampath "parampath")
           | [cmdpath](#cmdpath "cmdpath")
           | [evntpath](#evntpath "evntpath")
           | [searchpath](#searchpath "searchpath")</code>

</div>
<br><br>

<a name="objpath">**objpath**:</a>

![](diagram/objpath.png) <map name="objpath.map"><area shape="rect" coords="29,121,83,153" href="#name" title="name"> <area shape="rect" coords="143,33,183,65" href="#inst" title="inst"> <area shape="rect" coords="143,77,197,109" href="#name" title="name"> <area shape="rect" coords="261,77,331,109" href="#reffollow" title="reffollow"> <area shape="rect" coords="371,1,425,33" href="#name" title="name"></map>

<div class="ebnf">

<code>[objpath](#objpath "objpath")  ::= [name](#name "name") '.' ( [name](#name "name") ( '.' [inst](#inst "inst") | [reffollow](#reffollow "reffollow") '.' [name](#name "name") )? '.' )*</code>

</div>

referenced by:

*   [cmdpath](#cmdpath "cmdpath")
*   [evntpath](#evntpath "evntpath")
*   [idmpath](#idmpath "idmpath")
*   [parampath](#parampath "parampath")
<br><br>


<a name="parampath">**parampath**:</a>

![](diagram/parampath.png) <map name="parampath.map"><area shape="rect" coords="29,1,95,33" href="#objpath" title="objpath"> <area shape="rect" coords="115,1,169,33" href="#name" title="name"></map>

<div class="ebnf">

<code>[parampath](#parampath "parampath")
         ::= [objpath](#objpath "objpath") [name](#name "name")</code>

</div>

referenced by:

*   [idmpath](#idmpath "idmpath")
<br><br>

<a name="cmdpath">**cmdpath**:</a>

![](diagram/cmdpath.png) <map name="cmdpath.map"><area shape="rect" coords="29,1,95,33" href="#objpath" title="objpath"> <area shape="rect" coords="115,1,169,33" href="#name" title="name"></map>

<div class="ebnf">

<code>[cmdpath](#cmdpath "cmdpath")  ::= [objpath](#objpath "objpath") [name](#name "name") '()'</code>

</div>

referenced by:

*   [idmpath](#idmpath "idmpath")
<br><br>


<a name="evntpath">**evntpath**:</a>

![](diagram/evntpath.png) <map name="evntpath.map"><area shape="rect" coords="29,1,95,33" href="#objpath" title="objpath"> <area shape="rect" coords="115,1,169,33" href="#name" title="name"></map>

<div class="ebnf">

<code>[evntpath](#evntpath "evntpath") ::= [objpath](#objpath "objpath") [name](#name "name") '!'</code>

</div>

referenced by:

*   [idmpath](#idmpath "idmpath")
<br><br>


<a name="inst">**inst**:</a>

![](diagram/inst.png) <map name="inst.map"><area shape="rect" coords="49,1,117,33" href="#posnum" title="posnum"> <area shape="rect" coords="49,45,107,77" href="#keyref" title="keyref"> <area shape="rect" coords="49,89,95,121" href="#expr" title="expr"></map>

<div class="ebnf">

<code>[inst](#inst "inst")     ::= [posnum](#posnum "posnum")
           | [keyref](#keyref "keyref")
           | [expr](#expr "expr")
           | '*'</code>

</div>

referenced by:

*   [objpath](#objpath "objpath")
<br><br>

<a name="keyref">**keyref**:</a>

![](diagram/keyref.png) <map name="keyref.map"><area shape="rect" coords="95,45,163,77" href="#keyexpr" title="keyexpr"></map>

<div class="ebnf">

<code>[keyref](#keyref "keyref")   ::= '[' [keyexpr](#keyexpr "keyexpr") ( ',' [keyexpr](#keyexpr "keyexpr") )* ']'</code>

</div>

referenced by:

*   [inst](#inst "inst")
<br><br>

<a name="keyexpr">**keyexpr**:</a>

![](diagram/keyexpr.png) <map name="keyexpr.map"><area shape="rect" coords="29,1,89,33" href="#relpath" title="relpath"> <area shape="rect" coords="169,1,219,33" href="#value" title="value"></map>

<div class="ebnf">

<code>[keyexpr](#keyexpr "keyexpr")  ::= [relpath](#relpath "relpath") '==' [value](#value "value")</code>

</div>

referenced by:

*   [keyref](#keyref "keyref")
<br><br>

<a name="expr">**expr**:</a>

![](diagram/expr.png) <map name="expr.map"><area shape="rect" coords="97,45,177,77" href="#exprcomp" title="exprcomp"></map>

<div class="ebnf">

<code>[expr](#expr "expr")     ::= '{' [exprcomp](#exprcomp "exprcomp") ( '&&' [exprcomp](#exprcomp "exprcomp") )* '}'</code>

</div>

referenced by:
*   [inst](#inst "inst")
<br><br>

<a name="exprcomp">**exprcomp**:</a>

![](diagram/exprcomp.png) <map name="exprcomp.map"><area shape="rect" coords="29,1,89,33" href="#relpath" title="relpath"> <area shape="rect" coords="109,1,155,33" href="#oper" title="oper"> <area shape="rect" coords="175,1,225,33" href="#value" title="value"></map>

<div class="ebnf">

<code>[exprcomp](#exprcomp "exprcomp") ::= [relpath](#relpath "relpath") [oper](#oper "oper") [value](#value "value")</code>

</div>

referenced by:

*   [expr](#expr "expr")
<br><br>

<a name="relpath">**relpath**:</a>

![](diagram/relpath.png) <map name="relpath.map"><area shape="rect" coords="49,77,103,109" href="#name" title="name"> <area shape="rect" coords="113,33,183,65" href="#reffollow" title="reffollow"></map>

<div class="ebnf">

<code>[relpath](#relpath "relpath")  ::= [name](#name "name") ( [reffollow](#reffollow "reffollow")? '.' [name](#name "name") )*</code>

</div>

referenced by:

*   [exprcomp](#exprcomp "exprcomp")
*   [keyexpr](#keyexpr "keyexpr")
<br><br>


<a name="reffollow">**reffollow**:</a>

![](diagram/reffollow.png) <map name="reffollow.map"><area shape="rect" coords="119,33,187,65" href="#posnum" title="posnum"></map>

<div class="ebnf">

<code>[reffollow](#reffollow "reffollow")
         ::= ( '#' ( [posnum](#posnum "posnum") | '*' ) )? '+'<code>

</div>

referenced by:

*   [objpath](#objpath "objpath")
*   [relpath](#relpath "relpath")
<br><br>

<a name="oper">**oper**:</a>

![](diagram/oper.png)

<div class="ebnf">

<code>[oper](#oper "oper")     ::= '=='
           | '!='
           | '<'
           | '>'
           | '<='
           | '>='</code>

</div>

referenced by:

*   [exprcomp](#exprcomp "exprcomp")
<br><br>

<a name="value">**value**:</a>

![](diagram/value.png) <map name="value.map"><area shape="rect" coords="49,1,99,33" href="#literal" title="literal"> <area shape="rect" coords="49,45,115,77" href="#number" title="number"></map>

<div class="ebnf">

<code>[value](#value "value")    ::= [literal](#literal "literal")</code>
           | [number](#number "number")

</div>

referenced by:

*   [exprcomp](#exprcomp "exprcomp")
*   [keyexpr](#keyexpr "keyexpr")
<br><br>


<a name="name">**name**:</a>

![](diagram/name.png)

<div class="ebnf">

<code>[name](#name "name")     ::= [A-Za-z_] [A-Za-z_0-9]*</code>

</div>

referenced by:

*   [cmdpath](#cmdpath "cmdpath")
*   [evntpath](#evntpath "evntpath")
*   [objpath](#objpath "objpath")
*   [parampath](#parampath "parampath")
*   [relpath](#relpath "relpath")
<br><br>


<a name="literal">**literal**:</a>

![](diagram/literal.png)


<code>[literal](#literal "literal")  ::= '"' [^"]* '"'</code>

referenced by:

*   [value](#value "value")
<br><br>


<a name="number">**number**:</a>

![](diagram/number.png) <map name="number.map"><area shape="rect" coords="135,45,203,77" href="#posnum" title="posnum"></map>

<div class="ebnf">

<code>[number](#number "number")   ::= '0'
           | '-'? [posnum](#posnum "posnum")</code>

</div>

referenced by:

*   [value](#value "value")
<br><br>

<a name="posnum">**posnum**:</a>

![](diagram/posnum.png)

<div class="ebnf">

<code>[posnum](#posnum "posnum")   ::= [1-9] [0-9]*</code>

</div>

referenced by:

*   [inst](#inst "inst")
*   [number](#number "number")
*   [reffollow](#reffollow "reffollow")
<br><br>


##### BNF Diagrams for Supported Data Model
<a name="sdmpath">**sdmpath**:</a>

![](diagram/sdmpath.png) <map name="sdmpath.map"><area shape="rect" coords="29,17,83,49" href="#name" title="name"> <area shape="rect" coords="187,17,241,49" href="#name" title="name"> <area shape="rect" coords="345,49,413,81" href="#posnum" title="posnum"> <area shape="rect" coords="577,49,631,81" href="#name" title="name"></map>

<div class="ebnf">

<code>[sdmpath](#sdmpath "sdmpath")  ::= [name](#name "name") '.' ( [name](#name "name") '.' ( ( [posnum](#posnum "posnum") | '{i}' ) '.' )? )* [name](#name "name")?</code>

</div>
<br><br>

<a name="name">**name**:</a>

![](diagram/name.png)

<div class="ebnf">

<code>[name](#name "name")     ::= [A-Za-z_] [A-Za-z_0-9]*</code>

</div>

referenced by:

*   [sdmpath](#sdmpath "sdmpath")
<br><br>

<a name="posnum">**posnum**:</a>

![](diagram/posnum.png)

<div class="ebnf">

<code>[posnum](#posnum "posnum")   ::= [1-9] [0-9]*</code>

</div>

referenced by:

*   [sdmpath](#sdmpath "sdmpath")

<br><br>

[<-- Overview](/specification/)
[Discovery -->](/specification/discovery/)
