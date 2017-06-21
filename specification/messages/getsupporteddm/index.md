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

# The GetSupportedDM Message

GetSupportedDM is used to retrieve the Objects, Parameters, Events, and Commands in the Agent's Supported Data Model. This allows a Controller to learn what an Agent understands, rather than its current state.

The GetSupportedDM is different from other USP messages in that it deals exclusively with the Agent's Supported Data Model. This means that Path Names to Multi-Instance Objects only address the Object itself, rather than Instances of the Object, and those Path Names that contain Multi-Instance objects in the Path use the `{i}` identifier to indicate their place in the Path Name.

For example, a Path Name to the `AssociatedDevice` Object (a child of the `.Wifi.AccessPoint` Object) would be addressed in the Supported Data Model as:

`Device.Wifi.AccessPoint.{i}.AssociatedDevice.` or `Device.Wifi.AccessPoint.{i}.AssociatedDevice.{i}.`

Both of these syntaxes are supported and equivalent. The Agent's Response returns the Path Name to the Object in the associated Device Type document as specified in [TR-106][3].

For example, the Controller wishes to learn the Wifi capabilities the Agent represents. It could issue a GetSupportedDM Request as:

    GetSupportedDM {
      discover_obj_list {
        obj_path : Device.Wifi.
        next_level : false
        return_commands : true
        return_events : true
        return_params : true
      }
    }

The Agent's Response would be:

    GetSupportedDMResp {
      req_obj_result_list {
        req_obj_path : Device.Wifi.
        err_code : 0
        err_msg :
        data_model_inst_uri : urn:broadband-forum-org:tr-181-2-12-0
        supported_obj_list {
          supported_obj_path : Device.Wifi.
          access : READ_ONLY (0)
          is_multi_instance : false
          supported_param_list {
            param_name : RadioNumberOfEntries
            access : READ_ONLY (0)

            param_name : SSIDNumberOfEntries
            access : READ_ONLY (0)

            param_name : AccessPointNumberOfEntries
            access : READ_ONLY (0)

            param_name : EndPointNumberOfEntries
            access : READ_ONLY (0)
          }
          supported_command_list {
            command_name : SomeCommand()
            input_arg_name_list {
              SomeArgument1
              SomeArgument2
            }
            output_arg_name_list {
              SomeArgument1
              SomeArgument2
            }
          }
          supported_event_list {
            event_name : SomeEvent!
            arg_name_list {
              SomeArgumentA
              SomeArgumentB
            }
          }
          supported_obj_path : Device.Wifi.SSID.{i}.
          access : ADD_DELETE (1)
          is_multi_instance : true
          supported_param_list {
            param_name : Enable
            access : READ_WRITE (1)

            param_name: Status
            access : READ_ONLY (0)

            param_name : Alias
            access : READ_WRITE (1)

            param_name : Name
            access : READ_ONLY (0)

            param_name: LastChange
            access : READ_ONLY (0)

            param_name : LowerLayers
            access : READ_WRITE (1)

            param_name : BSSID
            access : READ_ONLY (0)

            param_name : MACAddress                    
            access : READ_ONLY (0)

            param_name : SSID
            access : READ_WRITE (1)
          }
          supported_command_list {
            command_name : SomeCommand()
            input_arg_name_list {
              SomeArgument1
              SomeArgument2
            }
            output_arg_name_list {
              SomeArgument1
              SomeArgument2
            }
          }
          supported_event_list {
            event_name : SomeEvent!
            arg_name_list {
              SomeArgumentA
              SomeArgumentB
            }
          }                

    // And continued, for Objects such as Device.Wifi.SSID.{i}.Stats., Device.Wifi.Radio.{i}, Device.Wifi.AccessPoint.{i}, Device.Wifi.AccessPoint.{i}.AssociatedDevice.{i}, etc.
      }
    }

## GetSupportedDM Request Elements

`repeated DiscoverObject discover_obj_list`

This element contains a repeated set of messages of type `DiscoverObject`.

### DiscoverObject Elements

`string obj_path`

This element contains a Path Name to an Object (not an Object Instance) in the Agent's Supported Data Model.

`bool next_level`

This element, if `true`, indicates that the Agent should return only those objects matched by the Path Name or Search Path in `obj_path` and its immediate (i.e., next level) child objects.

`bool return_commands`

This element, if `true`, indicates that the Agent should include a supported_command_list element containing Commands supported by the reported Object(s).

`bool return_events`

This element, if `true`, indicates that the Agent should include a supported_event_list element containing Events supported by the reported Object(s).

`bool return_params`

This element, if `true`, indicates that the Agent should include a supported_param_list element containing Parameters supported by the reported Object(s).

## GetSupportedDMResp Elements

`repeated RequestedObjectResult req_obj_result_list`

This element contains a repeated set of messages of type `RequestedObjectResult`.

### RequestedObjectResult Elements

`string req_obj_path`

This element contains one of the Path Names given in `obj_path` of the associated GetSupportedDM Request.

`fixed32 err_code`

This element contains a [numeric code](/usp/specification/error-codes/) indicating the type of error that caused the Get to fail on this path. A value of 0 indicates the path could be read successfully.

**R-GSP.0** - If the Controller making the Request does not have Read permission on an Object or Parameter matched through the `requested_path` element, the Object or Parameter MUST be treated as if it is not present in the Agent’s instantiated data model.

`string err_msg`

This element contains additional information about the reason behind the error.

`string data_model_inst_uri`

This element contains a Uniform Resource Identifier (URI) to the Data Model associated with the Object specified in `obj_path`.

`repeated SupportedObjectResult supported_obj_list`

The element contains a message of type `SupportedObjectResult` for each reported Object.

#### SupportedObjectResult Elements

`string supported_obj_path`

This element contains the Path Name of the reported Object.

`ObjAccessType access`

The element contains an enumeration of type ObjAccessType specifying the access permissions that are specified for this Object in the Agent's Supported Data Model. This usually only applies to Multi-Instance Objects. This may be further restricted to the Controller based on rules defined in the Agent's [Access Control List](addref). It is an enumeration of:

    OBJ_READ_ONLY (0)
    OBJ_ADD_DELETE (1)
    OBJ_ADD_ONLY (2)
    OBJ_DELETE_ONLY (3)

`bool is_multi_instance`

This element, if `true`, indicates that the reported Object is a Multi-Instance Object.

`repeated SupportedParamResult supported_param_list`

The element contains a message of type `SupportedParamResult` for each Parameter supported by the reported Object.

`repeated SupportedCommandResult supported_command_list`

The element contains a message of type `SupportedCommandResult` for each Command supported by the reported Object.

`repeated SupportedEventResult supported_event_list`

The element contains a message of type `SupportedEventResult` for each Event supported by the reported Object.

##### SupportedParamResult Elements

`string param_name`

This element contains the local name of the Parameter.

`ParamAccessType access`

The element contains an enumeration of type ParamAccessType specifying the access permissions that are specified for this Parameter in the Agent's Supported Data Model. This may be further restricted to the Controller based on rules defined in the Agent's [Access Control List](addref). It is an enumeration of:

    PARAM_READ_ONLY (0)
    PARAM_READ_WRITE (1)
    PARAM_WRITE_ONLY (2)

##### SupportedCommandResult Elements

`string command_name`

This element contains the local name of the Command.

`repeated string input_arg_name_list`

This element contains a repeated set of local names for the input arguments of the Command.

**R-GSP.1** - If any input arguments are multi-instance, the Agent MUST report them using Instance Number Addressing.

`repeated string output_arg_name_list`

This element contains a repeated set of local names for the output arguments of the Command.

**R-GSP.2** - If any output arguments are multi-instance, the Agent MUST report them using Instance Number Addressing.

##### SupportedEventResult

`string event_name`

This element contains the local name of the Event.

`repeated string arg_name_list`

This element contains a repeated set of local names for the arguments of the Event.

**R-GPS.3** - If any arguments are multi-instance, the Agent MUST report them using Instance Number Addressing.

## GetSupportedDM Error Codes

Appropriate error codes for the GetSupportedDM message include `7000-7006`, `7008`, `7016`, and `7800-7999`.

*Note - when using error `7016` (Object Does Not Exist), it is important to note that in the context of GetSupportedDM this applies to the Agent's Supported Data Model.*
