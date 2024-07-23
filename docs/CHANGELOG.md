<!-- do not edit! this file was created from PROJECT.yaml by project-parser.py -->

# TR-369: User Services Platform Change Log

See <https://usp.technology> for the current USP specification.

## 2024-07-23: [Release 1.4][TR-369 Amendment 4]

*Tags: [v1.4.0] (USP specification), 
       [v1.4.0][usp-data-models-v1.4.0] (data models)*

### TR-369 Document
Release contains the specification for the User Services Platform 1.4

* Updated ResolvedPathResult Fields to clarify that R-GET.4 does not return parameters for which the Controller
  does not have Read permission for.
* Added Appendix VI Usage of the Register Operation to define the Rules related to USP Services Registering data model paths.
* Added TLS Support to the UDS MTP impacting Section Handling Failures to Deliver USP Records with new requirements
  (R-UDS.23a and R-UDS.23b) and updates to Appendix V1 Basic Solution Concepts.
* Expanded Error Codes Section Applicability to multiple error codes from Error Message to Any, to send an
  operate response rather than USP error.
* Updated GetSupportedDM Request Fields Section to expand the Register Message for Commands, Events, and Parameters. Updated
  Definitions Section with new definitions for Command Path and Event Path.
* Updated R-OPR.4 and R-OPR.5 to align with R-OPR.1.
* Updated Appendix 1 Basic Solution Concepts Section to define that the Execution Environment is no longer static,
  and is managed via USP Software Module Management.
* Updated Handling of WebSocket Frames Section adding R-WS.14b to discourage the use of WebSocket fragmentation.
* Updated Handling of the WebSocket Session Section adding note to R-WS.8 to clarify the encoding of USP Endpoint ID
  for URI use.
* Opened up the OUI definition and Use of authorityscheme and authorityid Section R-ARC.2a to allow for not only the old
  24-bit OUIs but to also allow for 36-bit OUIs.
* Updated OnBoardRequest Section to state that the OnBoardRequest notification MUST be sent with send_resp=true,
  which included updates to R-NOT.5 and R-NOT-6 as well as the addition of R-NOT-6a to insure the
  Controller retries until a notification response is recieved.
* Defined the term "Partial Path" in Definitions Section.
* Fixed the Operate example in Operate Examples Section to include both sync and async data model commands.
* Updated the GetSupportedDM to now indicate the unique keys of a table, which caused updates to the
  examples in GetSupportedDM Examples Section and the usp-msg-1-4.proto file within the GetSupportedDM message.
* Updated Role Definition Section with clarifications to Role permissions applying to Supported and Instantiated
  Data model and the Secured Role as applying to "secured" parameter in the path(s), with examples
  of both.

### USP Protocol Buffers Schemas
USP v1.4 Record Schema

USP v1.4 Message Schema
* Added unique_key_set to GetSupportedDM

## 2023-10-20: [Release 1.3.1][TR-369 Amendment 3 Corrigendum 1]

*Tags: [v1.3.1] (USP specification), 
       [v1.3.0][usp-data-models-v1.3.0] (data models didn't change)*

### TR-369 Document
This Corrigendum has the following fixes
* Fix example by populating the empty UNIX Domain Socket references
* Small fixes to UDS example images
* Fix UnixDomainSocket path in example

## 2023-06-14: [Release 1.3][TR-369 Amendment 3]

*Tags: [v1.3.0] (USP specification), 
       [v1.3.0][usp-data-models-v1.3.0] (data models)*

### TR-369 Document
Release contains the specification for the User Services Platform 1.3

* Adds Appendix VI, "Software Modularization and USP-Enabled
  Applications Theory of Operation"
* Adds new Unix Domain Socket MTP
* Adds two new messages, "Register" and "Deregister", and associated
  error codes (primarily for use with Appendix VI but can be
  used in many scenarios)
* Adds new Software Module Management features
* Adds a note about the use of the new TriggerAction parameter in
  Subscription objects
* Updates "Authentication and Authorization" to include the use of
  new SecuredRole
* Updates the Add message to allow for Search Paths and clarifies the
  application of permissions during Add messages
* Obsoletes CoAP as an MTP
* Adds two new requirements regarding Unique Key immutability
* Clarifies how Set should respond when using a Search Path where one
  or more objects fail to update
* Updates the use of EndpointID in WebSocket arguments
  and adds an fqdn authority scheme
* Addesses a potential attack vector with using MQTT, and updates other
  MQTT behavior
* Updates Annex A to explain use of the "Exclude" parameter
* Updates Discovery to include the use of DHCP options for agent-device
  association
* Adds a note about USP protocol versioning and Controller/Agent
  behavior
* Clarifies and updates the use of certain error codes
* Clarifies the behavior of Get messages when asking for specific
  Multi-Instance Objects that don't exist
* Clarifies some behavior when responding via USP Records
* Updates message flow diagrams to remove the implication of ordered
  responses
* Adds new requirement R-SEC.4b for Trusted Brokers

### USP Protocol Buffers Schemas
USP v1.3 Record Schema
* Adds UDSConnectRecord

USP v1.3 Message Schema
* Adds Register and Deregister messages

## 2022-01-27: [Release 1.2][TR-369 Amendment 2]

*Tags: [v1.2.0] (USP specification), 
       [v1.2.0][usp-data-models-v1.2.0] (data models)*

### TR-369 Document
Release contains specification for the User Services Platform 1.2

* Clarify the expected responses in result of an `Operate` message
  (R-OPR.4)
* Deprecates the use of COAP as an MTP
* GetSupportedDM
  - now provides the data types for parameter values
  - now allows the Agent to provide information about whether or not
    it will ignore ValueChange subscriptions on a given parameter
  - now provides information about whether a command is synchronous
    vs. asynchronous
  - now allows requests on specific object instances and handles
    divergent data models
* Defines discovery mechanisms for Endpoints connected to STOMP and
  MQTT brokers
* Clarifies the use of search paths vs. unique key addressing in the
  Add message
* Clarifies the use of required parameters and defaults for unique
  keys in the Add message
* Annex A
  - now provides a theory of operations for use of the USPEventNotif
    mechanism for bulk data collection using the Push! event
  - defines a new bulk data collection over MQTT mechanism
* DHCP discovery mechanism now provides a Controller Endpoint ID to
  the Agent
* Enhances ease of use and clarifies requirements for use of TLS in
  USP Record integrity
* New USP records
  - adds USP connect and disconnect records for use independent of
    MTP
  - adds USP Record specific error mechanism and error codes
  - MQTT and STOMP no longer silently drop errors; they now report
    errors in the USP Record.
  - USP Records can now include an empty payload
* Get requests
  - can now include a max_depth flag to limit response size
  - Get response format has been clarified to return separate
    elements for sub-object
* Clarifies the requirements around processing an entire message in
  the event of a failed operation when allow_partial is true vs.
  false
* Clarifies the response behavior for Get, Set, and Delete when
  using a path that matches no instances
* Fixes and enhances the use of error codes for the Operate message
* Clarifies and updates Controller credential/authentication theory
  of operations and flow diagrams
* Clarifies the use of subjectAltName in certificates
* Clarifies R-E2E.4
* Deprecated and Obsolete terms are now defined in the References and
  Terminology section
* Updated R-E3E.43
* Deprecates R-MSG.2
* Deprecates R-E2E.2
* R-E2E.42 now makes TLS renegotiation forbidden
* Modifies R-NOT.9 and adds R-NOT.10 adjusting how the Agent and
  Controller should handle the subscription_id field

Corresponds to
[TR-106 Amendment 11](https://github.com/BroadbandForum/data-model-template/releases/tag/v1.11.0) and
[TR-181 Issue 2 Amendment 15](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.2.0)

### USP Protocol Buffers Schemas
USP v1.2 Record Schema
* Added Connect and Disconnect Record Types

USP v1.2 Message Schema
* Added max_depth as a new input argument to the Get message
* Enhanced the GetSupportedDM response to allow return of parameter
  types, parameters that will be ignored for value change
  notifications, divergent object paths, and command types

## 2020-11-18: Release 1.1.4

*Tags: [v1.1.4] (USP specification), 
       [v1.1.2][usp-data-models-v1.1.2] (data models didn't change)*

Corresponds to [TR-181 Issue 2 Amendment 14 Corrigendum 1](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.4)

## 2020-11-05: Release 1.1.3

*Tags: [v1.1.3] (USP specification), 
       [v1.1.2][usp-data-models-v1.1.2] (data models didn't change)*

Corresponds to [TR-106 Amendment 10](https://github.com/BroadbandForum/data-model-template/releases/tag/v1.10.0) and
[TR-181 Issue 2 Amendment 14](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.3)

## 2020-08-04: Release 1.1.2

*Tags: [v1.1.2] (USP specification), 
       [v1.1.2][usp-data-models-v1.1.2] (data models)*

Clarifies several examples, requirements, and error types

## 2020-04-06: Release 1.1.1

*Tags: [v1.1.1] (USP specification), 
       [v1.1.0][usp-data-models-v1.1.0] (data models didn't change)*

Regenerated data model HTML using fixed version of the BBF report tool

## 2019-10-18: [Release 1.1][TR-369 Amendment 1]

*Tags: [v1.1.0] (USP specification), 
       [v1.1.0][usp-data-models-v1.1.0] (data models)*

### TR-369 Document
Release contains specification for the User Services Platform 1.1

* Adds MQTT support as a Message Transfer Protocol
* Adds a theory of operations for IoT control using USP Agents
* Clarifications on protocol functions, error messages, and updates
  to examples

Corresponds to [TR-181 Issue 2 Amendment 13](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.0)

### USP Protocol Buffers Schemas
USP v1.1 Record Schema (no changes from v1.0)

USP v1.1 Message Schema (no changes from v1.0)

## 2018-11-01: [Release 1.0.2][TR-369 Corrigendum 2]

*Tags: [v1.0.2] (USP specification), 
       [v1.0.2][usp-data-models-v1.0.2] (data models)*

### TR-369 Document
* Typographical and example fixes

## 2018-08-02: [Release 1.0.1][TR-369 Corrigendum 1]

*Tags: [v1.0.1] (USP specification), 
       [v1.0.1][usp-data-models-v1.0.1] (data models)*

### TR-369 Document
* Added examples and clarifications to end-to-end messaging, use of
  endpoint ID, typographical fixes

## 2018-04-17: [Release 1.0][TR-369 Issue 1]

*Tags: [v1.0.0] (USP specification), 
       [v1.0.0][usp-data-models-v1.0.0] (data models)*

### TR-369 Document
Release contains specification for the User Services Platform 1.0

Corresponds to [TR-181 Issue 2 Amendment 12](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.0.0)

### USP Protocol Buffers Schemas
USP v1.0 Record Schema

USP v1.0 Message Schema

[TR-369 Amendment 1]: https://www.broadband-forum.org/download/TR-369_Amendment-1.pdf
[TR-369 Amendment 2]: https://www.broadband-forum.org/download/TR-369_Amendment-2.pdf
[TR-369 Amendment 3]: https://www.broadband-forum.org/download/TR-369_Amendment-3.pdf
[TR-369 Amendment 3 Corrigendum 1]: https://www.broadband-forum.org/download/TR-369_Amendment-3_Corrigendum-1.pdf
[TR-369 Amendment 4]: https://www.broadband-forum.org/download/TR-369_Amendment-4.pdf
[TR-369 Corrigendum 1]: https://www.broadband-forum.org/download/TR-369_Corrigendum-1.pdf
[TR-369 Corrigendum 2]: https://www.broadband-forum.org/download/TR-369_Corrigendum-2.pdf
[TR-369 Issue 1]: https://www.broadband-forum.org/download/TR-369_Issue-1.pdf
[usp-data-models-v1.0.0]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.0.0
[usp-data-models-v1.0.1]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.0.1
[usp-data-models-v1.0.2]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.0.2
[usp-data-models-v1.1.0]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.0
[usp-data-models-v1.1.2]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.2
[usp-data-models-v1.2.0]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.2.0
[usp-data-models-v1.3.0]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.3.0
[usp-data-models-v1.4.0]: https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.4.0
[v1.0.0]: https://github.com/BroadbandForum/usp/releases/tag/v1.0.0
[v1.0.1]: https://github.com/BroadbandForum/usp/releases/tag/v1.0.1
[v1.0.2]: https://github.com/BroadbandForum/usp/releases/tag/v1.0.2
[v1.1.0]: https://github.com/BroadbandForum/usp/releases/tag/v1.1.0
[v1.1.1]: https://github.com/BroadbandForum/usp/releases/tag/v1.1.1
[v1.1.2]: https://github.com/BroadbandForum/usp/releases/tag/v1.1.2
[v1.1.3]: https://github.com/BroadbandForum/usp/releases/tag/v1.1.3
[v1.1.4]: https://github.com/BroadbandForum/usp/releases/tag/v1.1.4
[v1.2.0]: https://github.com/BroadbandForum/usp/releases/tag/v1.2.0
[v1.3.0]: https://github.com/BroadbandForum/usp/releases/tag/v1.3.0
[v1.3.1]: https://github.com/BroadbandForum/usp/releases/tag/v1.3.1
[v1.4.0]: https://github.com/BroadbandForum/usp/releases/tag/v1.4.0
