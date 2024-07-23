# Messages

USP contains messages to create, read, update, and delete Objects, perform Object-defined operations, and allow Agents to notify controllers of events. This is often referred to as CRUD with the addition of O (operate) and N (notify), or CRUD-ON.

*Note: This version of the specification defines its Messages in [Protocol Buffers v3](#sec:encoding). This part of the specification may change to a more generic description (normative and non-normative) if further encodings are specified in future versions.*

These sections describe the types of USP Messages and the normative requirements for their flow and operation. USP Messages are described in a protocol buffers schema, and the normative requirements for the individual fields of the schema are outlined below.

## Encapsulation in a USP Record

All USP Messages are encapsulated by a USP Record. The definition of the USP Record portion of a USP Message can be found in [](#sec:record-definition), and the rules for managing transactional integrity are described in [](#sec:e2e-message-exchange).

## Requests, Responses and Errors

The three types of USP Messages are Request, Response, and Error.

A request is a Message sent from a source USP Endpoint to a target USP Endpoint that includes fields to be processed and returns a response or error. Unless otherwise specified, all requests have an associated response. Though the majority of requests are made from a Controller to an Agent, the Notify and Register Messages follow the same format as a request but is sent from an Agent to a Controller.

**[R-MSG.0]{}** - The target USP Endpoint MUST respond to a request Message from the source USP Endpoint with either a response Message or Error Message, unless otherwise specified (see [](#sec:operate) and [](#sec:notify)).

**[R-MSG.0a]{}** - The associated response or error Message MUST be sent through the same type of USP Record (i.e. A `record_type` of [`session_context`](#sec:exchange-of-usp-records-within-an-e2e-session-context) or [`no_session_context`](#sec:exchange-of-usp-records-without-an-e2e-session-context)) used along the associated request Message.

**[R-MSG.1]{}** - The target USP Endpoint MUST ignore or send an Error Message in response to Messages it does not understand.

*Note: Requirement R-MSG.2 was removed in USP 1.2, because it did not align with the concept of brokered MTPs and long-lived connections in general.*

**[R-MSG.3]{}** - In any USP Message originating from an Agent, unless otherwise specified, Path Names reported from the Agent's Instantiated Data Model MUST use Instance Number Addressing.

### Handling Duplicate Messages

Circumstances may arise (such as multiple Message Transfer Protocols) that cause duplicate Messages (those with an identical Message ID) to arrive at the target USP Endpoint.

**[R-MSG.4]{}** - If a target USP Endpoint receives a Message with a duplicate Message ID before it has processed and sent a Response or Error to the original Message, it MUST gracefully ignore the duplicate Message.

For Messages that require no response, it is up to the target Endpoint implementation when to allow the same Message ID to be re-used by the same source USP Endpoint.

### Handling Search Expressions

Many USP Messages allow for search expressions to be used in the request. To
help make Controller requests more flexible, it is desired that requests using
search expressions that match zero Objects should receive a successful
response. In these cases, the Agent is in the desired state the Controller
intends, and the result should not interrupt the Controller's application.

In the Messages below, this requirement is sometimes explicit, but it is stated here as a general requirement.

**[R-MSG.4a]{}** - Unless otherwise specified, if a Request contains a
Search Path, the associated Response MUST result in a successful operation
with an empty element (i.e. `oper_success{}`) if the Search Path matches zero
Objects in the Agent's Instantiated Data Model.

### Example Message Flows

Successful request/response: In this successful Message sequence, a Controller sends an Agent a request. The Message header and body are parsed, the Message is understood, and the Agent sends a response with the relevant information in the body.

*Note: this is not meant to imply that all request/response operations will be synchronous. Controllers can and should expect that Responses may be received in a different order than that in which Requests were made.*

![A successful request/response sequence](successful_response.png)

Failed request/response: In this failed Message sequence, a Controller sends an Agent a request. The Message header and body are parsed, but the Agent throws an error. The error arguments are generated and sent in an Error Message.

![A failed request/response sequence](error_response.png)

## Message Structure

A Message consists of a header and body. When using Protocol Buffers [@PROTOBUF], the fields of the header and body for different Messages are defined in a schema and sent in an encoded format from one USP Endpoint to another.

**[R-MSG.5]{}** - A Message MUST conform to the schemas defined in [%usp-msg-proto-file%](%usp-msg-proto-url%).

*See the section on [USP Record Encapsulation](#sec:usp-record-encapsulation) for information about Protocol Buffers default behavior and required fields.*

Every USP Message contains a header and a body. The header contains basic destination and coordination information, and is separated to allow security and discovery mechanisms to operate. The body contains the message itself and its arguments.

Each of the Message types and fields below are described with the field type according to Protocol Buffers [@PROTOBUF], followed by its name.

### The USP Message

`Header header`

**[R-MSG.6]{}** - A Message MUST contain exactly one header field.

`Body body`

The Message Body that must be present in every Message.  The Body field contains either a Request, Response, or Error field.

**[R-MSG.7]{}** - A Message MUST contain exactly one body field.

### Message Header

The Message Header includes a Message ID to associate Requests with Responses or Errors, and a field indicating the type of Message.

The purpose of the Message Header is to provide basic information necessary for the target Endpoint to process the message.

#### Message Header Fields

`string msg_id`

A locally unique opaque identifier assigned by the Endpoint that generated this Message.

**[R-MSG.8]{}** - The msg_id field MUST be present in every Header.

**[R-MSG.9]{}** - The msg_id field in the Message Header for a Response or Error that is associated with a Request MUST contain the Message ID of the associated request. If the msg_id field in the Response or Error does not contain the Message ID of the associated Request, the response or error MUST be ignored.

`enum MsgType msg_type`

This field contains an enumeration indicating the type of message contained in the Message body. It is an enumeration of:
```
    ERROR (0)
    GET (1)
    GET_RESP (2)
    NOTIFY (3)
    SET (4)
    SET_RESP (5)
    OPERATE (6)
    OPERATE_RESP (7)
    ADD (8)
    ADD_RESP (9)
    DELETE (10)
    DELETE_RESP (11)
    GET_SUPPORTED_DM (12)
    GET_SUPPORTED_DM_RESP (13)
    GET_INSTANCES (14)
    GET_INSTANCES_RESP (15)
    NOTIFY_RESP (16)
    GET_SUPPORTED_PROTO (17)
    GET_SUPPORTED_PROTO_RESP (18)
    REGISTER (19)
    REGISTER_RESP (20)
    DEREGISTER (21)
    DEREGISTER_RESP (22)
```

**[R-MSG.10]{}** - The `msg_type` field MUST be present in every Header. Though
required, it is meant for information only. In the event this field differs
from the `req_type` or `resp_type` in the Message body (respectively), the
type given in either of those elements SHOULD be regarded as correct.

### Message Body

The Message body contains the intended message and the appropriate fields for the Message type.

Every Message body contains exactly one message and its fields. When an Agent is the target Endpoint, these messages can be used to create, read, update, and delete Objects, or execute Object-defined operations. When a Controller is the target Endpoint, the Message will contain a notification, response, or an error.

#### Message Body Fields

`oneof msg_body`

This field contains one of the types given below:

`Request request`

This field indicates that the Message contains a request of a type given in the Request Message.

`Response response`

This field indicates that the Message contains a response of a type given in the Response Message.

`Error	error`

This field indicates that the Message contains an Error Message.

#### Request Fields

`oneof req_type`

This field contains one of the types given below. Each indicates that the Message contains a Message of the given type.

```
    Get get
    GetSupportedDM get_supported_dm
    GetInstances get_instances
    Set set
    Add add
    Delete delete
    Operate operate
    Notify notify
    GetSupportedProtocol get_supported_protocol
    Register register
    Deregister deregister
```

#### Response Fields

`oneof resp_type`

This field contains one of the types given below. Each indicates that the Message contains a Message of the given type.

```
    GetResp get_resp
    GetSupportedDMResp get_supported_dm_resp
    GetInstancesResp get_instances_resp
    SetResp set_resp
    AddResp add_resp
    DeleteResp delete_resp
    OperateResp operate_resp
    NotifyResp notify_resp
    GetSupportedProtocolResp get_supported_protocol_resp
    RegisterResp register_resp
    DeregisterResp deregister_resp
```

#### Error Fields

`fixed32 err_code`

This field contains a numeric code (see [](#sec:error-codes)) indicating the type of error that caused the overall Message to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

`repeated ParamError param_errs`

This field is present in an Error Message in response to an Add, Set, or Delete Message when the `allow_partial` field is false and detailed error information is available for each Object or Parameter that have caused the Message to report an Error.

##### ParamError Fields

`string param_path`

This field contains a Path Name to the Object or Parameter that caused the error.

`fixed32 err_code`

This field contains a numeric code (see [](#sec:error-codes)) indicating the type of error that caused the Message to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

## Creating, Updating, and Deleting Objects

The [Add](#sec:add), [Set](#sec:set), and [Delete](#sec:delete) requests are used to create, configure and remove Objects that comprise Service fields.

### Selecting Objects and Parameters

Each Add, Set, and Delete request operates on one or more Path Names. For the Add request, these Path Names are references to Multi-Instance Objects. For all other requests, these Path Names can contain either addressing based identifiers that match zero or one Object or search based identifiers that matches one or more Objects.

For Add and Set requests, each Object address or search is conveyed in a field that also contains a sub-field listing the Parameters to update in the matched Objects.

The Add response contains details about the success or failure of the creation of the Object and the Parameters set during its creation. In addition, it also returns those Parameters that were set by the Agent upon creation of the Object.

Note: The order of the data on the wire is not guaranteed to be in the order an implementation may require to process a `Message` piece by piece. Some common scenarios which an Agent will need to handle:

- In Objects containing a union Object, the union member Object will only exist after the discriminator Parameter was set to the associated value
- Key Parameters need only to have unique values after the whole Message has been processed
- All explicit and hidden data dependencies need to be accounted for, so if related Parameters are changed, the order in which they occur in the Message do not make any difference to the outcome

For example, a Controller wants to create a new Wi-Fi network on an Agent. It could use an Add Message with the following fields:

```{filter=pbv type=Request}
    add {
      allow_partial: false
      create_objs {
        obj_path: "Device.WiFi.SSID."
        param_settings {
          param: "LowerLayers"
          value: "Device.WiFi.Radio.1."
          required: true
        }
        param_settings {
          param: "SSID"
          value: "NewSSIDName"
          required: true
        }
      }
    }
```

The Agent’s response would include the Object created (with its instance identifier) and the Unique Key Parameters of the created Object as defined in the Device:2 Data Model [@TR-181]:

```{filter=pbv type=Response}
    add_resp {
      created_obj_results {
        requested_path: "Device.WiFi.SSID."
        oper_status {
          oper_success {
            instantiated_path: "Device.WiFi.SSID.4."
            unique_keys {
              key: "BSSID"
              value: "112233445566"
            }
            unique_keys {
              key: "Name"
              value: "GuestNetwork1"
            }
            unique_keys {
              key: "Alias"
              value: "cpe-alias-1"
            }
          }
        }
      }
    }
```
### Unique Key Immutability

In order to maintain addressing integrity of Multi-Instance Objects, the following prescriptions are made on the use of Unique Keys.

**[R-KEY.1]{}** - Non-functional Unique Keys (as defined in TR-106 [@TR-106]) MUST NOT change in the Agent's Instantiated Data Model after creation, as defined in [R-ADD.5]().

**[R-KEY.2]{}** - Functional Unique Keys (as defined in TR-106 [@TR-106]) MAY change incidentally as part of normal operation, but any change MUST abide by the uniqueness rules (i.e., no conflict with other instances).

### writeOnceReadOnly Parameter Access

There are several parameter access types defined in [@TR-106] that specify what a Controller is allowed to do with 
a particular Parameter as defined in [@TR-181]. Of these, `writeOnceReadOnly` affects the response of an Agent in 
specific ways. A `writeOnceReadOnly` Parameter can be set only once by a Controller, and then becomes 
read-only. In some cases, the value is assigned by the Agent upon Object creation if not specified by the Controller.
The expected behavior is otherwise as follows:

- When a `writeOnceReadyOnly` Parameter is set upon Object creation via the `Add` Message, the Controller making the 
Add Request is considered to have set the Parameter.
- When a `writeOnceReadOnly` Parameter is updated via a `Set` Message, an Agent will reject the update if the 
Parameter has already been set.
- `writeOnceReadyOnly` Parameters are reported as `PARAM_READ_WRITE (1)` in a `GetSupportedDM` Response. Controllers 
should rely on knowledge of the Agent's data model through other means (i.e., officially published data models) 
to determine that a parameter is `writeOnceReadOnly`.

### Using Allow Partial and Required Parameters {#sec:using-allow-partial-and-required-parameters}

The Add, Set, and Delete requests contain a field called "`allow_partial`". This field determines whether or not the Message should be treated as one complete configuration change, or a set of individual changes, with regards to the success or failure of that configuration.

For Delete, this is straightforward - if `allow_partial` is `true`, the Agent returns a Response Message with `affected_paths` and `unaffected_path_errs` containing the successfully deleted Objects and unsuccessfully deleted Objects, respectively. If `allow_partial` is `false`, the Agent will return an Error Message if any Objects fail to be deleted.

For the Add and Set Messages, Parameter updates contain a field called "`required`". This details whether or not the update or creation of the Object should fail if a required Parameter fails.

This creates a hierarchy of error conditions for the Add and Set requests, such as:

Parameter Error -> Object Error -> Message Error

If `allow_partial` is true, but one or more required Parameters fail to be updated or configured, the creation or update of a requested Path Name fails. This results in an `oper_failure` in the `oper_status` field and `updated_obj_result` or `created_obj_result` returned in the Add or Set response.

If `allow_partial` is false, the failure of any required Parameters will cause the update or creation of the Object to fail, which will cause the entire Message to fail. In this case, the Agent returns an Error Message rather than a response Message.

*Note: It is up to the individual implementation whether to abort and return an
Error Message after the first error, or provide information about multiple
failures.*

If the Message was at least partially successful, the response will make use of the `oper_success` field to indicate the successfully affected Objects.

The `oper_failure` and `oper_success` fields as well as Error Messages contain a field called `param_errs`, which contains fields of type `ParameterError` or `ParamError`. This is so that the Controller will receive the details of failed Parameter updates regardless of whether or not the Agent returned a Response or Error Message.

The logic can be described as follows:

| `allow_partial`	| Required Parameters	| Required Parameter Failed	| Other Parameter Failed | 	Response/Error |	Oper_status of Object	| Contains param_errs |
| -----: | :-----: | :-----: | :-----: | :-----: | :-----: | :----- |
| `true`/`false`	| No |-	|	No	| Response	| `oper_success`	| No |
| `true`/`false`	| No | - | Yes | Response | `oper_success` | Yes |
| `true`/`false` | Yes | No | No | Response | `oper_success` | No |
| `true`/`false` | Yes | No | Yes | Response | `oper_success` | Yes |
| `true` | Yes | Yes | - | Response | `oper_failure` | Yes |
| `false` | Yes | Yes | - | Error | N/A | Yes |

#### Search Paths and allow_partial in Set {#sec:search-paths-in-set}

In a Set Request that specifies a Search Path that matches multiple objects, it is intended that the Agent treats the requested path holistically regardless of the value of allow_partial. This represents a special case. Information about the failure reason for any one or more objects that failed to be created or updated is still desired, but would be lost if an Error message was returned rather than a Response message containing OperationFailure elements. See [R-SET.2a]() and [R-SET.2b]() for the specific requirements.

### The Add Message {#sec:add}

The Add Message is used to create new Instances of Multi-Instance Objects in the Agent's Instantiated Data Model.

#### Add Example

In this example, the Controller requests that the Agent create a new instance in the `Device.LocalAgent.Controller` table.

```{filter=pbv}
header {
  msg_id: "52867"
  msg_type: ADD
}
body {
  request {
    add {
      allow_partial: true
      create_objs {
        obj_path: "Device.LocalAgent.Controller."
        param_settings {
          param: "Enable"
          value: "true"
          required: false
        }
        param_settings {
          param: "EndpointID"
          value: "controller-temp"
          required: false
        }
      }
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "52867"
  msg_type: ADD_RESP
}
body {
  response {
    add_resp {
      created_obj_results {
        requested_path: "Device.LocalAgent.Controller."
        oper_status {
          oper_success {
            instantiated_path: "Device.LocalAgent.Controller.3."
            unique_keys {
              key: "EndpointID"
              value: "controller-temp"
            }
            unique_keys {
              key: "Alias"
              value: "cpe-alias-3"
            }
          }
        }
      }
    }
  }
}
```

#### Add Request Fields

`bool allow_partial`

This field tells the Agent how to process the Message in the event that one or more of the Objects specified in the `create_objs` argument fails creation.

**[R-ADD.0]{}** - If the `allow_partial` field is set to `true`, and no other exceptions are encountered, the Agent treats each Object matched in `obj_path` independently. The Agent MUST complete the creation of valid Objects regardless of the inability to create or update one or more Objects (see [](#sec:using-allow-partial-and-required-parameters)).

**[R-ADD.1]{}** - If the `allow_partial` field is set to `false`, and no other exceptions are encountered, the Agent treats each Object matched in `obj_path` holistically. A failure to create any one Object MUST cause the Add Message to fail and return an `Error` Message (see [](#sec:using-allow-partial-and-required-parameters)).

`repeated CreateObject create_objs`

This field contains a repeated set of CreateObject fields.

##### CreateObject Fields

`string obj_path`

This field contains an Object Path to a writeable Table in the Agent’s Instantiated Data Model.

**[R-ADD.2]{}** - The `obj_path` field in the `CreateObject` Message of an Add Request MUST specify or match exactly one Object Path. (DEPRECATED)

*Note: The R-ADD.2 requirement was deprecated in USP 1.3 because previous USP versions too narrowly restricted the usage of various paths in the obj_path field. If multiple paths are impacted, then the AddResp can contain multiple CreatedObjectResult instances that include the same requested_path.*

`repeated CreateParamSetting param_settings`

This field contains a repeated set of CreateParamSetting fields.

###### CreateParamSetting Fields

`string param`

This field contains a Relative Path to a Parameter of the Object specified in `obj_path`, or  any Parameter in a nested tree of single instance Sub-Objects of the Object specified in `obj_path`.

*Note: The Parameters that can be set in an Add Message are still governed by the permissions allowed to the Controller. Should a Controller attempt to create an Object when it does not have permission on one or more Parameters of that Object, the expected behavior is as follows:*

- *If the Add Message omits Parameters for which the Controller does not have write permission, those parameters will be set to their default (if any) by the Agent, and the Add Message succeeds.*

- *If the Add Message includes Parameters for which the Controller does not have write permission, the Message proceeds in accordance with the rules for allow_partial and required parameters.*

`string value`

This field contains the value of the Parameter specified in the `param` field that the Controller would like to configure as part of the creation of this Object.
Refer to [](#sec:parameter-value-encoding) for details of how Parameter values are encoded as Protocol Buffers v3 strings.

`bool required`

This field specifies whether the Agent should treat the creation of the Object specified in `obj_path` as conditional upon the successful configuration of this Parameter (see [](#sec:using-allow-partial-and-required-parameters)).

*Note: Any Unique Key Parameter contained in the Add Message will be considered as required regardless of how this field is set. This is to ensure that Unique Key constraints are met when creating the instance of the Object.*

**[R-ADD.2a]{}** - If the `allow_partial` field is set to `false` and and the `obj_path` field contains a Search Expression, a failure in any of the Paths matched by the Search Expression MUST result in a failure and the state of the Data Model MUST NOT change.

**[R-ADD.3]{}** - If the `required` field is set to true, a failure to update this Parameter MUST result in a failure to create the Object.

#### Add Response Fields

`repeated CreatedObjectResult created_obj_results`

A repeated set of `CreatedObjectResult` fields for each `CreateObject` field in the Add Message.

##### CreatedObjectResult Fields

`string requested_path`

This field returns the value of `obj_paths` in the `CreateObject` Message associated with this `CreatedObjectResult`.

`OperationStatus oper_status`

The field contains a Message of type `OperationStatus` that specifies the overall status for the creation of the Object specified in `requested_path`.

###### OperationStatus Fields

`oneof oper_status`

This field contains one of the types given below. Each indicates that the field contains a Message of the given type.

`OperationFailure oper_failure`

Used when the Object given in `requested_path` failed to be created.

`OperationSuccess oper_success`

Used when the `Add` Message was (at least partially) successful.

###### OperationFailure Fields

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the Object creation to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

###### Operation Success Fields

`string instantiated_path`

This field contains the Object Instance Path of the created Object.

`repeated ParameterError param_errs`

This field returns a repeated set of ParameterError messages.

**[R-ADD.4]{}** - If any of the Parameters and values specified in the `param_settings` field fail to configure upon creation, this set MUST include one field describing each of the failed Parameters and the reason for their failure.

`map<string, string> unique_keys`

This field contains a map of the Relative Path and value for all of this Object's Unique Key Parameters that are supported by the Agent.

**[R-ADD.5]{}** - If the Controller did not include some or all of the Unique Key Parameters that are supported by the Agent in the `param_settings` field, the Agent MUST assign values to these Parameters and return them in the `unique_keys` field.

**[R-ADD.6]{}** - If the Controller does not have Read permission on any of the Parameters returned in `unique_keys`, these Parameters MUST NOT be returned in this field.

###### ParameterError Fields

`string param`

This field contains the Relative Parameter Path to the Parameter that failed to be set.

`fixed32 err_code`

This field contains the numeric code ([](#sec:error-codes)) of the error that caused the Parameter set to fail.

`string err_msg`

This field contains text related to the error specified by `err_code`.

#### Add Message Supported Error Codes

Appropriate error codes for the Add Message include `7000-7019`, `7026`, and `7800-7999`.

### The Set Message {#sec:set}

The Set Message is used to update the Parameters of existing Objects in the Agent's Instantiated Data Model.

#### Set Example

In this example the Controller requests that the Agent change the value of the `FriendlyName` Parameter in the `Device.DeviceInfo.` Object.

```{filter=pbv}
header {
  msg_id: "19220"
  msg_type: SET
}
body {
  request {
    set {
      allow_partial: true
      update_objs {
        obj_path: "Device.DeviceInfo."
        param_settings {
          param: "FriendlyName"
          value: "MyDevicesFriendlyName"
          required: true
        }
      }
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "19220"
  msg_type: SET_RESP
}
body {
  response {
    set_resp {
      updated_obj_results {
        requested_path: "Device.DeviceInfo."
        oper_status {
          oper_success {
            updated_inst_results {
              affected_path: "Device.DeviceInfo."
              updated_params {
                key: "FriendlyName"
                value: "MyDevicesFriendlyName"
              }
            }
          }
        }
      }
    }
  }
}
```

#### Set Request Fields

`bool allow_partial`

This field tells the Agent how to process the Message in the event that one or more of the Objects matched in the `obj_path` fails to update.

**[R-SET.0]{}** - If the `allow_partial` field is set to true, and no other exceptions are encountered, the Agent treats each `UpdateObject` message `obj_path` independently. The Agent MUST complete the update of valid Objects regardless of the inability to update one or more Objects (see [](#sec:using-allow-partial-and-required-parameters)).

*Note: This may cause some counterintuitive behavior if there are no required Parameters to be updated. The Set Request can still result in a Set Response (rather than an Error Message) if `allow_partial` is set to true.*

**[R-SET.1]{}** - If the `allow_partial` field is set to false, and no other exceptions are encountered, the Agent treats each `UpdateObject` message `obj_path` holistically. A failure to update any one Object MUST cause the Set Message to fail and return an Error Message (see [](#sec:using-allow-partial-and-required-parameters)).

`repeated UpdateObject update_objs`

This field contains a repeated set of UpdateObject messages.

##### UpdateObject Fields

`string obj_path`

This field contains an Object Path, Object Instance Path, or Search Path to Objects or Object Instances in the Agent’s Instantiated Data Model.

`repeated UpdateParamSetting param_settings`

The field contains a repeated set of `UpdatedParamSetting` messages.

###### UpdateParamSetting Fields

`string param`

This field contains the Relative Path of a Parameter of the Object specified in `obj_path`.

`string value`

This field contains the value of the Parameter specified in the `param` field that the Controller would like to configure.
Refer to [](#sec:parameter-value-encoding) for details of how Parameter values are encoded as Protocol Buffers v3 strings.

`bool required`

This field specifies whether the Agent should treat the update of the Object specified in `obj_path` as conditional upon the successful configuration of this Parameter.

**[R-SET.2]{}** - If the `required` field is set to `true`, a failure to update this Parameter MUST result in a failure to update the Object (see [](#sec:using-allow-partial-and-required-parameters)).

**[R-SET.2a]{}** - If the `obj_path` field in the `UpdateObject` message of a Set Request contains a Search Path matching more than one object, the Agent MUST treat the results of that `obj_path` holistically, regardless of the value of the `allow_partial` field. That is, if any object that matches the Search Path fails to be updated due to an error, the Agent MUST undo any changes that were already processed due to this `obj_path`, and the Agent MUST return a Set Response with an UpdatedObjectResult containing:

  * A `requested_path` equal to the `obj_path` in the request.
  * An `oper_status` field containing an OperationFailure message.
  * At least one UpdatedInstanceFailure message with an `affected_path` that reflects the object that failed to update.

**[R-SET.2b]{}** - The Agent MAY terminate processing a Set Request with an `obj_path` field in the `UpdateObject` message that contains a Search Path matching more than one object after encountering any number of errors.

#### Set Response

`repeated UpdatedObjectResult updated_obj_results`

This field contains a repeated set of `UpdatedObjectResult` messages for each `UpdateObject` message in the associated Set Request.

##### UpdatedObjectResult Fields

`string requested_path`

This field returns the value of `updated_obj_results` in the `UpdateObject` message associated with this `UpdatedObjectResult`.

`OperationStatus oper_status`

The field contains a message of type `OperationStatus` that specifies the overall status for the update of the Object specified in `requested_path`.

###### OperationStatus Fields

`oneof oper_status`

This field contains a message of one of the following types.

`OperationFailure oper_failure`

Used when the Object specified in `requested_path` failed to be updated.

`OperationSuccess oper_success`

Used when the `Set` message was (at least partially) successful.

###### OperationFailure Fields

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the Object update to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

`repeated UpdatedInstanceFailure updated_inst_failures`

This field contains a repeated set of messages of type `UpdatedInstanceFailure`.

###### UpdatedInstanceFailure Fields

`string affected_path`

This field returns the Object Path or Object Instance Path of the Object that failed to update.

`repeated ParameterError param_errs`

This field contains a repeated set of `ParameterError` messages.

###### ParameterError Fields

`string param`

This field contains the Relative Parameter Path to the Parameter that failed to be set.

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the Parameter set to fail.

`string err_msg`

This field contains text related to the error specified by `err_code`.

###### OperationSuccess Fields

`repeated UpdatedInstanceResult updated_inst_results`

This field contains a repeated set of `UpdatedInstanceResult` messages.

###### UpdatedInstanceResult Fields

`string affected_path`

This field returns the Object Path or Object Instance Path of the updated Object.

`repeated ParameterError param_errs`

This field contains a repeated set of `ParameterError` messages.

`map<string, string> updated_params`

This field returns a set of key/value pairs containing a Relative Parameter Path (relative to the `affected_path`) to each of the Parameters updated by the Set Request and its value after the update.
Refer to [](#sec:parameter-value-encoding) for details of how Parameter values are encoded as Protocol Buffers v3 strings.

**[R-SET.3]{}** - If the Controller does not have Read permission on any of the Parameters specified in `updated_params`, these Parameters MUST NOT be returned in this field.

*Note: If the Set Request configured a Parameter to the same value it already had, this Parameter is still returned in the `updated_params`.*

###### ParameterError Fields

`string param`

This field contains the Parameter Path to the Parameter that failed to be set.

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the Parameter set to fail.

`string err_msg`

This field contains text related to the error specified by `err_code`.

#### Set Message Supported Error Codes
Appropriate error codes for the Set Message include `7000-7016`, `7020`, `7021`, `7026`, and `7800-7999`.

### The Delete Message {#sec:delete}

The Delete Message is used to remove Instances of Multi-Instance Objects in the Agent's Instantiated Data Model.

#### Delete Example

In this example, the Controller requests that the Agent remove the instance in
`Device.LocalAgent.Controller` table that has the EndpointID value of "`controller-temp`".

```{filter=pbv}
header {
  msg_id: "24799"
  msg_type: DELETE
}
body {
  request {
    delete {
      allow_partial: false
      obj_paths: 'Device.LocalAgent.Controller.[EndpointID=="controller-temp"].'
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "24799"
  msg_type: DELETE_RESP
}
body {
  response {
    delete_resp {
      deleted_obj_results {
        requested_path: 'Device.LocalAgent.Controller.[EndpointID=="controller-temp"].'
        oper_status {
          oper_success {
            affected_paths: "Device.LocalAgent.Controller.31185."
          }
        }
      }
    }
  }
}
```

#### Delete Request Fields

`bool allow_partial`

This field tells the Agent how to process the Message in the event that one or more of the Objects specified in the `obj_path` argument fails deletion.

**[R-DEL.0]{}** - If the `allow_partial` field is set to true, and no other exceptions are encountered, the Agent treats each entry in `obj_path` independently. The Agent MUST complete the deletion of valid Objects regardless of the inability to delete one or more Objects (see [](#sec:using-allow-partial-and-required-parameters)).

**[R-DEL.1]{}** - If the `allow_partial` field is set to false, the Agent treats each entry in `obj_path` holistically. Any entry referring to an Object which is non-deletable or doesn't exist in the supported data model MUST cause the Delete Message to fail and return an Error Message.

`repeated string obj_paths`

This field contains a repeated set of Object Instance Paths or Search Paths.

#### Delete Response Fields

`repeated DeletedObjectResult deleted_obj_results`

This field contains a repeated set of `DeletedObjectResult` messages.

##### DeletedObjectResult Fields

`string requested_path`

This field returns the value of the entry of `obj_paths` (in the Delete Request) associated with this `DeleteObjectResult`.

`OperationStatus oper_status`

This field contains a message of type `OperationStatus`.

###### OperationStatus Fields

`oneof oper_status`

This field contains a message of one of the following types.

`OperationFailure oper_failure`

Used when the Object specified in `requested_path` failed to be deleted.

`OperationSuccess oper_success`

Used when the `Delete` Message was (at least partially) successful.

###### OperationFailure Fields

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the delete to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

###### OperationSuccess Fields

`repeated string affected_paths`

This field returns a repeated set of Path Names to Object Instances.

**[R-DEL.2]{}** - If the Controller does not have Read permission on any of the Objects specified in `affected_paths`, these Objects MUST NOT be returned in this field.

**[R-DEL.2a]{}** - If the requested_path was valid (i.e., properly formatted and in the Agent's supported data model) but did not resolve to any Objects in the Agent's instantiated data model, the Agent MUST return an OperationSuccess for this requested_path, and include an empty set for affected_path.

`repeated UnaffectedPathError unaffected_path_errs`

This field contains a repeated set of messages of type `UnaffectedPathError`.

**[R-DEL.3]{}** - This set MUST include one `UnaffectedPathError` message for each Object Instance that exists in the Agent's instantiated data model and were matched by the Path Name specified in `obj_path` and failed to delete.

**[R-DEL.4]{}** - If the Controller does not have Read permission on any of the Objects specified in `unaffected_paths`, these Objects MUST NOT be returned in this field.

###### UnaffectedPathError Fields

`string unaffected_path`

This field returns the Path Name to the Object Instance that failed to be deleted.

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of the error that caused the deletion of this Object to fail.

`string err_msg`

This field contains text related to the error specified by `err_code`.

#### Delete Message Supported Error Codes

Appropriate error codes for the Delete Message include `7000-7008`, `7015`, `7016`, `7018`, `7024`, `7026` and `7800-7999`.

## Reading an Agent’s State and Capabilities

An Agent’s current state and capabilities are represented in its data model. The current state is referred to as its Instantiated Data Model, while the data model that represents its set of capabilities is referred to as its Supported Data Model. Messages exist to retrieve data from both the instantiated and Supported Data Models.

### The Get Message

The basic Get Message is used to retrieve the values of a set of Object’s Parameters in order to learn an Agent’s current state. It takes a set of Path Names as an input and returns the complete tree of all Objects and Sub-Objects of any Object matched by the specified expressions, along with each Object's Parameters and their values. The Search Paths specified in a Get request can also target individual Parameters within Objects to be returned.

*Note: Those familiar with Broadband Forum TR-069 [@TR-069] will recognize this behavior as the difference between "Partial Paths" and "Complete Paths". This behavior is replicated in USP for the Get Message for each Path Name that is matched by the expression(s) supplied in the request.*

*Note: Each Search Path is intended to be evaluated separately, and the results from a given Search Path are returned in a field dedicated to that Path Name. As such, it is possible that the same information may be returned from more than one Search Path. This is intended, and the Agent should treat each Search Path atomically.*

The response returns a `req_path_results` entry for each Path Name given in `param_paths`. If a Path expression specified in the request does not match any valid Parameters or Objects, the response will indicate that this expression was an "Invalid Path", indicating that the Object or Parameter does not currently exist in the Agent’s Supported Data Model.

Each `req_path_results` message given in the response contains a set of `resolved_path_results` messages for each Object and Sub-Object relative to the Path resolved by the `param_paths` element. Each results is followed by a list of Parameters (`result_params`) and their values. If there are no Parameters, `result_params` may be empty.  These Parameter Paths are Relative Paths to the `resolved_path`.
*Note: This behavior has been clarified as of USP 1.2. Previous versions implied that Sub-Object Parameters be returned as Relative Paths to the original `resolved_path` in a single `result_params` list. In USP 1.2, each Sub-Object is returned in its own `resolved_path`.*

The tree depth of a Get response can be limited by specifying a non-zero value for the `max_depth` field in Get request. If `max_depth` field is present and not `0` then the Agent will limit the maximum depth of each returned `req_path_results` to a tree rooted in `requested_path` with a depth specified by `max_depth` value.

*Note: The `max_depth` field was introduced in USP 1.2. If this field is not present in a Get request or has a value of `0`, the Agent returns the complete tree of all Objects and Sub-Objects of all the Path Names mentioned in `param_paths`. This is the same as the behavior specified for prior USP versions. An Agent implementing a prior version of the USP specification will ignore the field and behave as if the `max_depth` field was set to `0`.*


#### Get Examples

The following table illustrates the result params for one of the Path Names mentioned in `param_paths` is `Device.DeviceInfo.` and example values of the `max_depth` Get request field.

| `max_depth`	| `param_paths`	| `result_params`	|
| -----: | :-----: | :----- |
| `0` | `Device.DeviceInfo.` | All the Parameters of `Device.DeviceInfo.` and all of its Sub-Objects (like `Device.DeviceInfo.TemperatureStatus.` and `Device.DeviceInfo.TemperatureStatus.TemperatureSensor.{i}.`) along with their values |
| `1`	| `Device.DeviceInfo.` | All the Parameters of `Device.DeviceInfo.` and their values only |
| `2`	| `Device.DeviceInfo.` | All the Parameters of `Device.DeviceInfo.` and its first level Sub-Objects(like `Device.DeviceInfo.TemperatureStatus.`) along with their values |
| `3`	| `Device.DeviceInfo.` | All the Parameters of `Device.DeviceInfo.` and its first and second level Sub-Objects (like `Device.DeviceInfo.TemperatureStatus.` and `Device.DeviceInfo.TemperatureStatus.TemperatureSensor.{i}.`) along with their values |


For example, a Controller wants to read the data model to learn the settings and `Stats` of a single Wi-Fi SSID, "HomeNetwork" with a BSSID of "00:11:22:33:44:55". It could use a Get request with the following fields:

```{filter=pbv type=Request}
    get {
      param_paths: 'Device.WiFi.SSID.[SSID=="HomeNetwork"&&BSSID=="00:11:22:33:44:55"].'
      max_depth: 2
    }
```

In response to this request the Agent returns all Parameters, plus the Parameters of any Sub-Objects, of the addressed instance. Had `max_depth` been set to `1` then all of the SSID Parameters and their values would have been returned, but the `Stats` Sub-Object and its Parameters would have been omitted. The Agent returns this data in the Get response using a field for each of the requested Path Names. In this case:

```{filter=pbv type=Response}
    get_resp {
      req_path_results {
        requested_path: 'Device.WiFi.SSID.[SSID=="HomeNetwork"&&BSSID=="00:11:22:33:44:55"].'
        resolved_path_results {
          resolved_path: "Device.WiFi.SSID.1."
          result_params {
            key: "Enable"
            value: "true"
          }
          result_params {
            key: "Status"
            value: "Up"
          }
          result_params {
            key: "Alias"
            value: "cpe-alias-1"
          }
          result_params {
            key: "Name"
            value: "Home Network"
          }
          result_params {
            key: "LastChange"
            value: "864000"
          }
          result_params {
            key: "BSSID"
            value: "00:11:22:33:44:55"
          }
          result_params {
            key: "SSID"
            value: "HomeNetwork"
          }
        }

        resolved_path_results {
          resolved_path: "Device.WiFi.SSID.1.Stats."
          result_params {
            key: "BytesSent"
            value: "24901567"
          }
          result_params {
            key: "BytesReceived"
            value: "892806908296"
          }

#           (etc.)


        }
      }
    }
```

In another example, the Controller only wants to read the current status of the Wi-Fi network with the SSID "HomeNetwork" with the BSSID of 00:11:22:33:44:55. It could use a Get request with the following fields:

```{filter=pbv type=Request}
    get {
      param_paths: 'Device.WiFi.SSID.[SSID=="HomeNetwork"&&BSSID=="00:11:22:33:44:55"].Status'
    }
```

In response to this request the Agent returns only the Status Parameter and its value.

```{filter=pbv type=Response}
    get_resp {
      req_path_results {
        requested_path: 'Device.WiFi.SSID.[SSID=="HomeNetwork"&&BSSID=="00:11:22:33:44:55"].Status'
        resolved_path_results {
          resolved_path: "Device.WiFi.SSID.1."
          result_params {
            key: "Status"
            value: "Up"
          }
        }
      }
    }
```

Lastly, using wildcards or another Search Path, the requested Path Name may resolve to more than one resolved Path Names. For example for a Request sent to an Agent with two `WiFi.SSID` instances:

```{filter=pbv type=Request}
    get {
      param_paths: "Device.WiFi.SSID.*.Status"
    }
```

The Agent's response would be:

```{filter=pbv type=Response}
    get_resp {
      req_path_results {
        requested_path: "Device.WiFi.SSID.*.Status"
        resolved_path_results {
          resolved_path: "Device.WiFi.SSID.1."
          result_params {
            key: "Status"
            value: "Up"
          }
        }
        resolved_path_results {
          resolved_path: "Device.WiFi.SSID.2."
          result_params {
            key: "Status"
            value: "Up"
          }
        }
      }
    }
```

In an example with full USP Message header and body, the Controller requests all Parameters of the MTP table entry that contains the `Alias` value "WS-MTP1", and the value of the `Enable` Parameter of the `Subscription` table where the value of the Parameter `ID` is "boot-1" and the `Recipient` Parameter has a value of "Device.LocalAgent.Controller.1":

```{filter=pbv}
header {
  msg_id: "5721"
  msg_type: GET
}
body {
  request {
    get {
      param_paths: 'Device.LocalAgent.MTP.[Alias=="WS-MTP1"].'
      param_paths: 'Device.LocalAgent.Subscription.[ID=="boot-1"&&Recipient=="Device.LocalAgent.Controller.1"].Enable'
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "5721"
  msg_type: GET_RESP
}
body {
  response {
    get_resp {
      req_path_results {
        requested_path: 'Device.LocalAgent.MTP.[Alias=="WS-MTP1"].'
        resolved_path_results {
          resolved_path: "Device.LocalAgent.MTP.5156."
          result_params {
            key: "Alias"
            value: "WS-MTP1"
          }
          result_params {
            key: "Enable"
            value: "true"
          }
          result_params {
            key: "Status"
            value: "Up"
          }
          result_params {
            key: "Protocol"
            value: "WebSocket"
          }
          result_params {
            key: "EnableMDNS"
            value: "false"
          }
        }
        resolved_path_results {
          resolved_path: "Device.LocalAgent.MTP.5156.WebSocket."
          result_params {
            key: "Interfaces"
            value: "Device.IP.Interface.1."
          }
          result_params {
            key: "Port"
            value: "5684"
          }
          result_params {
            key: "Path"
            value: "usp-controller"
          }
          result_params {
            key: "EnableEncryption"
            value: "true"
          }
        }
      }

      req_path_results {
        requested_path: 'Device.LocalAgent.Subscription.[ID=="boot-1"&&Recipient=="Device.LocalAgent.Controller.1"].Enable'
        err_code: 0
        err_msg: ""
        resolved_path_results {
          resolved_path: "Device.LocalAgent.Subscription.6629."
          result_params {
            key: "Enable"
            value: "true"
          }
        }
      }
    }
  }
}
```

#### Get Request Fields

`repeated string param_paths`

This field is a set of Object Paths, Object Instance Paths, Parameter Paths, or Search Paths to Objects and Parameters in an Agent’s Instantiated Data Model.

`fixed32 max_depth`

This field limits the maximum depth of each returned `result_params` tree to the depth specified by `max_depth` value. A value of `0` returns the complete tree of all Objects and Sub-Objects of all the Path Names mentioned in `param_paths`.

**[R-GET.5]{}** - If the `max_depth` field is present and contains a value other than 0, then the Agent MUST limit the tree depth of the resolved Sub-Objects included in the `resolved_path_results` field of the Response to the specified value.

#### Get Response Fields

`repeated RequestedPathResult req_path_results`

A repeated set of `RequestedPathResult` messages for each of the Path Names given in the associated Get request.

##### RequestedPathResult Field

`string requested_path`

This field contains one of the Path Names or Search Paths given in the `param_path` field of the associated Get Request.

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the Get to fail on this Path Names. A value of 0 indicates the Path Name could be read successfully.

**[R-GET.0]{}** - If `requested_path` contains a Path Name (that is not a Search Path) that does not match any Object or Parameter in the Agent's Instantiated Data Model, or `requested_path` contains a Search Path that does not match any Object or Parameter in the Agent's Supported Data Model, the Agent MUST use the `7026 - Invalid Path` error in this `RequestedPathResult`.

**[R-GET.1]{}** - If the Controller making the Request does not have Read permission on an Object or Parameter matched through the `requested_path` field, the Object or Parameter MUST be treated as if it is not present in the Agent’s Supported data model.

*Note: Requiring Object Read permission is intended to act as a security feature. If a Controller does not have permission to obtain the names of the data model elements of an object via a `GetSupportedDM` request, then the Controller should not be able to discover these by probing with `Get` requests.*

`string err_msg`

This field contains additional information about the reason behind the error.

`repeated ResolvedPathResult resolved_path_results`

This field contains one message of type ResolvedPathResult for each Path Name resolved by the Path Name or Search Path given by `requested_path`.

**[R-GET.1a]{}** - If the `requested_path` is a valid Search Path (i.e., properly formatted and in the Agent's supported data model) but did not resolve to any Objects in the Agent's Instantiated Data Model, the `resolved_path_results` set MUST be empty and is not considered an error.

**[R-GET.1b]{}** - If the `requested_path` is a valid Object Path (i.e., properly formatted and in the Agent's supported data model), which is not a Search Path, but the Object does not have any Sub-Objects or Parameters, the `resolved_path_results` set MUST be empty and is not considered an error.

###### ResolvedPathResult Fields

`string resolved_path`

This field contains a Path Name to an Object or Object Instance that was resolved from the Path Name or Search Path given in `requested_path`.

**[R-GET.2]{}** - If the `requested_path` included a Path Name to a Parameter, the `resolved_path` MUST contain only the Path Name to the parent Object or Object Instance of that Parameter.

`map<string, string> result_params`

This field contains a set of mapped key/value pairs listing a Parameter Path (relative to the Path Name in `resolved_path`) to each of the Parameters and their values of the Object given in `resolved_path`.
Refer to [](#sec:parameter-value-encoding) for details of how Parameter values are encoded as Protocol Buffers v3 strings.

**[R-GET.3]{}** - If the `requested_path` included a Path Name to a Parameter, `result_params` MUST contain only the Parameter included in that Path Name.

**[R-GET.4]{}** - If the Controller has Read permission on the Object or Object Instance being returned in the `resolved_path`, but does not have Read permission on any of the Parameters specified in `result_params`, these Parameters MUST NOT be returned in this field. This MAY result in this field being empty.

#### Get Message Supported Error Codes

Appropriate error codes for the Get Message include `7000-7006`, `7008`, `7010`, `7016`, `7026` and `7800-7999`.

### The GetInstances Message {#sec:getinstances}

The GetInstances Message takes a Path Name to an Object and requests that the Agent return the Instances of that Object that exist and *possibly* any Multi-Instance Sub-Objects that exist as well as their Instances. This is used for getting a quick map of the Multi-Instance Objects (i.e., Tables) the Agent currently represents, and their Unique Key Parameters, so that they can be addressed and manipulated later.

GetInstances takes one or more Path Names to Multi-Instance Objects in a Request to an Agent. In addition, both GetInstances and GetSupportedDM (below) make use of a flag called `first_level_only`, which determines whether or not the Response should include all of the Sub-Objects that are children of the Object specified in `obj_path`. A value of `true` means that the Response returns data *only* for the Object specified. A value of false means that all Sub-Objects will be resolved and returned.

#### GetInstances Examples

For example, if a Controller wanted to know *only* the current instances of Wi-Fi SSID Objects that exist on an Agent (that has 2 SSIDs), it would send a GetInstances Request as:

```{filter=pbv type=Request}
    get_instances {
      obj_paths: "Device.WiFi.SSID."
      first_level_only: true
    }
```

The Agent's Response would contain:

```{filter=pbv type=Response}
    get_instances_resp {
      req_path_results {
        requested_path: "Device.WiFi.SSID."
        curr_insts {
          instantiated_obj_path: "Device.WiFi.SSID.1."
          unique_keys {
            key: "Alias"
            value: "UserWiFi1"
          }
          unique_keys {
            key: "Name"
            value: "UserWiFi1"
          }
          unique_keys {
            key: "BSSID"
            value: "00:11:22:33:44:55"
          }
        }

        curr_insts {
          instantiated_obj_path: "Device.WiFi.SSID.2."
          unique_keys {
            key: "Alias"
            value: "UserWiFi2"
          }
          unique_keys {
            key: "Name"
            value: "UserWiFi2"
          }
          unique_keys {
            key: "BSSID"
            value: "11:22:33:44:55:66"
          }
        }
      }
    }
```

In another example, the Controller wants to get all of  the Instances of the `Device.WiFi.AccessPoint` table, plus all of the instances of the AssociatedDevice Object and AC Object (Sub-Objects of AccessPoint). It would issue a GetInstances Request with the following:

```{filter=pbv type=Request}
    get_instances {
      obj_paths: "Device.WiFi.AccessPoint."
      first_level_only: false
    }
```

The Agent's Response will contain an entry in `curr_insts` for all of the Instances of the `Device.WiFi.AccessPoint` table, plus the Instances of the Multi-Instance Sub-Objects `.AssociatedDevice.` and `.AC.`:

```{filter=pbv type=Response}
    get_instances_resp {
      req_path_results {
        requested_path: "Device.WiFi.AccessPoint."
        curr_insts {
          instantiated_obj_path: "Device.WiFi.AccessPoint.1."
          unique_keys {
            key: "Alias"
            value: "cpe-alias-1"
          }
          unique_keys {
            key: "SSIDReference"
            value: "Device.WiFi.SSID.1"
          }
        }
        curr_insts {
          instantiated_obj_path: "Device.WiFi.AccessPoint.1.AssociatedDevice.1."
          unique_keys {
            key: "MACAddress"
            value: "11:22:33:44:55:66"
          }
        }
        curr_insts {
          instantiated_obj_path: "Device.WiFi.AccessPoint.1.AC.1."
          unique_keys {
            key: "AccessCategory"
            value: "BE"
          }
        }

        curr_insts {
          instantiated_obj_path: "Device.WiFi.AccessPoint.2."
          unique_keys {
            key: "Alias"
            value: "cpe-alias-2"
          }
          unique_keys {
            key: "SSIDReference"
            value: "Device.WiFi.SSID.2"
          }
        }
        curr_insts {
          instantiated_obj_path: "Device.WiFi.AccessPoint.2.AssociatedDevice.1."
          unique_keys {
            key: "MACAddress"
            value: "11:22:33:44:55:66"
          }
        }
        curr_insts {
          instantiated_obj_path: "Device.WiFi.AccessPoint.2.AC.1."
          unique_keys {
            key: "AccessCategory"
            value: "BE"
          }
        }
      }
    }
```

Or more, if more Object Instances exist.

#### GetInstances Request Fields

`repeated string obj_paths`

This field contains a repeated set of Path Names or Search Paths to Multi-Instance Objects in the Agent's Instantiated Data Model.

`bool first_level_only`

This field, if `true`, indicates that the Agent returns only those instances in the Object(s) matched by the Path Name or Search Path in `obj_path`, and not return any child Objects.

#### GetInstances Response Fields

`repeated RequestedPathResult req_path_results`

This field contains a RequestedPathResult message for each Path Name or Search

`string requested_path`

This field contains one of the Path Names or Search Paths given in `obj_path` of the associated GetInstances Request.

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the GetInstances to fail on this Path Name. A value of 0 indicates the Path Name could be read successfully.

**[R-GIN.0]{}** - If the Controller making the Request does not have Read permission on an Object or Parameter used for matching through the `requested_path` field, any otherwise matched Object MUST be treated as if it is not present in the Agent’s Instantiated Data Model

`string err_msg`

This field contains additional information about the reason behind the error.

`repeated CurrInstance curr_insts`

This field contains a message of type `CurrInstance` for each Instance of *all* of the Objects matched by `requested_path` that exists in the Agent's Instantiated Data Model.

###### CurrInstance Fields

`string instantiated_obj_path`

This field contains the Object Instance Path of the Object.

`map<string, string> unique_keys`

This field contains a map of key/value pairs for all of this Object's Unique Key Parameters that are supported by the Agent.

**[R-GIN.1]{}** - If the Controller does not have Read permission on any of the Parameters specified in `unique_keys`, these Parameters MUST NOT be returned in this field.

#### GetInstances Error Codes

Appropriate error codes for the GetInstances Message include `7000-7006`, `7008`, `7016`, `7018`, `7026` and `7800-7999`.

### The GetSupportedDM Message {#sec:the-getsupporteddm-message}

GetSupportedDM (referred to informally as GSDM) is used to retrieve the Objects, Parameters, Events, and Commands in the Agent's Supported Data Model. This allows a Controller to learn what an Agent understands, rather than its current state.

The GetSupportedDM Message is different from other USP Messages in that it only returns information about the Agent's Supported Data Model. This means that Path Names to Multi-Instance Objects only address the Object itself, rather than Instances of the Object, and those Path Names that contain Multi-Instance Objects in the Path Name use the `{i}` identifier to indicate their place in the Path Name as specified in TR-106 [@TR-106].

The `obj_paths` field takes a list of Object Paths, either from the Supported Data Model or the Instantiated Data Model.

For example, a Path Name to the `AssociatedDevice` Object (a child of the `.WiFi.AccessPoint` Object) could be addressed in the Supported Data Model as `Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.` but in addition to this notation the omission of the final `{i}.` is also allowed, such as `Device.WiFi.AccessPoint.{i}.AssociatedDevice.`. Both of these syntaxes are supported and equivalent.

Alternatively an Instantiated Data Model Object Path can be used as long as the Object exists, such as `Device.WiFi.AccessPoint.1.AssociatedDevice.`. The Agent will use the Supported Data Model pertaining to this particular Object when processing the Message.

If the Agent encounters a diverging Supported Data Model, e.g. due to the use of different Mounted Objects underneath a Mountpoint, the Agent will skip the traversal of the children Objects, populate the Response's `divergent_paths` element with all divergent Object Instance Paths, and continue processing with the next unambiguous Object. The Supported Data Model of such divergent Objects can only be obtained by specifically using Object Instance Paths in the `obj_paths` field of a GetSupportedDM request.

The Agent's Response returns all Path Names in the `supported_obj_path` field according to its Supported Data Model.

To clarify the difference between an Instantiated Data Model Object Path and a Supported Data Model Object Path:

*	If a `{i}` is encountered in the Object Path, it cannot be followed by an Instance Identifier.
*	If the Object Path ends with an Instance Identifier, it is treated as an Instantiated Data Model Object Path.
*	If the Object Path contains a `{i}`, it is a Supported Data Model Object Path.

#### GetSupportedDM Examples

For example, the Controller wishes to learn the Wi-Fi capabilities the Agent represents. It could issue a GetSupportedDM Request as:

```{filter=pbv type=Request}
    get_supported_dm {
      obj_paths : "Device.WiFi."
      first_level_only : false
      return_commands : false
      return_events : false
      return_params : false
      return_unique_key_sets : false
    }
```

The Agent's Response would be:

```{filter=pbv type=Response}
    get_supported_dm_resp {
      req_obj_results {
        req_obj_path: "Device.WiFi."
        data_model_inst_uri: "urn:broadband-forum-org:tr-181-2-12-0"
        supported_objs {
          supported_obj_path: "Device.WiFi."
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.Radio.{i}."
          access: OBJ_READ_ONLY
          is_multi_instance: true
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.Radio.{i}.Stats"
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.SSID.{i}."
          access: OBJ_ADD_DELETE
          is_multi_instance: true
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.SSID.{i}.Stats"
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}."
          access: OBJ_ADD_DELETE
          is_multi_instance: true
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.Security."
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.WPS."
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}."
          access: OBJ_READ_ONLY
          is_multi_instance: true
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.Stats."
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.AC.{i}."
          access: OBJ_READ_ONLY
          is_multi_instance: true
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.AC.{i}.Stats."
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}.Accounting."
          access: OBJ_READ_ONLY
          is_multi_instance: false
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.EndPoint.{i}."
          access: OBJ_ADD_DELETE
          is_multi_instance: true
        }

        ## And continued, for Device.WiFi.EndPoint.{i}. Sub-Objects such as Device.WiFi.EndPoint.{i}.Stats., Device.WiFi.EndPoint.{i}/// .Security., etc.

      }
    }
```

In another example request:

```{filter=pbv type=Request}
    get_supported_dm {
      obj_paths : "Device.WiFi."
      first_level_only : true
      return_commands : true
      return_events : true
      return_params : true
      return_unique_key_sets : true
    }
```

The Agent's response would be:

```{filter=pbv type=Response}
    get_supported_dm_resp {
      req_obj_results {
        req_obj_path: "Device.WiFi."
        data_model_inst_uri: "urn:broadband-forum-org:tr-181-2-12-0"
        supported_objs {
          supported_obj_path: "Device.WiFi."
          access: OBJ_READ_ONLY
          is_multi_instance: false
          supported_params {
            param_name: "RadioNumberOfEntries"
            access: PARAM_READ_ONLY
            value_type : PARAM_UNSIGNED_INT
            value_change : VALUE_CHANGE_ALLOWED
          }
          supported_params {
            param_name: "SSIDNumberOfEntries"
            access: PARAM_READ_ONLY
            value_type : PARAM_UNSIGNED_INT
            value_change : VALUE_CHANGE_ALLOWED
          }

          ## Continued for all Device.WiFi. Parameters

          supported_commands {
            command_name: "NeighboringWiFiDiagnostic()"
            output_arg_names: "Status"
            output_arg_names: "Result.{i}.Radio"
            output_arg_names: "Result.{i}.SSID"
            output_arg_names: "Result.{i}.BSSID"
            output_arg_names: "Result.{i}.Mode"
            output_arg_names: "Result.{i}.Channel"

            ## Continued for other NeighboringWiFiDiagnostic() output arguments

            command_type : CMD_ASYNC
          }
        }

        ## followed by its immediate child objects with no details

        supported_objs {
          supported_obj_path: "Device.WiFi.Radio.{i}."
          access: OBJ_READ_ONLY
          is_multi_instance: true
          unique_key_sets {
            key_names: "Alias"
          }
          unique_key_sets {
            key_names: "Name"
          }
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.SSID.{i}."
          access: OBJ_ADD_DELETE
          is_multi_instance: true
          unique_key_sets {
            key_names: "Alias"
          }
          unique_key_sets {
            key_names: "Name"
          }
          unique_key_sets {
            key_names: "BSSID"
          }
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.AccessPoint.{i}."
          access: OBJ_ADD_DELETE
          is_multi_instance: true
          unique_key_sets {
            key_names: "Alias"
          }
          unique_key_sets {
            key_names: "SSIDReference"
          }
        }
        supported_objs {
          supported_obj_path: "Device.WiFi.EndPoint.{i}."
          access: OBJ_ADD_DELETE
          is_multi_instance: true
          unique_key_sets {
            key_names: "Alias"
          }
          unique_key_sets {
            key_names: "SSIDReference"
          }
        }
      }
    }
```

#### GetSupportedDM Request Fields

`repeated string obj_paths`

This field contains a repeated set of Path Names to Objects, Commands, Events, or Parameters in the Agent's Supported or Instantiated Data Model. For Path Names from the Supported Data Model the omission of the final `{i}.` is allowed.

`bool first_level_only`

This field, if `true`, indicates that the Agent returns only those objects matched by the Path Name or Search Path in `obj_path` and its immediate (i.e., next level) child objects. The list of child objects does not include commands, events, or Parameters of the child objects regardless of the values of the following elements:

`bool return_commands`

This field, if `true`, indicates that, in the `supported_objs`, the Agent should include a `supported_commands` field containing Commands supported by the reported Object(s).

`bool return_events`

This field, if `true`, indicates that, in the `supported_objs`, the Agent should include a `supported_events` field containing Events supported by the reported Object(s).

`bool return_params`

This field, if `true`, indicates that, in the `supported_objs`, the Agent should include a `supported_params` field containing Parameters supported by the reported Object(s).

`bool return_unique_key_sets`

This field, if `true`, indicates that, in the `supported_objs`, the Agent should include a `unique_key_sets` field containing Parameters which uniquely identify an instance of the reported Object(s).

#### GetSupportedDMResp Fields

`repeated RequestedObjectResult req_obj_results`

This field contains a repeated set of messages of type `RequestedObjectResult`.

##### RequestedObjectResult Fields

`string req_obj_path`

This field contains one of the Path Names given in `obj_path` of the associated GetSupportedDM Request.

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the GetSupportedDM to fail on this Path Name. A value of 0 indicates the Path Name could be read successfully.

**[R-GSP.0]{}** - If the Controller making the Request does not have Read permission on an Object or Parameter matched through the `requested_path` field, the Object or Parameter MUST be treated as if it is not present in the Agent’s Supported Data Model.

`string err_msg`

This field contains additional information about the reason behind the error.

`string data_model_inst_uri`

This field contains a Uniform Resource Identifier (URI) to the Data Model associated with the Object specified in `obj_path`.

`repeated SupportedObjectResult supported_objs`

The field contains a message of type `SupportedObjectResult` for each reported Object.

###### SupportedObjectResult Fields

In the case of a diverging Supported Data Model, only the `supported_obj_path`, `access`, `is_multi_instance`, and `divergent_paths` fields will be populated for the divergent Object.

`string supported_obj_path`

This field contains the Full Object Path Name of the reported Object in Supported Data Model notation.

`ObjAccessType access`

The field contains an enumeration of type ObjAccessType specifying the access permissions that are specified for this Object in the Agent's Supported Data Model. This usually only applies to Multi-Instance Objects. This may be further restricted to the Controller based on rules defined in the Agent's Access Control List. It is an enumeration of:

```
    OBJ_READ_ONLY (0)
    OBJ_ADD_DELETE (1)
    OBJ_ADD_ONLY (2)
    OBJ_DELETE_ONLY (3)
```

`bool is_multi_instance`

This field, if `true`, indicates that the reported Object is a Multi-Instance Object.

`repeated SupportedParamResult supported_params`

The field contains a message of type `SupportedParamResult` for each Parameter supported by the reported Object. If there are no Parameters in the Object, this should be an empty list.

`repeated SupportedCommandResult supported_commands`

The field contains a message of type `SupportedCommandResult` for each Command supported by the reported Object. If there are no Commands supported by the Object, this should be an empty list.

`repeated SupportedEventResult supported_events`

The field contains a message of type `SupportedEventResult` for each Event supported by the reported Object. If there are no Events supported by the Object, this should be an empty list.

`repeated SupportedUniqueKeySet unique_key_sets`

The field contains a message of type `SupportedUniqueKeySet` for each UniqueKeySet supported by the reported Object. If the Object has no unique keys (for example a single instance object), this should be an empty list.

`repeated string divergent_paths`

The field contains an Object Instance Path for each divergent Path Name.

*Note: The `divergent_paths` field was added in USP 1.2. An Agent that supports versions before USP 1.2 would not know to send the `divergent_paths` field and thus an empty list will be seen by the Controller.*

###### SupportedParamResult Fields

`string param_name`

This field contains the Relative Path of the Parameter.

`ParamAccessType access`

The field contains an enumeration of type ParamAccessType specifying the access permissions that are specified for this Parameter in the Agent's Supported Data Model. This may be further restricted to the Controller based on rules defined in the Agent's Access Control List. If the Data Model indicates that a Parameter is writeOnceReadOnly, the GetSupportedDM returns PARAM_READ_WRITE. It is an enumeration of:

```
    PARAM_READ_ONLY (0)
    PARAM_READ_WRITE (1)
    PARAM_WRITE_ONLY (2)
```

`ParamValueType value_type`

This field contains an enumeration of type ParamValueType specifying the *primitive (or base) data type* of this Parameter in the Agent's Supported Data Model.  It is an enumeration of:
```
    PARAM_UNKNOWN (0)
    PARAM_BASE_64 (1)
    PARAM_BOOLEAN (2)
    PARAM_DATE_TIME (3)
    PARAM_DECIMAL (4)
    PARAM_HEX_BINARY (5)
    PARAM_INT (6)
    PARAM_LONG (7)
    PARAM_STRING (8)
    PARAM_UNSIGNED_INT (9)
    PARAM_UNSIGNED_LONG (10)
```
*Note: The value_type field was added in USP 1.2, and the PARAM_UNKNOWN enumerated value is present for backwards compatibility purposes. An Agent that supports versions before USP 1.2 would not know to send the value_type and thus a 0 value (PARAM_UNKNOWN) will be seen by the Controller.*

*Note: This refers to the data type of the Parameter as implemented on the device, even though the value itself is transmitted as a Protocol Buffers string.*

`ValueChangeType value_change`

This field contains an enumeration of type ValueChangeType specifying whether or not the Agent will honor or ignore a ValueChange Subscription for this Parameter. The value of this field does not impact the ability for a Controller to create a ValueChange Subscription that references the associated Parameter, it only impacts how the Agent handles the Subscription. It is an enumeration of:
```
    VALUE_CHANGE_UNKNOWN (0)
    VALUE_CHANGE_ALLOWED (1)
    VALUE_CHANGE_WILL_IGNORE (2)
```
*Note: The value_change field was added in USP 1.2, and the VALUE_CHANGE_UNKNOWN enumerated value is present for backwards compatibility purposes. An Agent that supports versions before USP 1.2 would not know to send the value_change and thus a 0 value (VALUE_CHANGE_UNKNOWN) will be seen by the Controller.*


###### SupportedCommandResult Fields

`string command_name`

This field contains the Relative Path of the Command.

`repeated string input_arg_names`

This field contains a repeated set of Relative Paths for the input arguments of the Command, which can include Objects and Object Instances where the names are represented in Supported Data Model notation.

*Note: This field only contains the Path Name of the supported Input arguments without details about the supported number of instances, mandatory arguments or expected data types. Those details are implementation specific and not detailed as part of the `SupportedCommandResult`.*

`repeated string output_arg_names`

This field contains a repeated set of Relative Paths for the output arguments of the Command, which can include Objects and Object Instances where the names are represented in Supported Data Model notation.

`CmdType command_type`

This field contains an enumeration of type CmdType specifying the type of execution for the Command.  It is an enumeration of:
```
    CMD_UNKNOWN (0)
    CMD_SYNC (1)
    CMD_ASYNC (2)
```
*Note: The command_type field was added in USP 1.2, and the CMD_UNKNOWN enumerated value is present for backwards compatibility purposes. An Agent that supports versions before USP 1.2 would not know to send the command_type and thus a 0 value (CMD_UNKNOWN) will be seen by the Controller.*

###### SupportedEventResult

`string event_name`

This field contains the Relative Path of the Event.

`repeated string arg_names`

This field contains a repeated set of Relative Paths for the arguments of the Event.

###### SupportedUniqueKeySet

`repeated string key_names`

This field contains a repeated set of relative parameters, whose values together uniquely identify an instance of the object in the instantiated data model.


#### GetSupportedDM Error Codes

Appropriate error codes for the GetSupportedDM Message include `7000-7006`, `7008`, `7016`, `7026`, and `7800-7999`.

*Note:  when using error `7026` (Invalid path), it is important to note that in the context of GetSupportedDM this applies to the Agent's Supported Data Model.*

### GetSupportedProtocol

The GetSupportedProtocol Message is used as a simple way for the Controller and Agent to learn
which versions of USP each supports to aid in interoperability and backwards
compatibility.

#### GetSupportedProtocol Request Fields

`string controller_supported_protocol_versions`

A comma separated list of USP Protocol Versions (major.minor) supported by this Controller.

#### GetSupportedProtocolResponse Fields

`string agent_supported_protocol_versions`

A comma separated list of USP Protocol Versions (major.minor) supported by this Agent.

### The Register Message {#sec:register}

The Register message is an Agent to Controller message used to register new Service Elements.

See [Software Modularization and USP-Enabled Applications Theory of Operation appendix](#sec:software-modularization-theory-of-operations) for more information on when to use the Register message.

#### Register Examples

A USP Agent can register several Service Elements with one or multiple Register Request messages.

```{filter=pbv}
header {
  msg_id: "94521"
  msg_type: REGISTER
}
body {
  request {
    register {
      allow_partial: true
      reg_paths {
        path: "Device.Time."
      }
      reg_paths {
        path: "Device.WiFi.DataElements."
      }
    }
  }
}
```

In case the registration was successful, the USP Controller will respond with a Register Response message.

```{filter=pbv}
header {
  msg_id: "94521"
  msg_type: REGISTER_RESP
}
body {
  response {
    register_resp {
      registered_path_results {
        requested_path: "Device.Time."
        oper_status {
          oper_success {
            registered_path: "Device.Time."
          }
        }
      }

      registered_path_results {
        requested_path: "Device.WiFi.DataElements."
        oper_status {
          oper_success {
            registered_path: "Device.WiFi.DataElements."
          }
        }
      }
    }
  }
}
```

In case the registration failed partially, because the "Device.WiFi.DataElements." object was already registered, the USP Controller will respond with the following Register Response message.

```{filter=pbv}
header {
  msg_id: "94521"
  msg_type: REGISTER_RESP
}
body {
  response {
    register_resp {
      registered_path_results {
        requested_path: "Device.Time."
        oper_status {
          oper_success {
            registered_path: "Device.Time."
          }
        }
      }

      registered_path_results {
        requested_path: "Device.WiFi.DataElements."
        oper_status {
          oper_failure {
            err_code: 7029
            err_msg: "Device.WiFi.DataElements. object path has already been registered"
          }
        }
      }
    }
  }
}
```

If `allow_partial` was set to `false` in the Register Request and the registration failed, the USP Controller would instead respond with a USP Error message.

```{filter=pbv}
header {
  msg_id: "94521"
  msg_type: ERROR
}
body {
  error {
    err_code: 7029
    err_msg: "Device.WiFi.DataElements. object path has already been registered"
  }
}
```

#### Register Request Fields

`bool allow_partial`

The Register message contains a boolean `allow_partial` to indicate whether the registration must succeed completely or is allowed to fail partially. If `allow_partial` is `false`, nothing will be registered if one of the provided paths fails to be registered (e.g. due to an already existing registration) and the USP Controller will respond with a USP Error message. If `allow_partial` is `true`, the USP Controller will try to register every path individually and will always respond with a RegisterResp message, even if none of the requested paths can be registered.

**[R-REG.0]{}** - If the `allow_partial` field is set to `true` and no other exceptions are encountered, the Controller treats each of the reg_paths independently. The Controller MUST complete the registration of each reg_path regardless of the inability to register one of the others.

**[R-REG.1]{}** - If the `allow_partial` field is set to `false`, and no other exceptions are encountered, the Controller treats each of the reg_paths holistically. A failure to handle one of the reg_paths will cause the Register Message to fail and return an Error Message.

`repeated RegistrationPath reg_paths`

This field contains a repeated set of RegistrationPaths for each path the USP Agent wants to register.

##### RegistrationPath Fields

`string path`

This field contains the Object Path the USP Agent wants to register.

**[R-REG.2]{}** - The path field MUST contain an Object Path, Command Path, Event Path, or Parameter Path without any instance numbers. This path MUST NOT not use the Supported Data Model notation (with \{i\}), meaning that it is not allowed to register a sub-object to a multi-instance object.

#### Register Response Fields

`repeated RegisteredPathResult registered_path_results`

This field contains a repeated set of RegisteredPathResults for each path the USP Agent tried to register.

#### RegisteredPathResult Fields

`string requested_path`

This field contains the value of the entry of the path (in the Register Request) associated with this RegisteredPathResult.

`OperationStatus oper_status`

This field contains a message of type OperationStatus.

##### OperationStatus Fields

`oneof oper_status`

This field contains a message of one of the following types.

`OperationFailure oper_failure`

Used when the path specified in requested_path failed to be registered.

`OperationSuccess oper_success`

Used when the path specified in requested_path was successfully registered.

##### OperationFailure Fields

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the registration to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

##### OperationSuccess Fields

`string registered_path`

This field returns the path that was registered.

#### Register Message Supported Error Codes

Appropriate error codes for the Register Message include 7000-7008, 7016, 7028-7029 and 7800-7999.

### The Deregister Message {#sec:deregister}

The Deregister message is an Agent to Controller message used to deregister a previously registered data model at the USP Controller. When a USP Agent terminates, all Services elements will be deregistered automatically by the USP Controller.

A USP Agent can choose to deregister its Service Elements during normal operation or when it terminates.

*Note: A Deregister Request does not contain a boolean `allow_partial`, but the Controller will handle each path in the Deregister Request individually. In other words, `allow_partial` is implicitly set to `true` during the deregistration. The USP Controller will provide information about the success or failure to deregister each requested path in the Deregister Response message.*

#### Deregister Examples

A USP Agent can deregister several Service Elements with a Deregister Request message.

```{filter=pbv}
header {
  msg_id: "94522"
  msg_type: DEREGISTER
}
body {
  request {
    deregister {
      paths: "Device.Time."
      paths: "Device.WiFi.DataElements."
    }
  }
}
```

In case the deregistration was successful, the USP Controller will respond with a Deregister Response message.

```{filter=pbv}
header {
  msg_id: "94522"
  msg_type: DEREGISTER_RESP
}
body {
  response {
    deregister_resp {
      deregistered_path_results {
        requested_path: "Device.Time."
        oper_status {
          oper_success {
            deregistered_path: "Device.Time."
          }
        }
      }

      deregistered_path_results {
        requested_path: "Device.WiFi.DataElements."
        oper_status {
          oper_success {
            deregistered_path: "Device.WiFi.DataElements."
          }
        }
      }
    }
  }
}
```

#### Deregister Request Fields

`repeated string paths`

This field contains a set of paths that the USP Agent wants to deregister.

**[R-DEREG.1]{}** - A USP Agent MUST *only* deregister Service Elements that it registered with a previous Register message.

**[R-DEREG.2]{}** - An empty path field MUST be interpreted to deregister all Service Elements belonging to the USP Agent.

**[R-DEREG.3]{}** - A USP Agent MAY deregister one or more Service Elements with one Deregister Request message containing multiple path fields.

*Note: The path field contains an Object Path, Command Path, Event Path, or Parameter Path without any instance numbers. This path doesn't contain any sub-objects to a multi-instance object.*

#### Deregister Response Fields

`repeated DeregisteredPathResult deregistered_path_results`

This field contains a repeated set of DeregisteredPathResults for each path the USP Agent tried to deregister.

**[R-DEREG.4]{}** - A USP Controller MUST always respond with a Deregister Response message to a Deregister Request. USP Error messages are not used.

#### DeregisteredPathResult Fields

`string requested_path`

This field contains the value of the entry of the path (in the Deregister Request) associated with this DeregisteredPathResult.

`OperationStatus oper_status`

This field contains a message of type OperationStatus.

##### OperationStatus Fields

`oneof oper_status`

This field contains a message of one of the following types.

`OperationFailure oper_failure`

Used when the path specified in requested_path failed to be deregistered.

`OperationSuccess oper_success`

Used when the path specified in requested_path was successfully deregistered.

##### OperationFailure Fields

`fixed32 err_code`

This field contains a numeric code ([](#sec:error-codes)) indicating the type of error that caused the deregistration to fail.

`string err_msg`

This field contains additional information about the reason behind the error.

##### OperationSuccess Fields

`string deregistered_path`

This field returns the path that was deregistered.

#### Deregister Message Supported Error Codes

Appropriate error codes for the Deregister Message include 7000-7008, 7016, 7030 and 7800-7999.

## Notifications and Subscription Mechanism {#sec:notifications-and-subscriptions}

A Controller can use the Subscription mechanism to subscribe to certain events that occur on the Agent, such as a Parameter change, Object removal, wake-up, etc. When such event conditions are met, the Agent may either send a [Notify Message](#sec:notify) to the Controller, update its own configuration, or perform both actions depending on the Subscription's configuration.

### Using Subscription Objects

Subscriptions are maintained in instances of the Multi-Instance Subscription Object in the USP data model. The normative requirements for these Objects are described in the data model Parameter descriptions for `Device.LocalAgent.Subscription.{i}.` in the Device:2 Data Model [@TR-181].

**[R-NOT.0]{}** - The Agent and Controller MUST follow the normative requirements defined in the `Device.LocalAgent.Subscription.{i}.` Object specified in the Device:2 Data Model [@TR-181].

**[R-NOT.0a]{}** - When considering the time needed to make a state change and trigger a Notification, an implementation SHOULD make changes to its state and initiate a Notification with a window no longer than 10 seconds.

*Note: Those familiar with Broadband Forum TR-069 [@TR-069] will recall that a notification for a value change caused by an Auto-Configuration Server (ACS - the CWMP equivalent of a Controller) are not sent to the ACS. Since there is only a single ACS notifying the ACS of value changes it requested is unnecessary. This is not the case in USP: an Agent should follow the behavior specified by a subscription, regardless of the originator of that subscription.*

#### ReferenceList Parameter

All subscriptions apply to one or more Objects or Parameters in the Agent’s Instantiated Data Model. These are specified as Path Names or Search Paths in the `ReferenceList` Parameter. The `ReferenceList` Parameter may have different meaning depending on the nature of the notification subscribed to.

For example, a Controller wants to be notified when a new Wi-Fi station joins the Wi-Fi network. It uses the Add Message to create an instance of a Subscription Object with `Device.WiFi.AccessPoint.1.AssociatedDevice.` specified in the `ReferenceList` Parameter and `ObjectCreation` as the `NotificationType`.

In another example, a Controller wants to be notified whenever an outside source changes the SSID of a Wi-Fi network. It uses the Add Message to create an instance of a Subscription Object with `Device.WiFi.SSID.1.SSID` specified in the `ReferenceList` and `ValueChange` as the `NotificationType`.

#### TriggerAction Parameter

Subscriptions can be used to define the actions to be performed by the Agent when an event occurs. This is defined in the `TriggerAction` Parameter. The default is for the Agent to send a [Notify Message](#sec:notify), but it could also perform an update of its own configuration, or both sending the Notify and performing the configuration.

For example, an Agent may be configure with a Subscription for the `Device.LocalAgent.Threshold.{i}.Triggered!` event such that when it occurs the Agent both sends a Notify message and configures the `Device.BulkData.Profile.{i}.Enable` to start sending BukData reports (if defined to do so in the `TriggerConfigSettings` Parameter of the Subscription).


### Responses to Notifications and Notification Retry {#sec:responses-and-retry}

The Notify request contains a flag, `send_resp`, that specifies whether or not the Controller should send a response Message after receiving a Notify request. This is used in tandem with the `NotifRetry` Parameter in the subscription Object - if `NotifRetry` is `true`, then the Agent sends its Notify requests with `send_resp : true`, and the Agent considers the notification delivered when it receives a response from the Controller. If `NotifRetry` is `false`, the Agent does not need to use the `send_resp` flag and should ignore the delivery state of the notification.

If `NotifRetry` is `true`, and the Agent does not receive a response from the Controller, it begins retrying using the retry algorithm below. The subscription Object also uses a `NotifExpiration` Parameter to specify when this retry should end if no success is ever achieved.

**[R-NOT.1]{}** - When retrying notifications, the Agent MUST use the following retry algorithm to manage the retransmission of the Notify request.

The retry interval range is controlled by two Parameters, the minimum wait interval and the interval multiplier, each of which corresponds to a data model Parameter, and which are described in the table below. The factory default values of these Parameters MUST be the default values listed in the Default column. They MAY be changed by a Controller with the appropriate permissions at any time.

| Descriptive Name | Symbol | Default | Data Model Parameter Name |
| ---------: | :-----: | :------: | :------------ |
| Minimum wait interval | m | 5 seconds | `Device.LocalAgent.Controller.{i}.USPNotifRetryMinimumWaitInterval` |
| Interval multiplier |	k | 2000 | `Device.LocalAgent.Controller.{i}.USPNotifRetryIntervalMultiplier` |

| Retry Count | Default Wait Interval Range (min-max seconds) | Actual Wait Interval Range (min-max seconds) |
| ----------: | :---------: | :-------------- |
| #1 | 5-10 | m - m.(k/1000) |
| #2 | 10-20 | m.(k/1000) - m.(k/1000)^2 |
| #3 | 20-40 | m.(k/1000)^2 - m.(k/1000)^3 |
| #4 | 40-80 | m.(k/1000)^3 - m.(k/1000)^4 |
| #5 | 80-160 | m.(k/1000)^4 - m.(k/1000)^5 |
| #6 | 160-320 | m.(k/1000)^5 - m.(k/1000)^6 |
| #7 | 320-640 | m.(k/1000)^6 - m.(k/1000)^7 |
| #8 | 640-1280 | m.(k/1000)^7 - m.(k/1000)^8 |
| #9 | 1280-2560 | m.(k/1000)^8 - m.(k/1000)^9 |
| #10 and subsequent | 2560-5120 | m.(k/1000)^9 - m.(k/1000)^10 |

**[R-NOT.2]{}** - Beginning with the tenth retry attempt, the Agent MUST choose from the fixed maximum range. The Agent will continue to retry a failed notification until it is successfully delivered or until the `NotifExpiration` time is reached.

**[R-NOT.3]{}** - Once a notification is successfully delivered, the Agent MUST reset the retry count to zero for the next notification Message.

**[R-NOT.4]{}** - If a reboot of the Agent occurs, the Agent MUST reset the retry count to zero for the next notification Message.

### Notification Types {#sec:notification-types}

There are several types events that can cause a Notify request. These include those that deal with changes to the Agent’s Instantiated Data Model (`ValueChange`, `ObjectCreation`, `ObjectDeletion`), the completion of an asynchronous Object-defined operation (`OperationComplete`), a policy-defined `OnBoardRequest`, and a generic `Event` for use with Object-defined events.

#### ValueChange

The `ValueChange` notification is subscribed to by a Controller when it wants to know that the value of a single or set of Parameters has changed from the state it was in at the time of the subscription or to a state as described in an expression, and then each time it transitions from then on for the life of the subscription. It is triggered when the defined change occurs, even if it is caused by the originating Controller.

#### ObjectCreation and ObjectDeletion

These notifications are used for when an instance of the subscribed to Multi-Instance Objects is added or removed from the Agent’s Instantiated Data Model. Like `ValueChange`, this notification is triggered even if the subscribing Controller is the originator of the creation or deletion or the instance was created or deleted implicitly, e.g. due to a configuration or status change or indirectly via an unrelated USP Message.

The `ObjectCreation` notification also includes the Object’s Unique Key Parameters and their values.

#### OperationComplete

The `OperationComplete` notification is used to indicate that an asynchronous Object-defined operation finished (either successfully or unsuccessfully). These operations may also trigger other Events defined in the data model (see below).

#### OnBoardRequest

An `OnBoardRequest` notification is used by the Agent to initiate the request in order to communicate with a Controller that can provide on-boarding procedures and communicate with that Controller (likely for the first time).

**[R-NOT.5]{}** - An Agent MUST send an `OnBoardRequest` notify request in the following circumstances:

1.	When the `SendOnBoardRequest()` command is executed. This sends the notification request to the Controller that is the subject of that operation. The `SendOnBoardRequest()` operation is defined in the Device:2 Data Model [@TR-181]. This requirement applies only to those Controller table instances that have their `Enabled` Parameter set to `true`. When the implementation supports the `Device.LocalAgent.Controller.{i}.OnBoardingComplete` parameter, executing this command will set the parameter value to `false`.

2.	When instructed to do so by internal application policy (for example, when using DHCP discovery defined above).

3.  When the implementation supports the `Device.LocalAgent.Controller.{i}.OnBoardingComplete` parameter and its value is set to false as this parameter signifies the Controller requires an `OnBoardRequest`. This parameter SHOULD be set to true by the Agent or Controller when the onboarding has been completed.

The value of the `OnBoardingRestartTime` parameter, if supported, describes how long the USP Agent must wait to send another `OnBoardRequest` when `OnBoardingComplete` remains `false`. This timer starts as soon as the Agent receives the `NotifyResponse` message for the original `OnBoardRequest`, because the Notification Retry mechanism needs to be completed first.

*Note: as defined in the Subscription table, OnBoardRequest is not included as one of the enumerated types of a Subscription, i.e., it is not intended to be the subject of a Subscription. However it is important that the OnBoardRequest reaches its destination so it MUST be sent with `send_resp=true`. In other words, it behaves as a subscription with `NotifRetry` set to true. Because the Controller might be unreachable for a long time, the notification MUST not expire, so it MUST behave as a subscripton with `NotifExpiration` set to 0.*

**[R-NOT.6]{}** The OnBoardRequest MUST be sent with send_resp=true and MUST follow the Retry logic defined above.

**[R-NOT.6a]{}** The OnBoardRequest MUST be retried until the Controller confirms it has received it with a Notify Response message.

#### Event
The `Event` notification is used to indicate that an Object-defined event was triggered on the Agent. These events are defined in the data model and include what Parameters, if any, are returned as part of the notification.

### The Notify Message {#sec:notify}

#### Notify Examples

In this example, a Controller has subscribed to be notified of changes in value to the `Device.DeviceInfo.FriendlyName` Parameter. When it is changed, the Agent sends a Notify Request to inform the Controller of the change.

```{filter=pbv}
header {
  msg_id: "33936"
  msg_type: NOTIFY
}
body {
  request {
    notify {
      subscription_id: "vc-1"
      send_resp: true
      value_change {
          param_path: "Device.DeviceInfo.FriendlyName"
          param_value: "MyDevicesFriendlyName"
      }
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "33936"
  msg_type: NOTIFY_RESP
}
body {
  response {
    notify_resp {
      subscription_id: "vc-1"
    }
  }
}
```

In another example, the event "Boot!", defined in the `Device.` Object, is triggered. The Agent sends a Notify Request to the Controller(s) subscribed to that event.

```{filter=pbv}
header {
  msg_id: "26732"
  msg_type: NOTIFY
}
body {
  request {
    notify {
      subscription_id: "boot-1"
      send_resp: true
      event {
        obj_path: "Device."
        event_name: "Boot!"
        params {
          key: "Cause"
          value: "LocalReboot"
        }
        params {
          key: "CommandKey"
          value: "controller-command-key"
        }
        params {
          key: "ParameterMap"
          value: '{"Device.LocalAgent.Controller.1.Enable":"True","Device.LocalAgent.Controller.2.Enable":"False"}'
        }
        params {
          key: "FirmwareUpdated"
          value: "false"
        }
      }
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "26732"
  msg_type: NOTIFY_RESP
}
body {
  response {
    notify_resp {
      subscription_id: "boot-1"
    }
  }
}
```

#### Notify Request Fields

`string subscription_id`

This field contains the locally unique opaque identifier that was set by the Controller when it created the Subscription on the Agent.

**[R-NOT.7]{}** - The `subscription_id` field MUST contain the Subscription ID of the Subscription Object that triggered this notification. If no subscription_id is available (for example, for OnBoardRequest notifications), this field MUST be set to an empty string.

`bool send_resp`

This field lets the Agent indicate to the Controller whether or not it expects a response in association with the Notify request.

**[R-NOT.8]{}** - When `send_resp` is set to false, the Controller SHOULD NOT send a response or error to the Agent. If a response is still sent, the responding Controller MUST expect that any such response will be ignored.

`oneof notification`

Contains one of the following Notification messages:

    Event	event
    ValueChange value_change
    ObjectCreation obj_creation
    ObjectDeletion obj_deletion
    OperationComplete oper_complete
    OnBoardRequest on_board_req

##### Event Fields

`string obj_path`

This field contains the Object or Object Instance Path of the Object that caused this event (for example, `Device.LocalAgent.`).

`string event_name`

This field contains the name of the Object defined event that caused this notification (for example, `Boot!`).

`map<string, string> parameters`

This field contains a set of key/value pairs of Parameters associated with this event.
Refer to [](#sec:parameter-value-encoding) for details of how Parameter values are encoded as Protocol Buffers v3 strings.

##### ValueChange Fields

`string param_path`

This field contains the Path Name of the changed Parameter.

`string param_value`

This field contains the value of the Parameter specified in `param_path`.
Refer to [](#sec:parameter-value-encoding) for details of how Parameter values are encoded as Protocol Buffers v3 strings.

##### ObjectCreation Fields

`string obj_path`

This field contains the Path Name of the created Object Instance.

`map<string, string> unique_keys`

This field contains a map of key/value pairs for all of this Object's Unique Key Parameters that are supported by the Agent.

##### ObjectDeletion Fields

`string obj_path`

This field contains the Path Name of the deleted Object Instance.

##### OperationComplete Fields

`string command_name`

This field contains the Relative Path of the Object defined command that caused this notification (i.e., `Download()`).

`string obj_path`

This field contains the Object or Object Instance Path to the Object that contains this operation.

`string command_key`

This field contains the command key set during an Object defined Operation that caused this notification.

`oneof operation_resp`

Contains one of the following messages:

    OutputArgs req_output_args
    CommandFailure cmd_failure

###### OutputArgs Fields

`map<string, string> output_args`

This field contains a map of key/value pairs indicating the output arguments (relative to the command specified in the `command_name` field) returned by the method invoked in the Operate Message.
Refer to [](#sec:parameter-value-encoding) for details of how argument values are encoded as Protocol Buffers v3 strings.

###### CommandFailure Fields

`fixed32 err_code`

This field contains a numeric code (see [](#sec:error-codes)) indicating the type of the error that caused the operation to fail. Appropriate error codes for CommandFailure include `7002-7008`, `7016`, `7022`, `7023`, and `7800-7999`.
Error `7023` is reserved for asynchronous operations that were canceled by
a Controller invoking the Cancel() command on the appropriate Request Object (see [](#sec:asynchronous-operations)).

`string err_msg`

This field contains additional (human readable) information about the reason behind the error.

##### OnBoardRequest Fields

`string oui`

This field contains the Organizationally Unique Identifier associated with the Agent.

`string product_class`

This field contains a string used to provide additional context about the Agent.

`string serial_number`

This field contains a string used to provide additional context about the Agent.

`string agent_supported_protocol_versions`

A comma separated list of USP Protocol Versions (major.minor) supported by this Agent.

#### Notify Response Fields

`string subscription_id`

This field contains the Subscription ID that was received with the Notify Request.

**[R-NOT.9]{}** -The Agent SHOULD ignore the subscription_id field.

*Note: The requirement in the previous versions of the specification requiring the Agent to check this subscription_id field has been deprecated. However for backward compatibility the Controller is still required to send the matching subscription_id.*

**[R-NOT.10]{}** - The Controller MUST populate the subscription_id field with the same Subscription ID as was presented in the Notify Request.

#### Notify Error Codes

Appropriate error codes for the Notify Message include `7000-7006`, and `7800-7999`.

## Defined Operations Mechanism

Additional methods (operations) are and can be defined in the USP data model. Operations are generally defined on an Object, using the "command" attribute, as defined in [@TR-106]. The mechanism is controlled using the [Operate Message](#sec:operate) in conjunction with the Multi-Instance Request Object.

### Synchronous Operations

A synchronous operation is intended to complete immediately following its processing. When complete, the output arguments are sent in the Operate response. If the `send_resp` flag is false, the Controller doesn’t need the returned information (if any), and the Agent does not send an Operate Response.

![Operate Message Flow for Synchronous Operations](synchronous_operation.png)

### Asynchronous Operations {#sec:asynchronous-operations}

An asynchronous operation expects to take some processing on the system the Agent represents and will return results at a later time. When complete, the output arguments are sent in a `Notify` (`OperationComplete`) request to any Controllers that have an active subscription to the operation and Object(s) to which it applies.

When a Controller using the Operate request specifies an operation that is defined as asynchronous, the Agent creates an instance of the Request Object in its data model, and includes a reference to the created Object in the Operate response. If the `send_resp` flag is `false`, the Controller doesn’t need the Request details, and intends to ignore it.

The lifetime of a Request Object expires when the operation is complete (either by success or failure). An expired Request Object is removed from the Instantiated Data Model.

**[R-OPR.0]{}** - When an Agent receives an Operate Request that addresses an asynchronous operation, it MUST create a Request Object in the Request table of its Instantiated Data Model (see the Device:2 Data Model [@TR-181]). When the Operation is complete (either success or failure), it MUST remove this Object from the Request table.

If any Controller wants a notification that an operation has completed, it creates a Subscription Object with the `NotificationType` set to `OperationComplete` and with the `ReferenceList` Parameter including a Path Name to the specified command. The Agent processes this Subscription when the operation completes and sends a Notify Message, including the `command_key` value that the Controller assigned when making the Operate request.

A Controller can cancel a request that is still present in the Agent's `Device.LocalAgent.Request.` table by invoking the `Device.LocalAgent.Request.{i}.Cancel()` command through another Operate Message.

![Operate Message Flow for Asynchronous Operations](asynchronous_operation.png)

#### Persistence of Asynchronous Operations

Synchronous Operations do not persist across a reboot or restart of the Agent or its underlying system. It is expected that  Asynchronous Operations do not persist, and a command that is in process when the Agent is rebooted can be expected to be removed from the Request table, and is considered to have failed. If a command is allowed or expected to be retained across a reboot, it will be noted in the command description.

### Operate Requests on Multiple Objects

Since the Operate request can take a Path Name expression as a value for the command field, it is possible to invoke the same operation on multiple valid Objects as part of a single Operate request. Responses to requests to Operate on more than one Object are handled using the `OperationResult` field type, which is returned as a repeated set in the Operate Response. The success or failure of the operation on each Object is handled separately and returned in a different `OperationResult` entry. For this reason, operation failures are never conveyed in an Error Message - in reply to an Operate request, Error is only used when the Message itself fails for one or more reasons, rather than the operation invoked.

*Note: This specification does not make any requirement on the order in which commands on multiple objects selected with a Path Name expression are executed.*

**[R-OPR.1]{}** - When processing Operate Requests on multiple Objects, an Agent MUST NOT send an Error Message due to a failed operation. It MUST instead include the failure in the `cmd_failure` field of the Operate response.

**[R-OPR.2]{}** - For asynchronous operations the Agent MUST create a separate Request Object for each Object and associated operation matched in the command field.

### Event Notifications for Operations

When an operation triggers an Event notification, the Agent sends the Event notification for all subscribed recipients as described in [](#sec:notifications-and-subscriptions).

### Concurrent Operations

If an asynchronous operation is triggered multiple times by one or more Controllers, the Agent has the following options:

1. Deny the new operation (with, for example, `7005 Resources Exceeded` )
2. The operations are performed in parallel and independently.
3. The operations are queued and completed in order.

**[R-OPR.3]{}** - When handling concurrently invoked operations, an Agent MUST NOT cancel an operation already in progress unless explicitly told to do so by a Controller with permission to do so (i.e., via the `Device.LocalAgent.Request.{i}.Cancel()` operation).

### Operate Examples

In this example of a synchronous command, the Controller requests that the Agent initiate the SendOnBoardRequest() operation defined in the `Device.LocalAgent.Controller.` Object.

```{filter=pbv}
header {
  msg_id: "42314"
  msg_type: OPERATE
}
body {
  request {
    operate {
      command: 'Device.LocalAgent.Controller.[EndpointID=="controller"].SendOnBoardRequest()'
      command_key: "onboard_command_key"
      send_resp: true
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "42314"
  msg_type: OPERATE_RESP
}
body {
  response {
    operate_resp {
      operation_results {
        executed_command: "Device.LocalAgent.Controller.1.SendOnBoardRequest()"
      }
    }
  }
}
```

In this example of an asynchronous command, the Controller requests that the Agent initiate the SelfDiagnostics() operation defined in the `Device.` object. 

```{filter=pbv}
header {
  msg_id: "42315"
  msg_type: OPERATE
}
body {
  request {
    operate {
      command: 'Device.SelfTestDiagnostics()'
      command_key: "selftest_command_key"
      send_resp: true
    }
  }
}
```

```{filter=pbv}
header {
  msg_id: "42315"
  msg_type: OPERATE_RESP
}
body {
  response {
    operate_resp {
      operation_results {
        executed_command: "Device.SelfTestDiagnostics()"
        req_obj_path: "Device.LocalAgent.Request.1"
      }
    }
  }
}
```

### The Operate Message {#sec:operate}

#### Operate Request Fields

`string command`

This field contains a Command Path or Search Path to an Object defined Operation in one or more Objects.

`string command_key`

This field contains a string used as a reference by the Controller to match the operation with notifications.

`bool send_resp`

This field lets the Controller indicate to Agent whether or not it expects a response in association with the operation request.

**[R-OPR.4]{}** - When `send_resp` is set to `false`, the target Endpoint SHOULD NOT send an `OperateResp` Message to the source Endpoint. If an error occurs during the processing of an `Operate` Message, the target Endpoint MAY send an `OperateResp` Message to the source Endpoint containing relevant `cmd_failure` elements. If a response is still sent, the responding Endpoint MUST expect that any such response will be ignored.

*Note: The requirement in the previous versions of the specification also discouraged the sending of an `Error` Message, however the Controller issuing the `Operate` might want to learn about and handle errors occurring during the processing of the `Operate` request but still ignore execution results.*

`map<string, string> input_args`

This field contains a map of key/value pairs indicating the input arguments (relative to the Command Path in the command field) to be passed to the method indicated in the command field.

**[R-OPR.5]{}** - A `Command` can have mandatory `input_args` as defined in the Supported Data Model. When a mandatory Input argument is omitted from the `input_args` field, the Agent MUST, in its `OperateResp`, include a `cmd_failure` element containg an `err_code` of type `7027` Invalid Command Arguments and stop processing the command.

**[R-OPR.6]{}** - When an unrecognized Input argument is included in the `input_args` field, the Agent MUST ignore the Input argument and continue processing the `Operate` Message.

**[R-OPR.7]{}** - When a non-mandatory Input argument is omitted from the `input_args` field, the Agent MUST use a default value for the missing Input argument and continue processing the `Operate` Message.

Refer to [](#sec:parameter-value-encoding) for details of how argument values are encoded as Protocol Buffers v3 strings.

#### Operate Response Fields

`repeated OperationResult operation_results`

This field contains a repeated set of `OperationResult` messages.

##### OperationResult Fields

`string executed_command`

This field contains a Command Path to the Object defined Operation that is the subject of this `OperateResp` message.

`oneof operate_resp`

This field contains a message of one of the following types.

```
  string req_obj_path
  OutputArgs req_output_args
  CommandFailure cmd_failure
```

###### Using req_obj_path

The req_obj_path field, when used as the `operate_resp`, contains an Object Instance Path to the Request Object created as a result of this asynchronous operation.

###### OutputArgs Fields

`map<string, string> output_args`

This field contains a map of key/value pairs indicating the output arguments (relative to the command specified in the `command` field) returned by the method invoked in the Operate Message.
Refer to [](#sec:parameter-value-encoding) for details of how argument values are encoded as Protocol Buffers v3 strings.

###### CommandFailure Fields

`fixed32 err_code`

This field contains a numeric code (see [](#sec:error-codes)) indicating the type of the error that caused the operation to fail.

`string err_msg`

This field contains additional (human readable) information about the reason behind the error.

#### Operate Message Error Codes
Appropriate error codes for the Operate Message include `7000-7008`, `7016`, `7022`, `7026`, `7027`, and `7800-7999`.

## Error Codes {#sec:error-codes}

USP uses error codes with a range 7000-7999 for both Controller and Agent errors. The errors appropriate for each Message (and how they must be implemented) are defined in the message descriptions below.

| Code | Name          | Applicability | Description                                    |
| :--- | :------------ | :------------ | :--------------------------------------------- |
| `7000` | Message failed	| Error Message | This error indicates a general failure that is described in an err_msg field. |
| `7001` | Message not supported | Error Message | This error indicates that the attempted message was not understood by the target Endpoint.|
| `7002` | Request denied (no reason specified) | Any | This error indicates that the target Endpoint cannot or will not process the message or operation. |
| `7003` | Internal error | Any | This error indicates that the message or operation failed due to internal hardware or software reasons. |
| `7004` | Invalid arguments | Any | This error indicates that the message or operation failed due to invalid values in the USP message. |
| `7005` | Resources exceeded | Any | This error indicates that the message or operation failed due to memory or processing limitations on the target Endpoint. |
| `7006` | Permission denied  | Any | This error indicates that the source Endpoint does not have the authorization for this action. |
| `7007` | Invalid configuration | Any | This error indicates that the message or operation failed because processing the message would put the target Endpoint in an invalid or unrecoverable state. |
| `7008` | Invalid path syntax | Any requested_path | This error indicates that the Path Name used was not understood by the target Endpoint. | 
| `7009` | Parameter action failed | Set | This error indicates that the Parameter failed to update for a general reason described in an err_msg field. |
| `7010` | Unsupported parameter | Add, Set | This error indicates that the requested Path Name associated with this ParamError or ParameterError did not match any instantiated Parameters. |
| `7011` | Invalid type | Add, Set | This error indicates that the received string can not be interpreted as a value of the correct type expected for the Parameter. |
| `7012` | Invalid value | Add, Set | This error indicates that the requested value was not within the acceptable values for the Parameter. |
| `7013` | Attempt to update non-writeable parameter | Add, Set | This error indicates that the source Endpoint attempted to update a Parameter that is not defined as a writeable Parameter. |
| `7014` | Value conflict | Add, Set | This error indicates that the requested value would result in an invalid configuration based on other Parameter values. |
| `7015` | Operation error | Add, Set, Delete | This error indicates a general failure in the creation, update, or deletion of an Object that is described in an err_msg field.
| `7016` | Object does not exist | Any | This error indicates that the requested Path Name did not address an Object in the Agent's Instantiated Data Model. |
| `7017` | Object could not be created | Add | This error indicates that the operation failed to create an instance of the specified Object. |
| `7018` | Object is not a table | Add, GetInstances | This error indicates that the requested Path Name is not a Multi-Instance Object. |
| `7019` | Attempt to create non-creatable object | Add | This error indicates that the source Endpoint attempted to create an Object that is not defined as able to be created. |
| `7020` | Object could not be updated | Set | This error indicates that the requested Object in a Set request failed to update. |
| `7021` | Required parameter failed | Add, Set | This error indicates that the request failed on this Object because one or more required Parameters failed to update. Details on the failed Parameters are included in an associated ParamError or ParameterError message. |
| `7022` | Command failure | Operate | This error indicates that an command initiated in an Operate Request failed to complete for one or more reasons explained in the err_msg field. |
| `7023` | Command canceled | Operate | This error indicates that an asynchronous command initiated in an Operate Request failed to complete because it was cancelled using the Cancel() operation. |
| `7024` | Delete failure | Delete | This error indicates that this Object Instance failed to be deleted. |
| `7025` | Object exists with duplicate key | Add, Set | This error indicates that an Object already exists with the Unique Keys specified in an Add or Set Message. |
| `7026` | Invalid path | Any | This error indicates that the Object, Parameter, or Command Path Name specified does not match any Objects, Parameters, or Commands in the Agent's Supported Data Model |
| `7027` | Invalid command arguments | Operate | This error indicates that an Operate Message failed due to invalid or unknown arguments specified in the command. |
| `7028` | Register failure | Register | This error indicates that a path in a Register Request failed to be registered for one or more reasons explained in the err_msg field. |
| `7029` | Already in use | Register | This error indicates that a path in a Register Request failed to be registered, because it was registered by a different USP Agent |
| `7030` | Deregister failure | Deregister | This error indicates that a path in a Deregister Request failed to be deregistered for one or more reasons explained in the err_msg field. |
| `7031` | Path already registered | Deregister | This error indicates that a path in a Deregister Request failed to be deregistered, because it was registered by a different USP Agent. |
| `7100-7199` | USP Record error codes | - | These errors are listed and described in [](#sec:usp-record-errors). |
| `7200-7299`| Data model defined error codes | - | These errors are described in the data model. |
| `7800-7999`| Vendor defined error codes | - | These errors are described in [](#sec:vendor-defined-error-codes). |

### Vendor Defined Error Codes {#sec:vendor-defined-error-codes}

Implementations of USP MAY specify their own error codes for use with Errors and Responses. These codes use the `7800-7999` series. There are no requirements on the content of these errors.
