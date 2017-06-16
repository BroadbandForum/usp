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

# Set

<a id="set" />

## Selecting Objects and Parameters for CUD Operations

<a id="selecting_objects_and_parameters_CUD" />

Each Add, Set, and Delete request operates on one or more paths. For the Add request, these paths are references to Multi-Instance Objects. For all other requests, these paths can contain either addressing based identifiers that match zero or one Object or search based identifiers that matches one or more Objects.

For Add and Set requests, each Object address or search is conveyed in an element that also contains a sub-element listing the parameters to update in the matched Objects.

example, a Controller wants to disable all of the Wifi networks on an Agent. It could use a Set message with the following elements:

```
    allow_partial: true
    update_obj_list {
      obj_path: Device.Wifi.SSID.*.
      param_setting_list {
        param: Enable
        value: False
        required: False
    }
```

Assuming the Agent had three Wifi SSIDs in its associated data model, it would return:

```
    updated_obj_result_list{
      requested_path: Device.Wifi.SSID.*.
      oper_status {
        oper_success {
          updated_inst_result {
            affected path: Device.WIfi.SSID.1.
            result_param_map:
            key: Enable
            value: False
          }
          updated_inst_result {
            affected path: Device.WIfi.SSID.2.
            result_param_map:
            key: Enable
            value: False
          }
          updated_inst_result {
            affected path: Device.WIfi.SSID.3.
            result_param_map:
            key: Enable:
            value: False
          }
      }
```

### Using Allow Partial and Required Parameters

<a id="allow_partial_and_required_parameters" />

The Add, Set, and Delete requests contain an element called “`allow_partial`”. This element determines whether or not the message should be treated as one complete configuration change, or a set of individual changes, with regards to the success or failure of that configuration.

For Delete, this is straightforward - if `allow_partial` is `true`, the Agent should return a Response message with `affected_path_list` and `unaffected_path_err_list` containing the successfully deleted Objects and unsuccessfully deleted objects, respectively. If `allow_partial` is `false`, the Agent should return an Error message if any Objects fail to be deleted.

For the Add and Set messages, parameter updates contain an element called “`required`”. This details whether or not the update or creation of the Object should fail if a required parameter fails.

This creates a hierarchy of error conditions for the Add and Set requests, such as:

Parameter Error -> Object Error -> Message Error

If `allow_partial` is true, but one or more required parameters fail to be updated or configured, the creation or update of an individual Object fails. This results in an `oper_failure` in the `oper_status` element and `updated_obj_result` or `created_obj_result` returned in the Add or Set response.

If `allow_partial` is false, the failure of any required parameters will cause the update or creation of the Object to fail, which will cause the entire message to fail. In this case, the Agent returns an error message rather than a response message.

Both the `oper_failure` elements and Error messages contain an element called `param_error`, which contains elements of type `ParamError`. This is so that the Controller will receive the details of failed parameter updates regardless of whether or not the Agent returned a response message or error message.

The logic can be described as follows:

| `allow_partial`	| Required Parameters	| Required Parameter Failed	| Other Parameter Failed | 	Response/Error |	Oper_status of Object	| Contains param_error |
| -----: | :-----: | :-----: | :-----: | :-----: | :-----: | :----- |
| `True`/`False`	| No |-	|	No	| Response	| `oper_success`	| No |
| `True`/`False`	| No | - | Yes | Response | `oper_success` | Yes |
| `True`/`False` | Yes | No | No | Response | `oper_success` | No |
| `True`/`False` | Yes | No | Yes | Response | oper_success | Yes |
| `True` | Yes | Yes | - | Response | `oper_failure` | No |
| `False` | Yes | Yes | - | Error | `oper_failure` | Yes |

## Set Request Elements

`bool allow_partial`

This element tells the Agent how to process the message in the event that one or more of the Objects matched in the `obj_path` fails to update.

**R-SET.0** - If the `allow_partial` element is set to true, and no other exceptions are encountered, the Agent treats each `UpdateObject` message `obj_path` independently. The Agent MUST complete the update of valid Objects regardless of the inability to update one or more Objects (see [allow partial and required parameters](/messages/#allow_partial_and_required_parameters)).

*Note: This may cause some counterintuitive behavior if there are no required parameters to be updated. The Set Request can still result in a Set Response (rather than an Error Message) if `allow_partial` is set to true.*

**R-SET.1** - If the `allow_partial` element is set to false, and no other exceptions are encountered, the Agent treats each `UpdateObject` message `obj_path` holistically. A failure to update any one Object MUST cause the Set message to fail and return an Error message (see [allow partial and required parameters](/messages/#allow_partial_and_required_parameters)).

`repeated UpdateObject update_obj_list`

This element contains a repeated set of UpdateObject messages.

### UpdateObject Elements

`string obj_path`

This element contains an Object Path, Instance Path, or Search Path to Objects or Object Instances in the Agent’s Instantiated Data Model.

`repeated UpdateParamSetting param_setting_list`

The element contains a repeated set of `UpdatedParamSetting` messages.

#### UpdateParamSetting Elements

`string param`

This element contains the local name of a parameter of the Object specified in `obj_path`.

`string value`

This element contains the value of the parameter specified in the `param` element that the Controller would like to configure.

`bool required`

This element specifies whether the Agent should treat the update of the Object specified in `obj_path` as conditional upon the successful configuration of this parameter.

**R-SET.2** - If the `required` element is set to `true`, a failure to update this parameter MUST result in a failure to update the Object (see [allow partial and required parameters](/messages/#allow_partial_and_required_parameters)).

## Set Response

`repeated UpdatedObjectResult updated_obj_result_list`

This element contains a repeated set of `UpdatedObjectResult` messages for each `UpdateObject` message in the associated Set Request.

### UpdatedObjectResult Elements

`string requested_path`

This element returns the value of `updated_obj_result_list` in the `UpdateObject` message associated with this `UpdatedObjectResult`.

`OperationStatus oper_status`

The element contains a message of type `OperationStatus` that specifies the overall status for the update of the Object specified in `requested_path`.

#### OperationStatus Elements

`oneof oper_status`

This element contains a message of one of the following types.

`OperationFailure oper_failure`

Used when the Object specified in `requested_path` failed to be updated.

`OperationSuccess oper_success`

##### OperationFailure Elements

`fixed32 err_code`

This element contains a [numeric code](/usp/specification/error-codes/) indicating the type of error that caused the Object update to fail.

`string err_msg`

This element contains additional information about the reason behind the error.

`repeated UpdatedInstanceFailure updated_inst_failure_list`

This element contains a repeated set of messages of type `UpdatedInstanceFailure`.

###### UpdatedInstanceFailure Elements

`string affected_path`

This element returns the Object Path or Object Instance Path of the Object that failed to update.

`repeated ParameterError param_err_list`

This element contains a repeated set of `ParameterError` messages.

###### ParameterError Elements

`string param`

This element contains the Parameter Path (relative to `affected_path`) to the parameter that failed to update.

##### OperationSuccess Elements

`repeated UpdatedInstanceResult updated_inst_result_list`

This element contains a repeated set of `UpdatedInstanceResult` messages.

###### UpdatedInstanceResult Elements

`string affected_path`

This element returns the Object Path or Object Instance Path (using Instance Number Addressing) of the updated Object.

`repeated ParameterError param_err_list`

This element contains a repeated set of `ParameterError` messages.

`map<string, string> updated_param_map`

This element returns a set of key/value pairs containing a path (relative to the `affected_path`) to each of the updated Object’s parameters, their values, plus sub-Objects and their values that were updated by the Set Request.

**R-SET.3** - If the Controller does not have Read permission on any of the parameters specified in `updated_param_map`, these parameters MUST NOT be returned in this element.

**R-SET.4** - Object Instance Paths in the keys of `updated_param_map` MUST use Instance Number Addressing.

*Note: If the Set Request configured a parameter to the same value it already had, this parameter is still returned in the `updated_param_map`.*

###### ParameterError Elements

`string param`

This element contains the Parameter Path to the parameter that failed to be set.

`fixed32 err_code`

This element contains the [error code](/usp/specification/error-codes/) of the error that caused the parameter set to fail.

`string err_msg`

This element contains text related to the error specified by `err_code`.

## Set Message Supported Error Codes
Appropriate error codes for the Set message include `7000-7016`, `7020`, `7021`, and `7800-7999`.
