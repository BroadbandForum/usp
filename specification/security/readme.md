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

USP provides an end-to-end security mechanism in addition to any security provided by the Message Transfer Protocol.

**R-SEC.0** – All USP endpoints MUST implement the USP end-to-end security mechanism.

**R-SEC.1** – All USP messages MUST be secured by the USP end-to-end security mechanism.

The current discussion on the structure and requirements for the USP end-to-end security mechanism is available for Broadband Forum members to view on the BBF wiki at:

https://wiki.broadband-forum.org/display/BBF/Security+Discussion

## Authentication and Authorization

Authentication of Endpoints is done using X.509 certificates as defined in [RFC 5280][15] and [RFC 6818][16]. These certificates, at a minimum, need to be usable for [MTP security](/mtp/#securing_mtps) with TLS or DTLS protocols.

In order to support various authentication models (e.g., trust Endpoint identity and associated certificate on first use; precise Endpoint identity is indicated in a certificate issued by a trusted Certificate Authority; trust that Endpoint is a member of a trusted domain as verified by a trusted Certificate Authority), this Working Text provides guidance based on conditions under which the Endpoint is operating, and on the Endpoint's policy for storing certificates of other Endpoints or just certificates of trusted CAs.

**R-SEC.2** – The Agent MUST have a Controller's certificate information prior to establishing an encrypted connection.

TLS and DTLS both have handshake mechanisms that allow for exchange of certificate information.

## Access Control List

It is expected that Agents will have some sort of Access Control List (ACL) that will define different levels of authorization for interacting with the Agent's data model. This Working Text refers to different levels of authorization as "Roles". The Agent may be so simple as to only support a single Role that gives full access to its data model; or it may have just an "untrusted" Role and a "full access" Role. Or it may be significantly more complex with, for example, "untrusted" Role, different Roles for parents and children in a customer household, and a different Role for the service provider Controller. These Roles may be fully defined in the Agent's code, or Role definition may be allowed via the data model.

## Trusted Certificate Authorities

An Agent can have a configured list of trusted Certificate Authority (CA) root certificates. The agent policy may trust the CA to approve validated Controllers to have a specific default Role, or the policy may simply trust the CA to validate the Controller identity.

**R-SEC.3** – To validate against a root certificate, the Agent MUST contain one or more trusted root certificates that are either pre-loaded in the Agent or provided to the Agent by a secure means.

This secure means can accomplished through USP (see section below on Data Model Elements), or through a mechanism external to USP.

**R-SEC.4** – Where a CA is only trusted to validate Controller identity, the Agent MUST ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

**R-SEC.5** – Where a CA is trusted to approve a Controller Role, but the Role the Agent has assigned to the Controller is different than te CA-identified Role, the Agent MUST ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

**R-SEC.6** – Where a CA is trusted to approve a Controller Role, and the Controller does not have a different Role assigned, the Agent MUST either ensure the URN form of the Controller Endpoint ID is in the Controller certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute, or perform the following validation:

## Self-Signed Certificates

**R-SEC.7** – An Endpoint that generates a self-signed certificate MUST place the URN form of its Endpoint ID in a certificate `subjectaltName` with a type `uniformResourceIdentifier` attribute.

Self-signed certificates supplied by Controllers can only be meaningfully used in cases where a person is in a position to provide Authorization (what Role the Controller is trusted to have). Whether or not an Agent allows self-signed certificates from a Controller is a matter of Agent policy.

**R-SEC.8** – If an Agent allows Controllers to provide self-signed certificates, the Agent MUST assign such Controllers an "untrusted" Role on first use.

That is, the Agent will trust the certificate for purpose of encryption, but will heavily restrict what the Controller is authorized to do.

**R-SEC.9** – If an Agent allows Controllers to provide self-signed certificates, the Agent MUST have a means of allowing an external entity to change the Role of each such Controller.

**R-SEC.10** – If an Agent allows Controllers to provide self-signed certificates, the Agent MUST have a means of allowing an external entity to Role to each such Controller.

Controller policy related to trust of Agent self-signed certificates is left to the Controller. Controllers may be designed to refuse self-signed certificates (thereby refusing to control the Agent), they may have a means of allowing a person to approve controlling the Agent via the Controller, or they may automatically accept the Agent.

**R-SEC.11** – An Endpoint that accepts self-signed certificates MUST maintain the association of accepted certificate public keys and Endpoint IDs.

## Challenge Strings

It is possible for the Agent to allow an external entity to change a Controller Role by means of a Challenge string. This Challenge string can take various forms, including having a user supply a passphrase or a PIN. Such a string could be printed on the Agent packaging, or supplied by means of a SMS to a phone number associated with the user account. These Challenge strings can be done using USP operations. Independent of how challenges are accomplished, following are some basic requirements related to Challenge strings.

**R-SEC.12** – The Agent MAY have factory-default Challenge string(s) in its configuration.

**R-SEC.13** – A factory-default Challenge string MUST be unique to the Agent. Re-using the same passphrase among multiple Agents is not permitted.

**R-SEC.14** – A factory-default Challenge string MUST NOT be derivable from information the Agent communicates about itself using any protocol at any layer.

**R-SEC.15** – The Agent MUST limit the number of tries for the Challenge string to be supplied successfully.

**R-SEC.16** – The Agent SHOULD have policy to lock out all use of Challenge strings for some time, or indefinitely, if the number of tries limit is exceeded.

## Data Model Elements Related to Authentication and Authorization

Service Elements for use with these requirements can be found in the [Device:2 Data Model for TR-069 Devices and USP Agents][1] in the `Device.LocalAgent.ControllerTrust.` object. Theory of Operations for data model elements related to authentication and authorization are TBD. Note that allowing visibility or control via USP of ACLs, certificate lists, and challenges is an Agent implementation decision.
