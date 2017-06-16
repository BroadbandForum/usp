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

# Delete

<a id="delete" />

## Delete Request Elements

`bool allow_partial`

This element tells the Agent how to process the message in the event that one or more of the Objects specified in the `obj_path` argument fails deletion.

**R-DEL.0** - If the `allow_partial` element is set to true, and no other exceptions are encountered, the Agent treats each entry in `obj_path` independently. The Agent MUST complete the deletion of valid Objects regardless of the inability to delete one or more Objects (see [allow partial and required parameters](/usp/specification/messages/add/#allow_partial_and_required_parameters)).

**R-DEL.1** - If the `allow_partial` element is set to false, and no other exceptions are encountered, the Agent treats each entry in `obj_path` holistically. A failure to delete any one Object MUST cause the Delete message to fail and return an Error message (see [allow partial and required parameters](/usp/specification/messages/add/#allow_partial_and_required_parameters)).

`repeated string obj_path_list`

This element contains a repeated set of Object Instance Paths or Search Paths.

## Delete Response Elements

`repeated DeletedObjectResult deleted_obj_result_list`

This element contains a repeated set of `DeletedObjectResult` messages.

### DeletedObjectResult Elements

`string requested_path`

This element returns the value of the entry of `obj_path_list` (in the Delete Request) associated with this `DeleteObjectResult`.

`OperationStatus oper_status`

This element contains a message of type `OperationStatus`.

#### OperationStatus Elements

`oneof oper_status`

This element contains a message of one of the following types.

`OperationFailure oper_failure`

Used when the Object specified in `requested_path` failed to be deleted.

`OperationSuccess oper_success`

##### OperationFailure Elements

*Note: Since the `OperationSuccess` message of the Delete Response contains an `unaffected_path_err_list`, the `OperationStatus` will only contain an `OperationFailure` message if the `requested_path` was did not match any existing Objects (error `7016`) or was syntactically incorrect (error `7008`).*

`fixed32 err_code`

This element contains a [numeric code](/usp/specification/error-codes/) indicating the type of error that caused the delete to fail. A value of 0 indicates the Object was deleted successfully.

`string err_msg`

This element contains additional information about the reason behind the error.

##### OperationSuccess Elements

`repeated string affected_path_list`

This element returns a repeated set of Path Names to Object Instances.

**R-DEL.2** - If the Controller does not have Read permission on any of the Objects specified in `affected_path_list`, these Objects MUST NOT be returned in this element.

**R-DEL.3** - The Path Names to Object Instances in `affected_path_list` MUST be addressed using Instance Number Addressing.

`repeated UnaffectedPathError unaffected_path_err_list`

This element contains a repeated set of messages of type `UnaffectedPathError`.

**R-DEL.4** - If any of the Object Instances specified in the `obj_path_list` element fail to delete, this set MUST include one `UnaffectedPathError` message for each of the Object Instances that failed to Delete.

**R-DEL.5** - If the Controller does not have Read permission on any of the Objects specified in `unaffected_path_list`, these Objects MUST NOT be returned in this element.

###### UnaffectedPathError Elements

`string unaffected_path`

This element returns the Path Name to the Object Instance that failed to be deleted.

**R-DEL.6** - The Path Names to Object Instances in `unaffected_path` MUST be addressed using Instance Number Addressing.

`fixed32 err_code`

This element contains the error code of the error that caused the deletion of this object to fail.

`string err_msg`

This element contains text related to the error specified by `err_code`.

## Delete Message Supported Error Codes

Appropriate error codes for the Delete message include `7000-7008`, `7015`, `7016`, `7018`, `7024`, and `7800-7999`.
