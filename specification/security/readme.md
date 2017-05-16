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
[15]: https://tools.ietf.org/html/rfc5280 "RFC 5290 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[16]: https://tools.ietf.org/html/rfc6818 "RFC 6818 Updates to the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"

[Conventions]: https://www.ietf.org/rfc/rfc2119.txt "Key words for use in RFCs to Indicate Requirement Levels"

# Security

*NOTE: Version 1.0 of this protocol will define end-to-end security above the MTP. All Endpoints will be required to implement end-to-end security and use it to secure USP messages at that time.*

<!--
USP provides an end-to-end security mechanism in addition to any security provided by the Message Transfer Protocol.

**R-SEC.0** - All USP endpoints MUST implement the USP end-to-end security mechanism.

**R-SEC.1** - All USP messages MUST be secured by the USP end-to-end security mechanism.

The current discussion on the structure and requirements for the USP end-to-end security mechanism is available for Broadband Forum members to view on the BBF wiki at:

https://wiki.broadband-forum.org/display/BBF/Security+Discussion
-->

## Authentication and Authorization

Authentication of Endpoints is done using X.509 certificates as defined in [RFC 5280][15] and [RFC 6818][16]. These certificates, at a minimum, need to be usable for [MTP security](/mtp/#securing_mtps) with TLS or DTLS protocols.

In order to support various authentication models (e.g., trust Endpoint identity and associated certificate on first use; precise Endpoint identity is indicated in a certificate issued by a trusted Certificate Authority; trust that Endpoint is a member of a trusted domain as verified by a trusted Certificate Authority), this Working Text provides guidance based on conditions under which the Endpoint is operating, and on the Endpoint's policy for storing certificates of other Endpoints or just certificates of trusted CAs.

**R-SEC.2** - The Agent MUST have a Controller's certificate information prior to establishing an encrypted connection.

TLS and DTLS both have handshake mechanisms that allow for exchange of certificate information.

## Access Control List

It is expected that Agents will have some sort of Access Control List (ACL) that will define different levels of authorization for interacting with the Agent's data model. This Working Text refers to different levels of authorization as "Roles". The Agent may be so simple as to only support a single Role that gives full access to its data model; or it may have just an "untrusted" Role and a "full access" Role. Or it may be significantly more complex with, for example, "untrusted" Role, different Roles for parents and children in a customer household, and a different Role for the service provider Controller. These Roles may be fully defined in the Agent's code, or Role definition may be allowed via the data model.

## Trusted Certificate Authorities

An Agent can have a configured list of trusted Certificate Authority (CA) root certificates. The agent policy may trust the CA to approve validated Controllers to have a specific default Role, or the policy may simply trust the CA to validate the Controller identity.

**R-SEC.3** - To validate against a root certificate, the Agent MUST contain one or more trusted root certificates that are either pre-loaded in the Agent or provided to the Agent by a secure means.

This secure means can accomplished through USP (see section below on Data Model Elements), or through a mechanism external to USP.

**R-SEC.4** - Where a CA is only trusted to validate Controller identity, the Agent MUST ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

**R-SEC.5** - Where a CA is trusted to approve a Controller Role, but the Role the Agent has assigned to the Controller is different than te CA-identified Role, the Agent MUST ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

**R-SEC.6** - Where a CA is trusted to approve a Controller Role, and the Controller does not have a different Role assigned, the Agent MUST either ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute, or perform the following validation:

* If the host portion of the Controller URL is a DNS name, this MUST be done according to the principles of [RFC 6125](https://tools.ietf.org/html/rfc6125), using the host portion of the Controller URL as the reference identifier.
* If the host portion of the Controller URL is an IP address, this MUST be done by comparing the IP address against any presented identifiers that are IP addresses.

*Note - the terms “reference identifier” and “presented identifier” are defined in [RFC 6125](https://tools.ietf.org/html/rfc6125).*
Note - wildcard certificates are permitted as described in [RFC 6125](https://tools.ietf.org/html/rfc6125).

**R-SEC.7**   An Agent capable of obtaining absolute time SHOULD wait until it has accurate absolute time before contacting a Controller.  If an Agent for any reason is unable to obtain absolute time, it can contact the Controller without waiting for accurate absolute time. If an Agent chooses to contact a Controller before it has accurate absolute time (or if it does not support absolute time), it MUST ignore those components of the Controller certificate that involve absolute time, e.g. not-valid-before and not-valid-after certificate restrictions.

## Self-Signed Certificates
<a id='self-signed-certificates'/>

**R-SEC.8** - An Endpoint that generates a self-signed certificate MUST place the URN form of its Endpoint ID in a certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

Self-signed certificates supplied by Controllers can only be meaningfully used in cases where a person is in a position to provide Authorization (what Role the Controller is trusted to have). Whether or not an Agent allows self-signed certificates from a Controller is a matter of Agent policy.

**R-SEC.9** - If an Agent allows Controllers to provide self-signed certificates, the Agent MUST assign such Controllers an "untrusted" Role on first use.

That is, the Agent will trust the certificate for purpose of encryption, but will heavily restrict what the Controller is authorized to do.

**R-SEC.10** - If an Agent allows Controllers to provide self-signed certificates, the Agent MUST have a means of allowing an external entity to change the Role of each such Controller.

**R-SEC.11** - If an Agent allows Controllers to provide self-signed certificates, the Agent MUST have a means of allowing an external entity to Role to each such Controller.

Controller policy related to trust of Agent self-signed certificates is left to the Controller. Controllers may be designed to refuse self-signed certificates (thereby refusing to control the Agent), they may have a means of allowing a person to approve controlling the Agent via the Controller, or they may automatically accept the Agent.

**R-SEC.12** - An Endpoint that accepts self-signed certificates MUST maintain the association of accepted certificate public keys and Endpoint IDs.

## Challenge Strings

It is possible for the Agent to allow an external entity to change a Controller Role by means of a Challenge string. This Challenge string can take various forms, including having a user supply a passphrase or a PIN. Such a string could be printed on the Agent packaging, or supplied by means of a SMS to a phone number associated with the user account. These Challenge strings can be done using USP operations. Independent of how challenges are accomplished, following are some basic requirements related to Challenge strings.

**R-SEC.13** - The Agent MAY have factory-default Challenge string(s) in its configuration.

**R-SEC.14** - A factory-default Challenge string MUST be unique to the Agent. Re-using the same passphrase among multiple Agents is not permitted.

**R-SEC.15** - A factory-default Challenge string MUST NOT be derivable from information the Agent communicates about itself using any protocol at any layer.

**R-SEC.16** - The Agent MUST limit the number of tries for the Challenge string to be supplied successfully.

**R-SEC.17** - The Agent SHOULD have policy to lock out all use of Challenge strings for some time, or indefinitely, if the number of tries limit is exceeded.

### Agent certificates

**R-SEC.18** - Support for Controller authentication of Agents using certificates signed by an appropriate CA chain is OPTIONAL for both Agents and Controllers. When certificates are used to authenticate the Agent to a Controller, the subjectaltName MUST contain either:

* the URN form of the Agent Endpoint ID with a type uniformResourceIdentifier attribute.
* the URN form of an Endpoint ID with a type uniformResourceIdentifier attribute, and with wildcards such that all Agent Endpoint IDs covered by the certificate fall within the wildcarded Endpoint ID.

**R-SEC-19** - If the Agent does not have a CA-issued cetificate, it MUST support use of a self-signed certificate. See requirements for Endpoints using [self-signed certificates](#self-signed-certificates).

## Theory of operations

The following theory of operations relies on objects, parameters, events, and operations from the [Device:2 Data Model for TR-069 Devices and USP Agents][1].

### Data Model Elements

These data model elements play a role in reporting on and allowing control of trusted Controllers and the permissions they have to read and write parts of the Agent’s data model, and allowing an Agent to establish trust with a Controller.

* `Controller.{i}.Role` object

From components `CoAP` and `HTTP`:

* Objects `MTP.{i}.CoAP.` , `Controller.{i}.MTP.{i}.CoAP.` , `MTP.{i}.HTTP.`, and `Controller.{i}.MTP.{i}.HTTP.`
* Parameters `EnableEncryption`, `ValidatePeerCertificate`, and `CheckPeerID`.

From component `ControllerTrust`:

* Object `ControllerTrust.`
* Parameter `UntrustedRole`	 
* Object `ControllerTrust.Role.{i}.`
* Object `ControllerTrust.Credential.{i}.`
* Object `ControllerTrust.Challenge.{i}.`

* Parameter `Controller.{i}.Credential`

### Roles (Access Control)

Controller permissions are conveyed in the data model through Roles.

#### Role Definition

A Role is expressed in the data model through use of the `ControllerTrust.Role.{i}.` object. This object can have multiple entries with the same `Role` parameter value. All entries with the same `Role` value combine together to define the Role. Each entry in this object identifies the Role it applies to, the Target (data model path that the related permissions apply to), permissions related to parameters, objects, instantiated objects, and commands identified by the Target parameter, and the relative order of precedence among entries for the same Role (the larger value of this parameter takes priority over an entry with a smaller value in the case of overlapping Targets for the same Role).

The permissions of a Role for the specified Targets are described by `ParameterPermissions`, `ObjectPermissions`, `InstantiatedObjectPermissions`, and `CommandEventPermissions` parameters. Each of these is expressed as a string of 4 characters where each character represents a permission ("`r`" for Read, "`w`" for Write, "`x`" for Execute", and "`n`" for Notify). The string is always in the same order (`rwxn`) and the lack of a permission is signified by a "`-`" character (e.g., `r--n`). How these permissions are applied to parameters, objects, and various Messages is described in the data model description of these parameters.

An Agent that wants to allow Controllers to define and modify Roles will implement the `ControllerTrust.Role.{i}.` object with all of the parameters listed in the data model. In order for a Controller to define or modify Role entries, it will need to be assigned a Role that gives it the necessary permission. Care should be taken to avoid defining this Role’s permissions such that an Agent with this Role can modify the Role such that it can no longer make future modifications to the `ControllerTrust.Role.{i}.` object.

A simple Agent that only wants to inform Controllers of pre-defined Roles (with no ability to modify or define additional Roles) can implement the `ControllerTrust` object with read-only data model definition for all entries and parameters. A simple Agent could even implement the object with read-only data model definition and just the `Alias` and `Role` parameters, with a single entry per Role; this could be sufficient in a case where the Role names convey enough information (e.g., there are only two pre-defined Roles named `“Untrusted”` and `“FullAccess”`).

An even simpler Agent might not implement `ControllerTrust.Role.{i}.` at all, if the Roles are sufficiently intuitive for users.

#### Special Roles

Two special Roles are identified by the `UntrustedRole` and `BannedRole` parameters under the `ControllerTrust.` object. An Agent can expose these parameters with read-only data model implementation if it simply wants to tell Controllers the names of these specific Roles.

The `UntrustedRole` is the Role the Agent will automatically assign to any Controller that has not been authorized for a different Role. Any Agent that has a means of allowing a Controller’s Role to be changed (by users through a Challenge string, by other Controllers through modification of `Controller.{i}.Role`, or through some other external means) and that allows “unknown” Controllers to attach will need to have an “untrusted” Role defined; even if the identity of this Role is not exposed to Controllers through implementation of the `UntrustedRole` parameter.

The `BannedRole` (if implemented) is assigned automatically by the Agent to Controllers whose certificates are invalid or have been revoked. If it is not implemented, the Agent can use the `UntrustedRole` for this, as well. It is also possible to simply implement policy for treatment of invalid or revoked certificates (e.g., refuse to connect), rather than associate them with a specific Role. This is left to the Agent policy implementation.

If the `ControllerTrust.Role.{i}.` object is implemented, it is good practice to include the `UntrustedRole` and `BannedRole` (if implemented) values in that table.

#### A Controller’s Role

A Controller’s assigned Roles can be conveyed by the `Controller.{i}.Role` parameter. This parameter is a list of all Role values assigned to the Controller. Where multiple assigned Roles have overlapping Targets, the resulting permission is the union of all assigned permissions. For example, if two Roles have the same Target with one Role assigning `ParameterPermissions` a value of `r---` and the other Role assigning `ParameterPermissions` a value of `---n`, the resulting permission will be `r--n`.

It is strongly recommended that Agents implement the Controller object with the `Role` parameter (with at least read-only data model definition), so users can see what Controllers have access to the Agent. This will help users identify rogue Controllers that may have gained access to the Agent.

#### Role Associated with a Credential or Challenge

The `ControllerTrust.Credential.{i}.Role` parameter is a default Role that is assigned to Controllers that have not previously been assigned a Role (other than “Untrusted” and whose credentials have been validated using the credentials in the same entry of the `ControllerTrust.Credential.{i}.` table. For more information on use of this table for assigning Controller Roles and validating credentials, see the sections below.

The `ControllerTrust.Challenge.{i}.Role` parameter is a default Role that is assigned to Controllers that send a successful `ChallengeResponse()` command. For more information on use of challenges for assigning Controller Roles, see the sections below. ## Assigning Controller Roles As mentioned above, the `Controller.{i}.Role` parameter can be used to expose the Controller’s assigned Role via the data model.

*Note: Even if it is not exposed through the data model, the Agent is expected to maintain knowledge of the permissions assigned to each known Controller.*

Controllers can be assigned Roles through a variety of methods, depending on the data model elements an Agent implements and the Agent’s coded policy. Note that it is possible for an Agent to maintain trusted credentials with associated permissions (as described by the `ControllerTrust.Credential.{i}.` object) and various default permission definitions (as identified by the `UntrustedRole` and `BannedRole` parameters) without exposing these through the data model. If the data is maintained but not exposed, the same methods can still be used.

* Another Controller (with appropriate permission) can insert a Controller (including the Role parameter value) into the `Controller.{i}.` table, or can modify the Role of an existing `Controller.{i}.` entry.

In the case of a Controller that has not previously been assigned a Role or who has been assigned the value of `UntrustedRole`:

* If credentials in an entry in a `ControllerTrust.Credential.{i}.Credential` parameter with an associated `ControllerTrust.Credential.{i}.Role` parameter are used to successfully validate the certificate presented by the Controller, the Controller is assigned the Role from the associated `ControllerTrust.Credential.{i}.Role`. This also applies if the Controller currently just has the role indicated in `UntrustedRole`.

* If the Controller’s certificate is validated by credentials in a `ControllerTrust.Credential.{i}.Credential` parameter but there is no associated `ControllerTrust.Credential.{i}.Role` parameter (or the value is empty), then the Controller is assigned the role in `UntrustedRole`. Note that assigning `UntrustedRole` means there needs to be some implemented way to elevate the Controller’s Role, either by another Controller manipulating the Role, implementing Challenges, or some non-USP method.

* If the Controller’s certificate is self-signed or is validated by credentials not in `ControllerTrust.Credential.{i}.`, the Agent policy may be to assign the role in `UntrustedRol`e. This policy can be influenced by the `MTP.{i}.<MTP>.ValidatePeerCertificate` parameter, if implemented, as described in the next section.

* If the Agent implements the `RequestChallenge()` and `ChallengeResponse()` commands, a Controller assigned the role in `UntrustedRole` can have permission to read one or more `ControllerTrust.Challenge.{i}.Alias` and `Description` values and issue the commands. Higher Roles can have permission to read additional `ControllerTrust.Challenge.{i}.Alias` and `Description` values. A successful Challenge results in the Controller being assigned the associated Role value.

* A Controller that presents a revoked or invalid certificate will be assigned the role in `BannedRole`, if this parameter or policy is implemented.

#### Controller Certificates and Certificate Validation

When an Agent is presented with a Controller’s certificate, the Agent will always attempt to validate the certificate to whatever extent possible. The scenarios below describe how data model elements can be used to drive the policy for handling various successful and unsuccessful attempts at validation.

Note that it is possible for an Agent to maintain policy of the type described by the `UntrustedRole`, `BannedRole`, and `MTP.{i}.<MTP>.ValidatePeerCertificate` parameters, and the information described by `ControllerTrust.Credential.{i}.` and `Controller.{i}.Credential` without exposing these through the data model. If the policy concepts and data are maintained but not exposed, the same methods can still be used. It is also possible for an Agent to have policy that is not described by any defined data model element.

1. If the certificate presented by the Controller is self-signed then:
    1. If the certificate is not in `Controller.{i}.Credential`, it includes the Controller Endpoint ID, and `MTP.{i}.<MTP>.ValidatePeerCertificate` is false, the Agent assigns sets `Controller.{i}.Role` to the role in `UntrustedRole`. The Agent stores the certificate information in `Controller.{i}.Credential`.
      1. If the certificate is not in `Controller.{i}.Credential` and either does not include the Controller Endpoint ID or `MTP.{i}.<MTP>.ValidatePeerCertificate` is true, the Agent refuses to establish an encrypted connection with the Controller and does not store the certificate information.
      2. If the certificate is in `Controller.{i}.Credential` and includes the Controller Endpoint ID, the Agent considers the certificate valid for purpose of confirming Controller identity, and allows the Controller use of its `Controller.{i}.Role`.
2. If the certificate indicates it has a chain of trust leading to a Certificate Authority (CA), and the CA indicates the certificate is not valid or has been revoked, the Agent will assign `Controller.{i}.Role` the role in `BannedRole`.
3. If the certificate indicates it has a chain of trust leading to a Certificate Authority (CA) and the CA indicates the certificate is valid, but the CA is not in `ControllerTrust.Credential.{i}.`, the certificate is treated like a self-signed certificate.
4. If the certificate indicates it has a chain of trust, but the CA is unreachable (e.g., no Internet access or CA not responding for some reason):
    1. If the Controller certificate is in `Controller.{i}.Credential` and includes the correct Controller Endpoint ID and `MTP.{i}.<MTP>.ValidatePeerCertificate` is `false`, the Agent will consider the certificate valid for purpose of confirming Controller identity, and allow the Controller use of `Controller.{i}.Role`.
    2. If the Controller certificate is in `Controller.{i}.Credential` and either does not include the correct Controller Endpoint ID or `MTP.{i}.<MTP>.ValidatePeerCertificate` is `true`, the Agent refuses to establish an encrypted connection with the Controller.
    3. If the Controller certificate is not in `Controller.{i}.Credential`, the Agent will treat it like a self-signed certificate.
5. If the certificate has a chain of trust, the CA indicates the certificate is valid, the CA is in
`ControllerTrust.Credential.{i}.`, the CA is reachable, and the certificate includes the Controller Endpoint ID:
    1. If the Controller has a `Controller.{i}.Role` that is not the role in `UntrustedRole`, the Agent considers the certificate valid for purpose of confirming Controller identity, and allows the Controller use of its `Controller.{i}.Role`. This includes the case where `Controller.{i}.Role` is the role in `BannedRole`.
    2. If the Controller has no `Controller.{i}.` entry, empty `Controller.{i}.Role`, or has `Controller.{i}.Role` with the role listed in `UntrustedRole`, *and* the CA has a non-empty `ControllerTrust.Credential.{i}.Role`, the Agent assigns `Controller.{i}.Role` this Role.
    3. If the Controller has no `Controller.{i}.` entry or empty `Controller.{i}.Role`, and there is no `ControllerTrust.Credential.{i}.Role`, the Agent assigns the `Controller.{i}.Role` the role listed in `UntrustedRole`.
6. If the certificate has a chain of trust, the CA indicates the certificate is valid, the CA is in `ControllerTrust.Credential.{i}.`, the CA is reachable, and the certificate does not include the Controller Endpoint ID, but does include the Controller domain, with or without wildcard:
    1. If the CA has a non-empty `ControllerTrust.Credential.{i}.Role`, the Agent applies the `ControllerTrust.Credential.{i}.Role` to the Controller for the current TLS or DTLS session, but does not permanently modify `Controller.{i}.Role`. Any Role associated with the Controller Endpoint ID is ignored, because the identity of the actual Controller identity has not been validated.
    2. If the Controller has no `Controller.{i}.` entry or empty `Controller.{i}.Role`, and `ControllerTrust.Credential.{i}.Role` is empty, the Agent assigns the `Controller.{i}.Role` the role listed in `UntrustedRole`.

### Encryption

The `EnableEncryption` parameter, if implemented in `MTP.{i}.CoAP.` or `MTP.{i}.HTTP.`, allows encryption of the MTP to be enabled or disabled. If this parameter is not implemented, then there is no USP mechanism to toggle encryption. It is recommended that Agents implement the ability to encrypt all MTPs (via TLS 1.2 or DTLS 1.2 insert references, as appropriate), enable it by default, and not implement the ability to disable it.

### Challenges

An Agent can implement the ability to provide Controllers with challenges via USP, in order to be trusted with certain Roles. It is also possible to use non-USP methods to issue challenges, such as HTTP digest authentication with prompts for login and password.

To use the USP mechanism, the `RequestChallenge()` and `ChallengeResponse()` commands and `ControllerTrust.Challenge.{i}.` object with at least the `Alias` and `Description` parameters must be implemented. The other functionality implied by the other `ControllerTrust.Challenge.{i}.` needs to be implemented, but does not have to be exposed through the data model.

A Controller that sends a Get message on `Device.ControllerTrust.Challenge.{i}.` will receive all entries and parameters that are allowed for its current assigned Role. In the simplest case, this will be a single entry and only Alias and Description will be supplied for that entry. It is important to restrict visibility to all other implemented parameters to highly trusted Roles.

The Controller can display the value of `Description` to the user and allow the user to indicate they want to request the described challenge. If multiple entries were returned, the user can be asked to select which challenge they want to request, based on the description. An example of a description might be “Request administrative privileges” or “Request guest privilege”.

When the user indicates to the Controller which challenge they want, the Controller sends `RequestChallenge()` with the `Alias` associated with the selected `Description`. The Agent replies with the associated `Instruction` and an auto-generated `ChallengeID`. The Controller presents the value of `Instruction` to the user. Examples of an instruction might be “Enter passphrase printed on bottom of device” or “Enter PIN sent to registered email address”. The user enters a string per the instructions, and the Controller sends this value together with the `ChallengeID` in `ChallengeResponse()`.

If the returned value matches `Value`, the Agent gives a successful response - otherwise it returns an unsuccessful response. If successful, the `ControllerTrust.Challenge.{i}.Role` replaces an `UntrustedRole` in `Controller.{i}.Role` or is appended to any other `Controller.{i}.Role` value.

The number of times a `ControllerTrust.Challenge.{i}.` entry can be consecutively failed (across all Controllers, without intermediate success) is defined by `Retries`. Once the number of failed consecutive attempts equals `Retries`, the `ControllerTrust.Challenge.{i}.` cannot be retried until after `LockoutPeriod` has expired.

Type values other than `Passphrase` can be used and defined to trigger custom mechanisms, such as requests for emailed or SMS-provided PINs.
