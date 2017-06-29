<!-- Reference Links -->
[1]:	https://github.com/BroadbandForum/usp/tree/master/data-model "TR-181 Issue 2 Device Data Model for TR-069"
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

# Add

<a id="add" />

## Selecting Objects and Parameters for CUD Operations

Each Add, Set, and Delete request operates on one or more paths. For the Add request, these paths are references to Multi-Instance Objects. For all other requests, these paths can contain either addressing based identifiers that match zero or one Object or search based identifiers that matches one or more Objects.

For Add and Set requests, each Object address or search is conveyed in an element that also contains a sub-element listing the parameters to update in the matched Objects.

The Add response contains details about the success or failure of the creation of the Object and the parameters set during its creation. In addition, it also returns those parameters that were set by the Agent upon creation of the Object.

For example, a Controller wants to create a new Wifi network on an Agent. It could use an Add message with the following elements:

    allow_partial: false
    create_obj_list {
    	obj_path: Device.Wifi.SSID.
    	param_setting_list {

    		paramparam: LowerLayers
    		value: Device.Wifi.Radio.1.
    		required: True

    		paramparam: SSID
    		value: NewSSIDName
    		required: True
    		}
    	}

The Agent’s response would include the successful Object update and the list of parameters that were set, including the default values for the Enable and Status parameters defined in [Device:2][1]:

    created_obj_result_list {
      requested_path: Device.Wifi.SSID.
      oper_status {
        oper_success {
          instantiated_path: Device.Wifi.SSID.2.
          created_param_result_map:

          key: Enable
          value: false

          key: Status
          value: Down

          key: LowerLayers
          value: : Device.Wifi.Radio.1.

          key: SSID
          value: NewSSIDName: NewSSIDName				
        }
    }

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

## Add Request Elements

`bool allow_partial`

This element tells the Agent how to process the message in the event that one or more of the Objects specified in the create_obj_list argument fails creation.

**R-ADD.0** - If the `allow_partial` element is set to `true`, and no other exceptions are encountered, the Agent treats each Object matched in `obj_path` independently. The Agent MUST complete the creation of valid Objects regardless of the inability to create or update one or more Objects (see [allow partial and required parameters](/messages/#allow_partial_and_required_parameters)).

**R-ADD.1** - If the `allow_partial` element is set to `false`, and no other exceptions are encountered, the Agent treats each Object matched in `obj_path` holistically. A failure to create any one Object MUST cause the Add message to fail and return an `Error` Message (see [allow partial and required parameters](/messages/#allow_partial_and_required_parameters)).

`repeated CreateObject create_obj_list`

This element contains a repeated set of CreateObject elements.

### CreateObject Elements

`string obj_path`

This element contains an Object Path to a writeable Table in the Agent’s Instantiated Data Model.

**R-ADD.2** - The `obj_path` element in the `CreateObject` message of an Add Request MUST NOT contain Search Paths.

`repeated CreateParamSetting param_setting_list`

This element contains a repeated set of CreateParamSetting elements.

#### CreateParamSetting Elements

`string param`

This element contains a relative path to a parameter of the Object specified in `obj_path`, or a parameter of a single instance sub-object of the Object specified in `obj_path`.

`string value`

This element contains the value of the parameter specified in the `param` element that the Controller would like to configure as part of the creation of this Object.

`bool required`

This element specifies whether the Agent should treat the creation of the Object specified in `obj_path` as conditional upon the successful configuration of this parameter (see [allow partial and required parameters](/messages/#allow_partial_and_required_parameters)).

**R-ADD.3** - If the `required` element is set to true, a failure to update this parameter MUST result in a failure to create the Object.

## Add Response Elements

`repeated CreatedObjectResult created_obj_result_list`

A repeated set of `CreatedObjectResult` elements for each `CreateObject` element in the Add message.

### CreatedObjectResult Elements

`string requested_path`

This element returns the value of `obj_path_list` in the `CreateObject` message associated with this `CreatedObjectResult`.

`OperationStatus oper_status`

The element contains a message of type `OperationStatus` that specifies the overall status for the creation of the Object specified in `requested_path`.

#### OperationStatus Elements

`oneof oper_status`

This element contains one of the types given below. Each indicates that the element contains a message of the given type.

`OperationFailure oper_failure`

This message is used when the object given in `requested_path` failed to be created.

`OperationSuccess oper_success`

##### OperationFailure Elements

`fixed32 err_code`

This element contains a [numeric code](/usp/specification/messages/error-codes/) indicating the type of error that caused the Object creation to fail. A value of 0 indicates the Object was created successfully.

`string err_msg`

This element contains additional information about the reason behind the error.

##### Operation Success Elements

`string instantiated_path`

This element contains the Object Instance Path (using Instance Number Addressing) of the created Object.

`repeated ParameterError param_err_list`

This element returns a repeated set of ParameterError messages.

**R-ADD.4** - If any of the parameters and values specified in the `param_setting_list` element fail to configure upon creation, this set MUST include one element describing each of the failed parameters and the reason for their failure.

`map<string, string> unique_key_map`

This element contains a map of the local name and value for each supported parameter that is part of any of this Object's unique keys.

**R-ADD.5** - If the Controller did not include some or all of a unique key that the Agent supports in the `param_setting_list` element, the Agent MUST assign values to the unique key(s) and return them in the `unique_key_map`.

**R-ADD.6** - If the Controller does not have Read permission on any of the parameters specified in `unique_key_map`, these parameters MUST NOT be returned in this element.

###### ParameterError Elements

`string param`

This element contains the Relative Parameter Path to the parameter that failed to be set.

`fixed32 err_code`

This element contains the [error code](/usp/specification/error-codes/) of the error that caused the parameter set to fail.

`string err_msg`

This element contains text related to the error specified by `err_code`.

## Add Message Supported Error Codes

Appropriate error codes for the Add message include `7000-7019` and `7800-7999`.

[<-- Messages](/usp/specification/messages/)
[The Delete Message -->](/usp/specification/messages/delete/)
