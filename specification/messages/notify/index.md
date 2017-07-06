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

# The Notify Message

<a id="notify" />

### Using Subscription Objects

Subscriptions are maintained in instances of the Multi-Instance Subscription Object in the USP data model. The normative requirements for these Objects are described in the data model parameter descriptions for `Device.Subscription.{i}.` in [Device:2][1].

**R-NOT.0** - The Agent and Controller MUST follow the normative requirements defined in the `Device.Subscription.{i}.` Object specified in [Device:2][1].

*Note: Those familiar with Broadband Forum [TR-069][2] will recall that a notification for a value change caused by an Auto-Configuration Server (ACS - the CWMP equivalent of a Controller) are not sent to the ACS. Since there is only a single ACS notifying the ACS of value changes it requested is unnecessary. This is not the case in USP: an Agent should follow the behavior specified by a subscription, regardless of the originator of that subscription.*

#### ReferenceList Parameter

All subscriptions apply to one or more Objects or parameters in the Agent’s Instantiated Data Model. These are specified as Path Names or Search Paths in the `ReferenceList` parameter. The `ReferenceList` parameter may have different meaning depending on the nature of the notification subscribed to.

For example, a Controller wants to be notified when a new Wifi station joins the Wifi network. It uses the Add message to create a subscription Object instance with `Device.WiFi.AccessPoint.1.AssociatedDevice.` specified in the `ReferenceList` parameter and `ObjectCreation` as the `NotificationType`.

In another example, a Controller wants to be notified whenever an outside source changes the SSID of a Wifi network. It uses the Add message to create a subscription Object instance with `Device.Wifi.SSID.1.SSID` specified in the `ReferenceList` and `ValueChange` as the `NotificationType`.

#### Responses to Notifications and Notification Retry

The Notify request contains a flag, `send_resp`, that specifies whether or not the Controller should send a response message after receiving a Notify request. This is used in tandem with the `NotificationRetry` parameter in the subscription Object - if `NotificationRetry` is `true`, then the Agent sends its Notify requests with `send_resp : true`, and the Agent considers the notification delivered when it receives a response from the Controller. If `NotificationRetry` is `false`, the Agent does not need to use the `send_resp` flag and should ignore the delivery state of the notification.

If `NotificationRetry` is `true`, and the Agent does not receive a response from the Controller, it begins retrying using the retry algorithm below. The subscription Object also uses a `NotificationExpiration` parameter to specify when this retry should end if no success is ever achieved.

**R-NOT.1** - When retrying notifications, the Agent MUST use the following retry algorithm to manage the retransmission of the Notify request.

The retry interval range is controlled by two Parameters, the minimum wait interval and the interval multiplier, each of which corresponds to a data model Parameter, and which are described in the table below. The factory default values of these Parameters MUST be the default values listed in the Default column. They MAY be changed by a Controller with the appropriate permissions at any time.

| Descriptive Name | Symbol | Default | Data Model Parameter Name |
| ---------: | :-----: | :------: | :------------ |
|Minimum wait interval | m | 5 seconds |	`Device.Controller.{i}.USPRetryMinimumWaitInterval` |
| Interval multiplier |	k | 2000 | `Device.Controller.{i}.USPRetryIntervalMultiplier` |

| Retry Count | Default Wait Interval Range (min-max seconds) | Actual Wait Interval Range (min-max seconds) |
| ----------: | :---------: | :-------------- |
| #1 | 5-10 | m - m.(k/1000) |
| #2 | 10-20 | m.(k/1000) - m.(k/1000)2 |
| #3 | 20-40 | m.(k/1000)2 - m.(k/1000)3 |
| #4 | 40-80 | m.(k/1000)3 - m.(k/1000)4 |
| #5 | 80-160 | m.(k/1000)4 - m.(k/1000)5 |
| #6 | 160-320 | m.(k/1000)5 - m.(k/1000)6 |
| #7 | 320-640 | m.(k/1000)6 - m.(k/1000)7 |
| #8 | 640-1280 | m.(k/1000)7 - m.(k/1000)8 |
| #9 | 1280-2560 | m.(k/1000)8 - m.(k/1000)9 |
| #10 and subsequent | 2560-5120 | m.(k/1000)9 - m.(k/1000)10 |

**R-NOT.2** - Beginning with the tenth retry attempt, the Agent MUST choose from the fixed maximum range. The Agent will continue to retry a failed notification until it is successfully delivered or until the `NotificationExpiration` time is reached.

**R-NOT.3** - Once a notification is successfully delivered, the Agent MUST reset the retry count to zero for the next notification message.

**R-NOT.4** - If a reboot of the Agent occurs, the Agent MUST reset the retry count to zero for the next notification message.

#### Notification Types

There are several types events that can cause a Notify request. These include those that deal with changes to the Agent’s Instantiated Data Model (`ValueChange`, `ObjectCreation`, `ObjectDeletion`), the completion of an asynchronous Object-defined operation (`OperationComplete`), a policy-defined `OnBoardRequest`, and a generic `Event` for use with Object-defined events.

##### ValueChange

The `ValueChange` notification is subscribed to by a Controller when it wants to know that the value of a single or set of parameters has changed from the state it was in at the time of the subscription or to a state as described in an expression, and then each time it transitions from then on for the life of the subscription. It is triggered when the defined change occurs, even if it is caused by the originating Controller.

#####	 ObjectCreation and ObjectDeletion
These notifications are used for when an instance of the subscribed to Multi-Instance Objects is added or removed from the Agent’s Instantiated Data Model. Like `ValueChange`, this notification is triggered even if the subscribing Controller is the originator of the creation or deletion.

The `ObjectCreation` notification also includes the Object’s unique keys and their values as data in the notification.

##### OperationComplete

The `OperationComplete` notification is used to indicate that an asynchronous Object-defined operation finished (either successfully or unsuccessfully). These operations may also trigger other Events defined in the data model (see below).

##### OnBoardRequest

An `OnBoardRequest` notification is used by the Agent when it is triggered by an external source to initiate the request in order to communicate with a Controller that can provide on-boarding procedures and communicate with that Controller (likely for the first time).

**R-NOT.5** - An Agent MUST send an `OnBoardRequest` notify request in the following circumstances:

1.	When the `SendOnBoardRequest()` command is executed. This sends the notification request to the Controller that is the subject of that operation. The `SendOnBoardRequest()` operation is defined in the [Device:2 Data Model for TR-069 Devices and USP Agents][1].

2.	When instructed to do so by internal application policy (for example, when using DHCP discovery defined above).

*Note: as defined in the Subscription table, OnBoardRequest is not included as one of the enumerated types of a Subscription, i.e., it is not intended to be the subject of a Subscription.*

Further policy defines whether an OnBoardRequest requires a Notify Response.

##### Event
The `Event` notification is used to indicate that an Object-defined event was triggered on the Agent. These events are defined in the data model and include what parameters, if any, are returned as part of the notification.

## Notify Request Elements

`string subscription_id`

This element contains the locally unique opaque identifier that was set by the Controller when it created the Subscription on the Agent.

**R-NOT.6** - The `subscription_id` element MUST contain the Subscription ID of the Subscription Object that triggered this notification.

`bool send_resp`

This element lets the Agent indicate to the Controller whether or not it expects a response in association with the Notify request.

**R-NOT.7** - When `send_response` is set to false, the Controller SHOULD NOT send a response or error to the Agent. If a response is still sent, the responding Controller MUST expect that any such response will be ignored.

`oneof notification`

Contains one of the following Notification messages:

    Event	event
    ValueChange value_change
    ObjectCreation obj_creation
    ObjectDeletion obj_deletion
    OperationComplete oper_complete
    OnBoardRequest on_board_req

### Event Elements

`string obj_path`

This element contains the Object or Object Instance Path of the Object that caused this event (for example, `Device.LocalAgent.`).

**R-NOT.8** - Path Names containing Object Instances in the `obj_path` element of the Event notification MUST be addressed using Instance Number Addressing.

`string event_name`

This element contains the name of the Object defined event that caused this notification (for example, `Boot!`).

`map<string, string> parameter_map`

This element contains a set of key/value pairs of parameters associated with this event.

**R-NOT.9** - Any values in `parameter_map` whose keys contain Object Paths to Multi-Instance Objects MUST be addressed by Instance Number.

### ValueChange Elements

`string param_path`

This element contains the Path Name of the changed parameter.

**R-NOT.10** - Path Names containing Object Instances in the `param_path` element of the ValueChange notification MUST be addressed using Instance Number Addressing.

`string param_value`

This element contains the value of the parameter specified in `param_path`.

### ObjectCreation Elements

`string obj_path`

This element contains the Path Name of the created Object instance.

**R-NOT.11** - Path Names containing Object Instances in the `obj_path` element of the ObjectCreation notification MUST be addressed using Instance Number Addressing.

`map<string, string> unique_key_map`

This element contains a map of key/value pairs for all supported parameters that are part of any of this Object's unique keys.

### ObjectDeletion Elements

`string obj_path`

This element contains the Path Name of the deleted Object instance.

**R-NOT.12** - Path Names containing Object Instances in the `obj_path` element of the ObjectDeletion notification MUST be addressed using Instance Number Addressing.

### OperationComplete Elements

`string command_name`

This element contains the local name l of the Object defined command that caused this notification (i.e., `Download()`).

`string obj_path`

This element contains the Object or Object Instance Path to the Object that contains this operation.

**R-NOT.13** - Path Names containing Object Instances in the `obj_path` element of the OperationComplete notification MUST be addressed using Instance Number Addressing.

`string command_key`

This element contains the command key set during an Object defined Operation that caused this notification.

`oneof operation_resp`

Contains one of the following messages:

    OutputArgs req_output_args
    CommandFailure cmd_failure

#### OutputArgs Elements

`map<string, string> output_arg_map`

This element contains a map of key/value pairs indicating the output arguments (relative to the command specified in the `command_name` element) returned by the method invoked in the Operate message.

**R-NOT.14** - Any key in the `output_arg_map` that contains multi-instance arguments MUST use Instance Number Addressing.

#### CommandFailure Elements

`fixed32 err_code`

This element contains the [error code](/specification/messages/error-codes/) of the error that caused the operation to fail. Appropriate error codes for CommandFailure include `7002-7008`, `7016`, `7022`, `7023`, and `7800-7999`.

`string err_msg`

This element contains additional (human readable) information about the reason behind the error.

### OnBoardRequest Elements

`string obj_path`

This element contains the Path Name of the Object associated with this notification.

**R-NOT.15** - Path Names containing Object Instances in the `obj_path` element of the OnBoardRequest notification MUST be addressed using Instance Number Addressing.

## Notify Response Elements

`string subscription_id`

This element contains the locally unique opaque identifier that was set by the Controller when it created the Subscription on the Agent.

**R-NOT.16** - The `subscription_id` element MUST contain the Subscription ID of the Subscription Object that triggered this notification. If the `subscription_id` element does not contain the Subcription ID of the Subscription Object that triggered this notification, this Response MUST be ignored and not considered valid for the purpose of calculating notification retries.

## Notify Error Codes

Appropriate error codes for the Notify message include `7000-7006`, and `7800-7999`.

[<-- The Operate Message](/specification/messages/operate/)
[Error Codes -->](/specification/messages/error-codes/)
