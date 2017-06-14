# USP Message Abstraction Proxy

The USP Message Abstraction Proxy presents an abstracted view of Agents to Controllers via a proxying device that has both Agent and Controller. The proxy’s Agent supports a data model for the proxy’s Controller function, including representations of proxied Agents.

This sort of proxying allows the proxy to present an abstracted view of a group of Agents as being represented by a single Agent. A Controller could send a single USP Message to the proxy’s Agent, and the proxy would in turn send individual USP Messages to each of the proxied Agents.

## Agent Modelling of a USP Controller

An Agent that models a USP Controller is able to gain information about Agents that the proxied Controller interacts with.

### Agent Certificates and Certificate Validation

When an Controller is presented with an Agent's certificate, the Controller could attempt to validate the certificate to whatever extent possible. The scenarios below describe how data model elements can be used to drive the policy for handling various successful and unsuccessful attempts at validation.

Note that it is possible for an Controller to maintain policy of the type described by the `MTP.{i}.<MTP>.ValidatePeerCertificate` parameters, and the information described by `RemoteAgent.Credential.{i}.` without exposing these through the data model. If the policy concepts and data are maintained but not exposed, the same methods can still be used. It is also possible for a Controller to have policy that is not described by any defined data model element.

1. If the certificate presented by the Agent is self-signed:
  1. If the certificate is not in `RemoteAgent.{i}.Credential` and includes the Agent Endpoint ID and `MTP.{i}.<MTP>.ValidatePeerCertificate` is false, the Controller might wish to discard messages from the Agent. The Controller might store the certificate information in `RemoteAgent.{i}.Credential`.
    1. If the certificate is not in `RemoteAgent.{i}.Credential` and either does not include the Agent Endpoint ID or `MTP.{i}.<MTP>.ValidatePeerCertificate` is true, the Controller refuses to establish an encrypted connection with the Agent and does not store the certificate information.

2. If the certificate indicates it has a chain of trust leading to a Certificate Authority (CA) and the CA indicates the certificate is valid, but the CA is not in `Security.Credential.{i}.`, the certificate is treated like a self-signed certificate.

3. If the certificate indicates it has a chain of trust, but the CA is unreachable (e.g., no Internet access or CA not responding for some reason):

  1. If the Agent certificate is in `RemoteAgent.{i}.Credential` and includes the correct Agent Endpoint ID and `MTP.{i}.<MTP>.ValidatePeerCertificate` is `false`, the Controller will consider the certificate valid for purpose of confirming Agent identity, and allows messages from the Agent.

  2. If the Agent certificate is in `RemoteAgent.{i}.Credential` and either does not include the correct Agent Endpoint ID or `MTP.{i}.<MTP>.ValidatePeerCertificate` is true, the Controller refuses to establish an encrypted connection with the Agent.

  3. If the Agent certificate is not in `RemoteAgent.{i}.Credential`, the Controller will treat it like a self-signed certificate.

4. If the certificate has a chain of trust, the CA indicates the certificate is valid, the CA is in `Security.Credential.{i}.`, the CA is reachable, and the certificate includes the Agent Endpoint ID
If the Controller considers the certificate valid for purpose of confirming Agent identity, and allows messages from the Agent.

5. If the certificate has a chain of trust, the CA indicates the certificate is valid, the CA is in `Security.Credential.{i}.`, the CA is reachable, and the certificate does not include the Agent Endpoint ID, but does include the Agent domain, with or without wildcard, it is up to the implementation to accept messages from the Agent.
