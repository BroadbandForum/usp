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
[Conventions]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"

# Authentication and Authorization

1. [Authentication](#authentication)
2. [Role Based Access Control (RBAC)](#role_based_access_control_rbac)
3. [Trusted Certificate Authorities](#trusted_certificate_authorities)
4. [Trusted Brokers](#trusted_brokers)
5. [Self-Signed Certificates](#self_signed_certificates)
6. [Agent Authentication](#agent_authentication)
7. [Challenge Strings and Images](#challenge_strings_and_images)
8. [Analysis of Controller Certificates](#analysis_of_controller_certificates)
    1. [Receiving a USP Record](#receiving_a_usp_record)
    2. [Sending a USP Record](#sending_a_usp_record)
    3. [Checking a Certificate Containing an Endpoint ID](#checking_a_certificate_containing_an_endpoint_id)
    4. [Using a Trusted Broker](#using_a_trusted_broker)
9. [Theory of Operations](#theory_of_operations)
    1. [Data Model Elements](#data_model_elements)
    2. [Roles (Access Control)](#roles_access_control)
    3. [Assigning Controller Roles](#assigning_controller_roles)
    4. [Controller Certificates and Certificate Validation](#controller_certificates_and_certificate_validation)
    5. [Challenges](#challenges)
    6. [Certificate Management](#certificate_management)
    7. [Application of Modified Parameters](#application_of_modified_parameters)

USP contains mechanisms for Authentication and Authorization, and Encryption. Encryption can be provided at the MTP layer, the USP layer, or both. Where Endpoints can determine (through Authentication) that the termination points of the MTP and USP messages are the same, MTP encryption is sufficient to provide end-to-end encryption and security. Where the termination points are different (because there is a proxy or other intermediate device between the USP Endpoints), USP layer [Secure Message Exchange](../e2e-message-exchange/index.md#) is required, or the intermediate device must be a trusted part of the end-to-end ecosystem.

<a id='authentication' />

## Authentication

Authentication of Controllers is done using X.509 certificates as defined in [RFC 5280][15] and [RFC 6818][16]. Authentication of Agents is done either by using X.509 certificates or shared secrets. X.509 certificates, at a minimum, need to be usable for [MTP security]( ../mtp/index.md#securing_mtps) with TLS or DTLS protocols. It is recommended that Agents implement the ability to encrypt all MTPs using one of these two protocols, enable it by default, and not implement the ability to disable it.

In order to support various authentication models (e.g., trust Endpoint identity and associated certificate on first use; precise Endpoint identity is indicated in a certificate issued by a trusted Certificate Authority; trust that MTP connection is being made to a member of a trusted domain as verified by a trusted Certificate Authority (CA)), this specification provides guidance based on conditions under which the Endpoint is operating, and on the Endpoint's policy for storing certificates of other Endpoints or certificates of trusted CAs. The `Device.LocalAgent.Certificate` object can be implemented if choosing to expose these stored certificates through the data model. See the Theory of Operations, Certificate Management subsection, below for additional information.

**R-SEC.0** - Prior to processing a USP Message from a Controller, the Agent MUST either:

* have the Controller's certificate information and have a cryptographically protected connection between the two Endpoints, or
* have a Trusted Broker's certificate information and have a cryptographically protected connection between the Agent and the Trusted Broker

TLS and DTLS both have handshake mechanisms that allow for exchange of certificate information. If the MTP connection is between the Agent and Controller (for example, without going through any application-layer proxy or other intermediate application-layer middle-box), then a secure MTP connection will be sufficient to ensure end-to-end protection, and the USP Record can use `payload_security` "PLAINTEXT" encoding of the Message. If the middle-box is part of a trusted end-to-end ecosystem, the MTP connection may also be considered sufficient. Otherwise, the USP Record will use [Secure Message Exchange](../e2e-message-exchange/index.md#).   

Whether a Controller requires Agent certificates is left up to the Controller implementation.

<a id='role_based_access_control_rbac' />

## Role Based Access Control (RBAC)

It is expected that Agents will have some sort of Access Control List (ACL) that will define different levels of authorization for interacting with the Agent's data model. This Working Text refers to different levels of authorization as "Roles". The Agent may be so simple as to only support a single Role that gives full access to its data model; or it may have just an "untrusted" Role and a "full access" Role. Or it may be significantly more complex with, for example, "untrusted" Role, different Roles for parents and children in a customer household, and a different Role for the service provider Controller. These Roles may be fully defined in the Agent's code, or Role definition may be allowed via the data model.

**R-SEC.1** - An Agent MUST confirm a Controller has the necessary permissions to perform the requested actions in a Message prior to performing that action.

**R-SEC.1a** - Agents SHOULD implement the Controller object with the `AssignedRole` parameter (with at least read-only data model definition) and `InheritedRole` parameter (if allowed Roles can come from a trusted CA), so users can see what Controllers have access to the Agent and their permissions. This will help users identify rogue Controllers that may have gained access to the Agent.

See the Theory of Operations, Roles (Access Control) and Assigning Controller Roles subsections, below for additional information on data model elements that can be implemented to expose information and allow control of Role definition and assignment.

<a id='trusted_certificate_authorities' />

## Trusted Certificate Authorities

An Endpoint can have a configured list of trusted Certificate Authority (CA) certificates. The Agent policy may trust the CA to authorize authenticated Controllers to have a specific default Role, or the policy may only trust the CA to authenticate the Controller identity. The Controller policy may require an Agent certificate to be signed by a trusted CA before the Controller exchanges USP Messages with the Agent.

**R-SEC.2** - To confirm a certificate was signed by a trusted CA, the Endpoint MUST contain information from one or more trusted CA certificates that are either pre-loaded in the Endpoint or provided to the Endpoint by a secure means. At a minimum, this stored information will include a certificate fingerprint and fingerprint algorithm used to generate the fingerprint. The stored information MAY be the entire certificate.

This secure means can be accomplished through USP (see [Theory of Operations](./#theory-of-operations), Certificate Management subsection, making use of the `Device.LocalAgent.Certificate` object), or through a mechanism external to USP. The stored CA certificates can be root or intermediate CAs.

**R-SEC.3** - Where a CA is trusted to authenticate Controller identity, the Agent MUST ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute, and this matches the USP Record `from_id`.

**R-SEC.4** - Where a CA is trusted to authorize a Controller Role, the Agent MUST ensure the URN form of the Controller Endpoint ID (that matches the USP Record `from_id`) is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

Note that trusting a CA to authorize a Controller Role requires the Agent to maintain an association between a CA certificate and the Role(s) that CA is trusted to authorize. If the Agent allows CAs to authorize Roles, the Agent will need to identify specific CA certificates in a Controller’s chain of trust that can authorize Roles. The specific Role(s) associated with such a CA certificate can then be inherited by the Controller. The `Device.LocalAgent.ControllerTrust.Credential` object can be implemented to expose and allow control over trust and authorization of CAs.

<a id='trusted_brokers' />

## Trusted Brokers

An Endpoint can have a configured list of Trusted Broker certificates. The Endpoint policy would be to trust the broker to vouch for the identity of Endpoints it brokers – effectively authenticating the `from_id` contained in a received USP Record. The Agent policy may trust the broker to authorize all Controllers whose Records transit the broker to have a specific default Role.

**R-SEC.4a** - To confirm a certificate belongs to a Trusted Broker, the Endpoint MUST contain information from one or more Trusted Broker certificates that are either pre-loaded in the Endpoint or provided to the Endpoint by a secure means. This stored information MUST be sufficient to determine if a presented certificate is the Trusted Broker certificate.

This secure means of loading certificate information into an Agent can be accomplished through USP (see Theory of Operations section related to Certificate Management), or through a mechanism external to USP.

Note that trusting a broker to authorize a Controller Role requires the Agent to maintain an association between a Trusted Broker certificate and the Role(s) that Trusted Broker is trusted to authorize. The `Device.LocalAgent.ControllerTrust.Credential` object can be implemented to expose and allow control over identifying Trusted Brokers. The `AllowedUses` parameter is used to indicate whether an entry is a Trusted Broker.

<a id='self_signed_certificates'/>

## Self-Signed Certificates

**R-SEC.5** - An Endpoint that generates a self-signed certificate MUST place the URN form of its Endpoint ID in a certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

Self-signed certificates supplied by Controllers can only be meaningfully used in cases where a person is in a position to provide Authorization (what Role the Controller is trusted to have). Whether or not an Agent allows self-signed certificates from a Controller is a matter of Agent policy.

**R-SEC.6** - If an Agent allows Controllers to provide self-signed certificates, the Agent MUST assign such Controllers an "untrusted" Role on first use.

That is, the Agent will trust the certificate for purpose of encryption, but will heavily restrict what the Controller is authorized to do.

**R-SEC.7** - If an Agent allows Controllers to provide self-signed certificates, the Agent MUST have a means of allowing an external entity to change the Role of each such Controller.

Controller policy related to trust of Agent self-signed certificates is left to the Controller. Controllers may be designed to refuse self-signed certificates (thereby refusing to control the Agent), they may have a means of allowing a person to approve controlling the Agent via the Controller, or they may automatically accept the Agent.

**R-SEC.8** - An Endpoint that accepts self-signed certificates MUST maintain the association of accepted certificate and Endpoint IDs.

Self-signed certificates require a "trust on first use" (TOFU) policy when using them to authenticate an Endpoint's identity. An external entity (a trusted Controller or user) can then authorize the authenticated Endpoint to have certain permissions. Subsequent to the first use, this same self-signed certificate can be trusted to establish the identity of that Endpoint. However, authentication of the Endpoint can only be subsequently trusted if the association of certificate to identity is remembered (i.e., it is known this is the same certificate that was used previously by that Endpoint). If it is not remembered, then every use is effectively a first use and would need to rely on an external entity to authorize permissions every time. The `Device.LocalAgent.Certificate` object can be implemented if choosing to expose and allow control of remembered certificates in the data model.

<a id='agent_authentication' />

## Agent Authentication

**R-SEC.9** - Controllers MUST authenticate Agents either through X.509 certificates, a shared secret, or by trusting a Trusted Broker to vouch for Agent identity.

When authentication is done using X.509 certificates, it is up to Controller policy whether to allow for Agents with self-signed certificates or to require Agent certificates be signed by a CA.

Note that allowing use of, method for transmitting, and procedure for handling shared secrets is specific to the MTP used, as described in [Message Transfer Protocols](../mtp/index.md). Shared secrets that are not unique per device are not recommended as they leave devices highly vulnerable to various attacks -- especially devices exposed to the Internet.

**R-SEC.10** - An Agent certificate MUST contain the URN form of the Agent Endpoint ID in the `subjectaltName` with a type `uniformResourceIdentifier` attribute.

**R-SEC.10a** - The certificate `subjectaltName` value MUST be used to authenticate the USP Record `from_id` for any Records secured with an Agent certificate.

Agent certificates can be used to secure Records by encrypting at the MTP layer [Message Transfer Protocols](../mtp/index.md) enryption and/or encrypting at the USP layer [Secure Message Exchange](../e2e-message-exchange/index.md#).

Some Controller implementations may allow multiple Agents to share a single certificate with a wildcarded Endpoint ID.

**R-SEC.11** - If a single certificate is shared among multiple Agents, those Agents MUST include a wild-carded `instance-id` in the Endpoint ID in the `subjectaltName` with identical `authority-scheme` and `authority-id`.

Use of a shared certificate is not recommended, and which portion of the `instance-id` can be wildcarded may be specific to the authorizing CA or to the `authority-id` and `authority-scheme` values of the Endpoint ID. Wildcards can only be allowed in cases where the assigning entity is explicitly identified. Controllers are not required to support wildcarded certificates.

**R-SEC.12** - If a wildcard character is present in the `instance-id` of an Endpoint ID in a certificate `subjectaltName`, the `authority-scheme` MUST be one of "oui", "cid", "pen", "os", or "ops". In the case of "os" and "ops", the portion of the `instance-id` that identifies the assigning entity MUST NOT be wildcarded.

<a id='challenge_strings_and_images' />

## Challenge Strings and Images

It is possible for the Agent to allow an external entity to change a Controller Role by means of a Challenge string or image. This Challenge string or image can take various forms, including having a user supply a passphrase or a PIN. Such a string could be printed on the Agent packaging, or supplied by means of a SMS to a phone number associated with the user account. These Challenge strings or images can be done using USP operations. Independent of how challenges are accomplished, following are some basic requirements related to Challenge strings and images.

**R-SEC.13** - The Agent MAY have factory-default Challenge value(s) (strings or images) in its configuration.

**R-SEC.14** - A factory-default Challenge value MUST be unique to the Agent. Re-using the same passphrase among multiple Agents is not permitted.

**R-SEC.15** - A factory-default Challenge value MUST NOT be derivable from information the Agent communicates about itself using any protocol at any layer.

**R-SEC.16** - The Agent MUST limit the number of tries for the Challenge value to be supplied successfully.

**R-SEC.17** - The Agent SHOULD have policy to lock out all use of Challenge values for some time, or indefinitely, if the number of tries limit is exceeded.

See the Theory of Operations, Challenges subsection, below for a description of data model elements that need to be implemented and are used when doing challenges through USP operations.

<a id='analysis_of_controller_certificates'/>

## Analysis of Controller Certificates

An Agent will analyze Controller certificates to determine if they are valid, are appropriate for authentication of Controllers, and to determine what permissions (Role) a Controller has. The Agent will also determine whether MTP encryption is sufficient to provide end-to-end protection of the Record and Message, or if USP layer [Secure Message Exchange](../e2e-message-exchange/index.md#) is required.

The diagrams in this section use the database symbol to identify where the described information can be represented in the data model, if an implementation chooses to expose this information through the USP protocol.

<a id='receiving_a_usp_record' />

### Receiving a USP Record

**R-SEC.19** - An Agent capable of obtaining absolute time SHOULD wait until it has accurate absolute time before contacting a Controller.  If an Agent for any reason is unable to obtain absolute time, it can contact the Controller without waiting for accurate absolute time. If an Agent chooses to contact a Controller before it has accurate absolute time (or if it does not support absolute time), it MUST ignore those components of the Controller certificate that involve absolute time, e.g. not-valid-before and not-valid-after certificate restrictions.

**R-SEC.20** - An Agent that has obtained accurate absolute time MUST validate those components of the Controller certificate that involve absolute time.

**R-SEC.21** – An Agent MUST clear all cached encryption session and Role authorization information when it reboots.

**R-SEC.22** - When an Agent receives a USP Record, the Agent MUST execute logic that achieves the same results as in the decision flows from Figures [SEC.1](./#figure-SEC1) and [SEC.2](./#figure-SEC2).

<img src="receive-record.png" />

Figure SEC.1 – Receiving a USP Record

<a id='figure-SEC1'/>

---

<img src="no-secure-message-exchange.png" />

Figure SEC.2 – USP Record without USP Layer Secure Message Exchange

<a id='figure-SEC2'/>

<a id='sending_a_usp_record' />

### Sending a USP Record

**R-SEC.23** - When an Agent sends a USP Record, the Agent MUST execute logic that achieves the same results as in the decision flow from Figure [SEC.3](./#figure-SEC3).

<img src="send-record.png" />

Figure SEC.3 – Sending a USP Record

<a id='figure-SEC3'/>

<a id='checking_a_certificate_containing_an_endpoint_id' />

### Checking a Certificate Containing an Endpoint ID

**R-SEC.24** - When an Agent analyzes a Controller certificate for authentication and determining permissions (Role), the Agent MUST execute logic that achieves the same results as in the decision flows from Figures [SEC.4](./#figure-SEC4) and [SEC.5](./#figure-SEC5).

**R-SEC.25** - When determining the inherited Role to apply based on Roles associated with a trusted CA, only the first matching CA in the chain will be used.

<img src="check-cert.png" />

Figure SEC.4 – Checking a Certificate Containing an Endpoint ID

<a id='figure-SEC4'/>

---

<img src="determine-role.png" />

Figure SEC.5 – Determining the Role

<a id='figure-SEC5'/>

<a id='using_a_trusted_broker' />

### Using a Trusted Broker

Support for Trusted Broker logic is optional.

**R-SEC.26** - If Trusted Brokers are supported, and a Trusted Broker is encountered (from the optional "Trusted Broker cert?" decision diamonds in Figures SEC.2 or SEC.3), the Agent MUST execute logic that achieves the same results as in the decision flows from Figure [SEC.6](./#figure-SEC6) for a received USP Record and Figure [SEC.7](./#figure-SEC7) for sending a USP Record.

<img src="broker-with-received-record.png" />

Figure SEC.6 - Trusted Broker with Received Record

<a id='figure-SEC6'/>

---

<img src="broker-with-sent-record.png" />

Figure SEC.7 - Trusted Broker Sending a Record

<a id='figure-SEC7'/>

<a id="theory_of_operations" />

## Theory of Operations

The following theory of operations relies on objects, parameters, events, and operations from the `LocalAgent` Object of the [Device:2 Data Model][1].

<a id='data_model_elements' />

### Data Model Elements

These data model elements play a role in reporting on and allowing control of trusted Controllers and the permissions they have to read and write parts of the Agent’s data model, and allowing an Agent to establish trust with a Controller.

* `LocalAgent.Controller.{i}.AssignedRole` parameter
* `LocalAgent.Controller.{i}.InheritedRole` parameter
* `LocalAgent.Controller.{i}.Credential` parameter

From component `ControllerTrust`:

* Object `LocalAgent.ControllerTrust.`
* Parameters `UntrustedRole`, `BannedRole`, TOFUAllowed, TOFUInactivityTimer
* Commands `RequestChallenge()`, `ChallengeResponse()`
* Object `LocalAgent.ControllerTrust.Role.{i}.`
* Object `LocalAgent.ControllerTrust.Credential.{i}.`
* Object `LocalAgent.ControllerTrust.Challenge.{i}.`

The Object `LocalAgent.Certificate.` can be used to manage Controller and CA certificates, along with the `LocalAgent.AddCertificate()` and `LocalAgent.Controller.{i}.AddMyCertificate()` commands.

For brevity, `Device.LocalAgent` is not placed in front of all further object references in this Security section. However, all objects references are under `Device.LocalAgent`. This section does not describe use of parameters under other top level components.

<a id='roles_access_control' />

### Roles (Access Control)

Controller permissions are conveyed in the data model through Roles.

#### Role Definition

A Role is described in the data model through use of the `ControllerTrust.Role.{i}.` object. Each entry in this object identifies the Role it describes, and has a `Permission.` sub-object for the `Targets` (data model paths that the related permissions apply to), permissions related to parameters, objects, instantiated objects, and commands identified by the `Targets` parameter, and the relative `Order` of precedence among `Permission.` entries for the Role (the larger value of this parameter takes priority over an entry with a smaller value in the case of overlapping `Targets` entries for the Role).

The permissions of a Role for the specified `Target` entries are described by `Param`, `Obj`, `InstantiatedObj`, and `CommandEvent` parameters. Each of these is expressed as a string of 4 characters where each character represents a permission ("`r`" for Read, "`w`" for Write, "`x`" for Execute", and "`n`" for Notify). The 4 characters are always presented in the same order in the string (`rwxn`) and the lack of a permission is signified by a "`-`" character (e.g., `r--n`). How these permissions are applied to parameters, objects, and various Messages is described in the data model description of these parameters.

An Agent that wants to allow Controllers to define and modify Roles will implement the `ControllerTrust.Role.{i}.` object with all of the parameters listed in the data model. In order for a Controller to define or modify Role entries, it will need to be assigned a Role that gives it the necessary permission. Care should be taken to avoid defining this Role’s permissions such that an Agent with this Role can modify the Role and no longer make future modifications to the `ControllerTrust.Role.{i}.` object.

A simple Agent that only wants to inform Controllers of pre-defined Roles (with no ability to modify or define additional Roles) can implement the `ControllerTrust.Role.` object with read-only data model definition for all entries and parameters. A simple Agent could even implement the object with read-only data model definition and just the `Alias` and `Role` parameters, and no `Permission.` sub-object; this could be sufficient in a case where the Role names convey enough information (e.g., there are only two pre-defined Roles named `"Untrusted"` and `"FullAccess"`).

#### Special Roles

Two special Roles are identified by the `UntrustedRole` and `BannedRole` parameters under the `ControllerTrust.` object. An Agent can expose these parameters with read-only data model implementation if it simply wants to tell Controllers the names of these specific Roles.

The `UntrustedRole` is the Role the Agent will automatically assign to any Controller that has not been authorized for a different Role. Any Agent that has a means of allowing a Controller’s Role to be changed (by users through a Challenge string, by other Controllers through modification of `Controller.{i}.AssignedRole`, or through some other external means) and that allows "unknown" Controllers to attach will need to have an "untrusted" Role defined; even if the identity of this Role is not exposed to Controllers through implementation of the `UntrustedRole` parameter.

The `BannedRole` (if implemented) is assigned automatically by the Agent to Controllers whose certificates have been revoked. If it is not implemented, the Agent can use the `UntrustedRole` for this, as well. It is also possible to simply implement policy for treatment of invalid or revoked certificates (e.g., refuse to connect), rather than associate them with a specific Role. This is left to the Agent policy implementation.

#### A Controller’s Role

A Controller’s assigned Roles can be conveyed by the `Controller.{i}.AssignedRole` parameter. This parameter is a list of all Role values assigned to the Controller through means other than `ControllerTrust.Credential.{i}.Role`. A Controller’s inherited Roles (those inherited from `ControllerTrust.Credential.{i}.Role` as described in the next section) need to be maintained separately from assigned Roles and can be conveyed by the `Controller.{i}.InheritedRole` parameter. Where multiple assigned and inherited Roles have overlapping `Targets` entries, the resulting permission is the union of all assigned and inherited permissions. For example, if two Roles have the same `Targets` with one Role assigning the `Targets` `Param` a value of `r---` and the other Role assigning `Param` a value of `---n`, the resulting permission will be `r--n`. This is done after determining which `ControllerTrust.Role.{i}.Permission.{i}` entry to apply for each Role for specific `Targets`, in the case where a Role has overlapping `Permission.{i}.Targets` entries for the same Role.

For example,
 Given the following `ControllerTrust.Role.{i}.` entries:

```
  i=1, Role = "A"; Permission.1.: Targets = "Device.LocalAgent.", Order = 3, Param = "r---"
  i=1, Role = "A"; Permission.2.: Targets = "Device.LocalAgent.Controller.", Order = 55, Param = "r-xn"
  i=3, Role = "B"; Permission.1: Targets = "Device.LocalAgent.", Order = 20, Param = "r---"
  i=3, Role = "B"; Permission.5: Targets = "Device.LocalAgent.Controller.", Order = 78, Param = "----"
```

 and `Device.LocalAgent.Controller.1.AssignedRole` = "Device.LocalAgent. ControllerTrust.Role.1., Device.LocalAgent. ControllerTrust.Role.3."

When determining permissions for the `Device.LocalAgent.Controller.` table, the Agent will first determine that for Role A Permission.2 takes precedence over Permission.1 (55 > 3). For B, Permission.5 takes precedence over Permission.1 (78 > 20). The union of A and B is "r-xn" + "----" = "r-xn".

#### Role Associated with a Credential or Challenge

The `ControllerTrust.Credential.{i}.Role` parameter value is inherited by Controllers whose credentials have been validated using the credentials in the same entry of the `ControllerTrust.Credential.{i}.` table. Whenever `ControllerTrust.Credential.{i}.` is used to validate a certificate, the Agent writes the current value of the associated `ControllerTrust.Credential.{i}.Role` into the `Controller.{i}.InheritedRole` parameter.  For more information on use of this table for assigning Controller Roles and validating credentials, see the sections below.

The `ControllerTrust.Challenge.{i}.Role` parameter is a Role that is assigned to Controllers that send a successful `ChallengeResponse()` command. For more information on use of challenges for assigning Controller Roles, see the sections below.

<a id='assigning_controller_roles' />

### Assigning Controller Roles

As mentioned above, the `Controller.{i}.AssignedRole` parameter can be used to expose the Controller’s assigned Role via the data model.

*Note: Even if it is not exposed through the data model, the Agent is expected to maintain knowledge of the permissions assigned to each known Controller.*

Controllers can be assigned Roles through a variety of methods, depending on the data model elements an Agent implements and the Agent’s coded policy. Note that it is possible for an Agent to maintain trusted CA credentials with associated permissions (as described by the `ControllerTrust.Credential.{i}.` object) and various default permission definitions (as identified by the `UntrustedRole` and `BannedRole` parameters) without exposing these through the data model. If the data is maintained but not exposed, the same methods can still be used.

Figures [SEC.4](./#figure-SEC4) and [SEC.5](./#figure-SEC5) in the above [Analysis of Controller Certificates](./#analysis-controller-certificates) section identify points in the decision logic where some of the following calls to data model parameters can be made. The following bullets note when they are identified in one of these figures.

* Another Controller (with appropriate permission) can insert a Controller (including the `AssignedRole` parameter value) into the `Controller.{i}.` table, or can modify the `AssignedRole` parameter of an existing `Controller.{i}.` entry. The `InheritedRole` value cannot be modified by another Controller.

* If credentials in an entry in a `ControllerTrust.Credential.{i}.Credential` parameter with an associated `ControllerTrust.Credential.{i}.Role` parameter are used to successfully validate the certificate presented by the Controller, the Controller inherits the Role from the associated `ControllerTrust.Credential.{i}.Role`. The Agent writes this value to the `Controller.{i}.InheritedRole` parameter. This step is shown in Figure [SEC.5](./#figure-SEC5).

* A Controller whose associated certificate is revoked by a CA can be assigned the role in `BannedRole`, if this parameter or policy is implemented. In this case, the value of `BannedRole` must be the only value in `Controller.{i}.AssignedRole` (all other entries are removed) and `Controller.{i}.InheritedRole` must be empty (all entries are removed). This step is shown in Figure [SEC.4](./#figure-SEC4).In the case of a Controller that has not previously been assigned a Role or who has been assigned the value of `UntrustedRole`:

* If the Controller’s certificate is validated by credentials in a `ControllerTrust.Credential.{i}.Credential` parameter but there is no associated `ControllerTrust.Credential.{i}.Role` parameter (or the value is empty), then the Controller is assigned the role in `UntrustedRole` (written to the `Controller.{i}.AssignedRole` parameter). This step is shown in Figure [SEC.5](./#figure-SEC5). Note that assigning `UntrustedRole` means there needs to be some implemented way to elevate the Controller’s Role, either by another Controller manipulating the Role, implementing Challenges, or some non-USP method.

* If the Controller’s certificate is self-signed or is validated by credentials not in `ControllerTrust.Credential.{i}.`, the Agent policy may be to assign the role in `UntrustedRole`. The optional policy decision (whether or not to allow Trust on First Use (TOFU), which can be codified in the data model with the ControllerTrust.TOFUAllowed flag) is shown in Figure [SEC.4](./#figure-SEC4); Figure [SEC.5](./#figure-SEC5) shows the Role assignment.

* If the Agent implements the `RequestChallenge()` and `ChallengeResponse()` commands, a Controller assigned the role in `UntrustedRole` can have permission to read one or more `ControllerTrust.Challenge.{i}.Alias` and `Description` values and issue the commands. Roles with more extensive permissions can have permission to read additional `ControllerTrust.Challenge.{i}.Alias` and `Description` values. A successful Challenge results in the Controller being assigned the associated Role value.

<a id='controller_certificates_and_certificate_validation'/>

### Controller Certificates and Certificate Validation

When an Agent is presented with a Controller’s certificate, the Agent will always attempt to validate the certificate to whatever extent possible. Figures [SEC.4](./#figure-SEC4) and [SEC.5](./#figure-SEC5) in [Analysis of Controller Certificates](./#analysis-controller-certificates) identify points in the decision logic where data model parameters can be used to influence policy decisions related to Controller certificate analysis.

Note that it is possible for an Agent to maintain policy of the type described by the `UntrustedRole`, `BannedRole`, and the information described by `ControllerTrust.Credential.{i}.` and `Controller.{i}.Credential` without exposing these through the data model. If the policy concepts and data are maintained but not exposed, the same methods can still be used. It is also possible for an Agent to have policy that is not described by any defined data model element.

<a id='challenges' />

### Challenges

An Agent can implement the ability to provide Controllers with challenges via USP, in order to be trusted with certain Roles. It is also possible to use non-USP methods to issue challenges, such as HTTP digest authentication with prompts for login and password.

To use the USP mechanism, the `RequestChallenge()` and `ChallengeResponse()` commands and `ControllerTrust.Challenge.{i}.` object with at least the `Alias`, `Role`, and `Description` parameters needs to be implemented. The functionality implied by the other `ControllerTrust.Challenge.{i}.` parameters needs to be implemented, but does not have to be exposed through the data model.

A Controller that sends a Get message on `Device.ControllerTrust.Challenge.{i}.` will receive all entries and parameters that are allowed for its current assigned Role. In the simplest case, this will be a single entry and only Alias and Description will be supplied for that entry. It is important to restrict visibility to all other implemented parameters to highly trusted Roles, if at all.

The Controller can display the value of `Description` to the user and allow the user to indicate they want to request the described challenge. If multiple entries were returned, the user can be asked to select which challenge they want to request, based on the description. An example of a description might be "Request administrative privileges" or "Request guest privilege".

When the user indicates to the Controller which challenge they want, the Controller sends `RequestChallenge()` with the path name of the `Challenge` object instance associated with the desired `Description`. The Agent replies with the associated `Instruction`, `InstructionType`, `ValueType` and an auto-generated `ChallengeID`. The Controller presents the value of `Instruction` to the user (in a manner appropriate for `InstructionType`). Examples of an instruction might be "Enter passphrase printed on bottom of device" or "Enter PIN sent to registered email address". The user enters a string per the instructions, and the Controller sends this value together with the `ChallengeID` in `ChallengeResponse()`.

If the returned value matches `Value`, the Agent gives a successful response - otherwise it returns an unsuccessful response. If successful, the `ControllerTrust.Challenge.{i}.Role` replaces an `UntrustedRole` in `Controller.{i}.AssignedRole` or is appended to any other `Controller.{i}.AssignedRole` value.

The number of times a `ControllerTrust.Challenge.{i}.` entry can be consecutively failed (across all Controllers, without intermediate success) is defined by `Retries`. Once the number of failed consecutive attempts equals `Retries`, the `ControllerTrust.Challenge.{i}.` cannot be retried until after `LockoutPeriod` has expired.

Type values other than `Passphrase` can be used and defined to trigger custom mechanisms, such as requests for emailed or SMS-provided PINs.

<a id='certificate_management' />

### Certificate Management

If an Agent wants to allow certificates associated with Controllers and CAs to be exposed through USP, the Agent can implement the `Controller.{i}.Credential` and `ControllerTrust.Credential.{i}.Credential` parameters, which require implementation of the `LocalAgent.Certificate.` object. Allowing management of these certificates through USP can be accomplished by implementing `LocalAgent.AddCertificate()`, `Controller.{i}.AddMyCertificate()` and `Certificate.{i}.Delete()` commands.

To allow a Controller to check whether the Agent has correct certificates, the `Certificate.{i}.GetFingerprint()` command can be implemented.

<a id='application_of_modified_parameters' />

### Application of Modified Parameters

It is possible that various parameters related to authentication and authorization may change that would impact cached encrypted sessions and Role permissions for Controllers. Example of such parameters include `Controller.{i}.AssignedRole`, `Controller.{i}.Credential`, `ControllerTrust.Role.` definition of a Role, and `ControllerTrust.Credential.{i}.Role`.

There is no expectation that an Agent will apply these changes to cached sessions. It is up to the Agent to determine whether or not it will detect these changes and flush cached session information. However, it is expected that a reboot will clear all cached session information.


[<-- Messages](../messages/index.md)

[Extensions -->](../extensions/index.md)
