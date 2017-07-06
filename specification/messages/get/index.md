<!-- Reference Links -->
[1]:	https://github.com/BroadbandForum/tree/master/data-model "TR-181 Issue 2 Device Data Model for TR-069"
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

# The Get Message

The basic Get message is used to retrieve the values of a set of Object’s parameters in order to learn an Agent’s current state. It takes a set of search paths as an input and returns the complete tree of parameters, plus the parameters of all sub-Objects, of any Object matched by the specified expressions. The search paths specified in a Get request can also target individual parameters within Objects to be returned.

*Note: Those familiar with Broadband Forum [TR-069][2] will recognize this behavior as the difference between “partial paths” and “complete paths”. This behavior is replicated in USP for the Get message for each path that is matched by the expression(s) supplied in the request.*

*Note: Each search path is intended to be evaluated separately, and the results from a given search path are returned in an element dedicated to that path. As such, it is possible that the same information may be returned from more than one search path. This is intended, and the Agent should treat each search path atomically.*

The response returns an entry for each Path Name resolved by the path given in `requested_path`. If a path expression specified in the request does not match any valid parameters or Objects, the response will indicate that this expression was an “invalid path”, indicating that the Object or parameter does not currently exist in the Agent’s Instantiated Data Model.

For each resolved Path Name, a `ResolvedPathResult` message is given in the Response. This ResolvedPathResult contains the `resolved_path`, followed by a list of parameters of both the resolved_path Object and all of its sub-objects, plus their values. These Parameter Paths are Relative Paths to the `resolved_path`.

For example, a Controller wants to read the data model to learn the settings and stats of a single Wifi SSID, “HomeNetwork” with a BSSID of 00:11:22:33:44:55. It could use a Get request with the following elements:

    Get {
      param_path_list {
        Device.Wifi.SSID.[SSID="Homenetwork", BSSID=00:11:22:33:44:55].
      }
    }
In response to this request the Agent returns all parameters, plus sub-Objects and their parameters, of the addressed instance. The Agent returns this data in the Get response using an element for each of the requested paths. In this case:

    GetResp {
        req_path_result_list {
        requested_path: Device.Wifi.SSID.[SSID="Homenetwork",BSSID=00:11:22:33:44:55].
        err_code : 0
        err_msg :
        resolved_path_result_list {
          resolved_path : Device.Wifi.SSID.1.
          result_parm_map {		
            key: Enable
            value: True

            key: Status
            value: Up

            key: Name
            value: “Home Network”

            key: LastChange
            value: 864000

            key: BSSID
            value: 00:11:22:33:44:55

            key: Stats.BytesSent
            value: 24901567

            key: Stats.BytesReceived
            value: 892806908296

            etc.
          }
        }
      }

In another example, the Controller only wants to read the current status of the Wifi network with the SSID “HomeNetwork” with the BSSID of 00:11:22:33:44:55. It could use a Get request with the following elements:

    Get {
      param_path_list {
        Device.Wifi.SSID.[SSID=”Homenetwork”,BSSID=00:11:22:33:44:55].Status
      }
    }

In response to this request the Agent returns only the Status parameter and its value.

    GetResp {
      req_path_result_list {
        requested_path: Device.Wifi.SSID.[SSID=”Homenetwork”,BSSID=00:11:22:33:44:55].Status
        err_code : 0
        err_msg :
        resolved_path_result_list {
          resolved_path : Device.Wifi.SSID.1.
          result_parm_map {
            key: Status
            value: Up
          }
        }
      }
    }

Lastly, using wildcards or another Search Path, the requested path may resolve to more than one resolved path. For example for a Request sent to an Agent with two `Wifi.SSID` instances:

```
    Get {
      param_path_list {
        Device.Wifi.SSID.*.Status
      }
    }
```

The Agent's GetResponse would be:

```
    GetResp {
      req_path_result_list {
        requested_path: Device.Wifi.SSID.*.
        err_code : 0
        err_msg :
        resolved_path_result_list {
          resolved_path : Device.Wifi.SSID.1.
          result_parm_map {
            key: Status
            value: Up
          }

          resolved_path :Device.Wifi.SSID.2.
          result_param_map {
              key: Status
              value: Up
          }
        }
      }
    }
```

## Get Request Elements

`repeated string param_path_list`

This element is a set of Object Paths, Instance Paths, Parameter Paths, or Search Paths to Objects, Object Instances, and Parameters in an Agent’s Instantiated Data Model.

## Get Response Elements

`repeated RequestedPathResult req_path_result_list`

A repeated set of `RequestedPathResult` messages for each of the Path Names given in the associated Get request.

### RequestedPathResult Element

`string requested_path`

This element contains one of the Path Names or Search Paths given in the `param_path` element of the associated Get Request.

`fixed32 err_code`

This element contains a [numeric code](/specification/error-codes/) indicating the type of error that caused the Get to fail on this path. A value of 0 indicates the path could be read successfully.

**R-GET.0** - If the Controller making the Request does not have Read permission on an Object or Parameter matched through the `requested_path` element, the Object or Parameter MUST be treated as if it is not present in the Agent’s instantiated data model.

`string err_msg`

This element contains additional information about the reason behind the error.

`repeated ResolvedPathResult resolved_path_result_list`

This element contains one message of type ResolvedPathResult for each path resolved by the Path Name or Search Path given by `requested_path`.

#### ResolvedPathResult Elements

`string resolved_path`

This element contains a Path Name to an Object or Object Instance that was resolved from the Path Name or Search Path given in `requested_path`.

**R-GET.1** - If the `requested_path` included a Path Name to a Parameter, the `resolved_path` MUST contain only the Path Name to the parent Object or Object Instance of that parameter.

`map<string, string> result_param_map`

This element contains a set of mapped key/value pairs listing a Parameter Path (relative to the Path Name in `resolved_path`) to each of the parameters and their values, plus sub-objects and their values, of the Object given in `resolved_path`.

**R-GET.2** - If the `requested_path` included a Path Name to a Parameter, `result_param_map` MUST contain only the Parameter included in that path.

**R-GET.3** - If the Controller does not have Read permission on any of the parameters specified in `result_param_map`, these parameters MUST NOT be returned in this element. This MAY result in this element being empty.

**R-GET.4** - Path Names containing Object Instance Paths in the keys of `result_param_map` MUST be addressed using Instance Number Addressing.

#### Get Message Supported Error Codes

Appropriate error codes for the Get message include `7000-7006`, `7008`, `7010`, and `7800-7999`.

[<-- The Delete Message](/specification/messages/delete/)
[The GetInstances Message -->](/specification/messages/getinstances/)
