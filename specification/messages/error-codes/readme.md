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
[Conventions]: https://www.ietf.org/rfc/rfc2119.txt "Key words for use in RFCs to Indicate Requirement Levels"

# Error Codes

<a id="error_codes" />

USP uses error codes with a range of 6000-6999 for Controller errors, and 7000-7999 for Agent errors. The errors appropriate for each message (and how they must be implemented) are defined in the message descriptions below.

## Controller Error Codes

<a id="controller_error_codes" />

*Note: The 6000 series of errors applies entirely to Error messages sent in reply to Notify Requests from an Agent.*

| Code | Name | Description
| -----: | :------------: | :---------------------- |
|`6000` | Message failed | This error indicates a general failure that is described in an err_msg element. |
|`6001` | Message not supported | This error indicates that the attempted message was not understood by the target endpoint. |
|`6002` | Request denied (no reason specified) | This error indicates that the target endpoint cannot or will not process the message. |
| `6003` | Internal error	| This error indicates that the message failed due to internal hardware or software reasons.|
| `6004` | Invalid arguments | This error indicates that the message failed due to invalid values in the Request elements and/or the failure to update one or more parameters during an Add or Set message.
| `6005` |	Resources exceeded | This error indicates that the message failed due to memory or processing limitations on the target endpoint. |
| `6006` | Permission denied | This error indicates that the source endpoint does not have the authorization to use this message on the target endpoint. |
| `6800-6999` | Vendor defined error codes | These errors are vendor defined(#vendor_defined_error_codes). |

## Agent Error Codes

<a id="agent_error_codes" />

*Note: The 7000 series of errors applies entirely to Error messages sent in reply to Requests from a Controller.*

| Code | Name | Description
| -----: | :------------: | :---------------------- |
| `7000` | Message failed	| This error indicates a general failure that is described in an err_msg element. |
| `7001` | Message not supported | This error indicates that the attempted message was not understood by the target endpoint.|
| `7002` | Request denied (no reason specified) | This error indicates that the target endpoint cannot or will not process the message. |
| `7003` | Internal error | This error indicates that the message failed due to internal hardware or software reasons. |
| `7004` | Invalid arguments | This error indicates that the message failed due to invalid values in the Request elements and/or the failure to update one or more parameters during an Add or Set message. |
| `7005` | Resources exceeded | This error indicates that the message failed due to memory or processing limitations on the target endpoint. |
| `7006` | Permission denied  | This error indicates that the source endpoint does not have the authorization for this action. |
| `7007` | Invalid configuration | This error indicates that the message failed because processing the message would put the target endpoint in an invalid or unrecoverable state. |
| `7008` | Invalid path syntax | This error indicates that the Path Name used was not understood by the target endpoint. |
| `7009` | Parameter action failed | This error indicates that the parameter failed to update for a general reason described in an err_msg element. |
| `7010` | Unsupported parameter | This error indicates that the requested Path Name associated with this ParamError did not match any instantiated parameters. |
| `7011` | Invalid type | This error indicates that the requested value was not of the correct data type for the parameter. |
| `7012` | Invalid value | This error indicates that the requested value was not within the acceptable values for the parameter. |
| `7013` | Attempt to update non-writeable parameter. | This error indicates that the source endpoint attempted to update a parameter that is not defined as a writeable parameter. |
| `7014` | Value conflict | This error indicates that the requested value would result in an invalid configuration based on other parameter values. |
| `7015` | Operation error | This error indicates a general failure in the creation, update, or deletion of an Object that is described in an err_msg element.
| `7016` | Object does not exist | This error indicates that the requested Path Name associated with this OperationStatus did not match any instantiated Objects. |
| `7017` | Object could not be created | This error indicates that the operation failed to create an instance of the specified Object. |
| `7018` | Object is not a table | This error indicates that the requested Path Name associated with this OperationStatus is not a Multi-Instance Object. |
| `7019` | Attempt to create non-creatable Object | This error indicates that the source endpoint attempted to create an Object that is not defined as able to be created. |
| `7020` | Object could not be updated | This error indicates that the requested Object in a Set request failed to update. |
| `7021` | Required parameter failed | This error indicates that the request failed on this Object because one or more required parameters failed to update. Details on the failed parameters are included in an associated ParamError message. |
| `7022` | Command failure | This error indicates that an command initiated in an Operate Request failed to complete for one or more reasons explained in the err_msg element. |
| `7023` | Command canceled | This error indicates that an asynchronous command initiated in an Operate Request failed to complete because it was cancelled using the Cancel() operation. |
| `7024` | Delete failure | This error indicates that this Object Instance failed to be deleted. |
| `7025` | Object exists with duplicate key | This error indicates that an Object tried to be created with a unique keys that already exist, or the unique keys were configured to those that already exist.
| `7800-7999`| Vendor defined error codes | These errors are [vendor defined](#vendor_defined_error_codes).

## Vendor Defined Error Codes

<a id="vendor_defined_error_codes" />

Implementations of USP MAY specify their own error codes for use with Errors and Responses. These codes use either the `6800-6999` series for Controller errors, or the `7800-7999` series for Agent errors, respectively. There are no requirements on the content of these errors.
