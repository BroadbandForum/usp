# Bulk Data Collection {.annex1}

*Note:  This Annex has been re-written in the 1.2 version of the USP specification to include the previously-defined USP Event Notification aspects of Bulk Data Collection and the new MQTT aspects of Bulk Data Collection, in addition to the already defined HTTP Bulk Data Collection mechanism.*

This section discusses the Theory of Operation for USP specific mechanisms related to the collection and transfer of bulk data using either HTTP, MQTT, or USP Event Notifications.  This includes an explanation of how the Agent can be configured to enable the collection of bulk data using HTTP, MQTT, or USP Event Notifications via the BulkData Objects, which are defined in the Device:2 Data Model [@TR-181].

## Introduction

The general concept behind the USP Bulk Data collection mechanism is that a USP Controller can configure an Agent to consistently deliver a bulk data report at a specific interval. For large CPE populations, this is a more efficient mechanism when compared to the alternative of polling each individual CPE for the data. There are four key aspects of configuring the bulk data collection mechanism on an Agent:

* **What data needs to be collected** :: The set of Object/Parameter Path Names that dictate the set of Parameters that will be included in each Bulk Data report.  Anything included in this set should be considered a filter that is applied against the Instantiated Data Model at the time of report generation, which means that the generation of the report is not contingent upon the Path Name being present in the Instantiated Data Model at the time of report generation.

* **How often does the data need to be collected** :: The interval and time reference that dictates the frequency and cycle of report generation. For example,  the interval could be set to 15 minutes while the time reference could be set to 42 minutes past 1 AM, which would mean that the report is generated every 15 minutes at 42 past the hour, 57 past the hour, 12 past the hour, and 27 past the hour.

* **Where does the data need to be sent** :: The destination of where the report needs to be delivered after it has been generated.  This is specific to the Bulk Data collection mechanism being used: HTTP vs MQTT vs USP Event Notification.

* **How does the data get sent** :: The protocol used to send the data across the wire, the encoding of the data, and the format of the data. From a Protocol perspective, the HTTP Bulk Data collection mechanism utilizes either the HTTP or HTTPS protocols, the MQTT Bulk Data Collection mechanism utilizes the MQTT protocol, and the USPEventNotif Bulk Data collection mechanism utilizes the existing USP communications channel related to the USP Controller that owns the bulk data profile. From a data encoding perspective, both Bulk Data collection mechanisms support the *CSV* and *JSON* options as described later. From a data formatting perspective, both Bulk Data collection mechanisms support the *Object Hierarchy* and *Name Value Pair* report formats, also described later.

The Bulk Data collection mechanism is configured within an Agent by creating a Bulk Data Profile.  A Bulk Data Profile defines the configuration of the four key aspects (as mentioned above) for a given Bulk Data Report.  Meaning, the Bulk Data Profile defines the protocol to use (HTTP vs MQTT vs USPEventNotif), the data encoding to use (CSV vs JSON), the report format to use (Object Hierarchy vs Name Value Pair), the destination of the report, the frequency of the report generation, and the set of Parameters to include in the report. Furthermore, the Bulk Data Profile has a `Controller` Parameter that is a read-only Parameter and is set by the Agent based on the Controller that created the Bulk Data Profile.  The Controller Parameter represents the owner of the Profile, which is used when determining permissions. When the Agent generates the Bulk Data Report it uses the permissions associated with the referenced Controller to determine what is included in the Report (Objects and Parameters that fail the permissions check are simply filtered out of the Report).

*Note:  When a Bulk Data Collection Profile is either created or updated the Agent performs validation checks for the associated Objects and Parameters against the Supported Data Model at the time of the operation.*

*Note:  When a Bulk Data Collection Report is generated the Agent performs permission checks for the associated Objects and parameters against the Instantiated Data Model, filtering out any Object instances or Parameters that are not present at that time.*


## HTTP Bulk Data Collection
The Bulk Data Collection mechanism that utilizes an out-of-band HTTP/HTTPS communications mechanism for delivering the Bulk Data Report.

### Enabling HTTP/HTTPS Bulk Data Communication

HTTP/HTTPS communication between the Agent and Bulk Data Collector is enabled by either configuring an existing `BulkData.Profile` Object Instance for the HTTP/HTTPS transport protocol or adding and configuring a new `BulkData.Profile` Object Instance using the [Add Message](#sec:add). For example:

    .BulkData.Profile.1
    .BulkData.Profile.1.Enable=true
    .BulkData.Profile.1.Protocol = "HTTP"
    .BulkData.Profile.1.ReportingInterval = 300
    .BulkData.Profile.1.TimeReference = "0001-01-01T00:00:00Z"
    .BulkData.Profile.1.HTTP.URL =  "https://bdc.acme.com/somedirectory"
    .BulkData.Profile.1.HTTP.Username = "username"
    .BulkData.Profile.1.HTTP.Password = "password"
    .BulkData.Profile.1.HTTP.Method = "POST"
    .BulkData.Profile.1.HTTP.UseDateHeader = true

The configuration above defines a profile that transfers data from the Agent to the Bulk Data Collector using secured HTTP. In addition the Agent will provide authentication credentials (username, password) to the Bulk Data Collector, if requested by the Bulk Data Collector. Finally, the Agent establishes a communication session with the Bulk Data Collector every 300 seconds in order to transfer the data defined by the `.BulkData.Report.` Object Instance.

Once the communication session is established between the Agent and Bulk Data Collector the data is transferred from the Agent using the POST HTTP method with a HTTP Date header and no compression.

**[R-BULK.0]{}** - In many scenarios Agents will utilize "chunked" transfer encoding. As such, the Bulk Data Collector MUST support the HTTP transfer-coding value of "chunked".

### Use of the URI Query Parameters

The HTTP Bulk Data transfer mechanism allows Parameters to be used as HTTP URI query parameters. This is useful when Bulk Data Collector utilizes the specific parameters that the Agent reports for processing (e.g., logging, locating directories) without the need for the Bulk Data Collector to parse the data being transferred.

**[R-BULK.1]{}** - The Agent MUST transmit the device's Manufacturer OUI, Product Class and Serial Number or the USP Endpoint ID as part of the URI query parameters. The data model Parameters are encoded as:

    .DeviceInfo.ManufacturerOUI -> oui
    .DeviceInfo.ProductClass  -> pc
    .DeviceInfo.SerialNumber  -> sn
    .LocalAgent.EndpointID -> eid

As such, the values of the device’s OUI, Serial Number and Product Class are formatted in the HTTP request URI as follows:

    POST https://<bulk data collector url>?oui=00256D&pc=Z&sn=Y

If the USP Endpoint ID is used the HTTP request URI is formatted as:

    POST https://<bulk data collector url>?eid=os::000256:asdfa99384

*Note:  If the USP Endpoint ID should be transmitted together with the device's Manufacturer OUI, Product Class and Serial Number (e.g. to distinguish multiple bulk data collection instances on the same device), then the USP Endpoint ID has to be configured as additional URI parameter in the `.BulkData.Profile.{i}.HTTP.RequestURIParameter.{i}.` table.*

Configuring the URI query parameters for other Parameters requires that instances of a `.BulkData.Profile.{i}.HTTP.RequestURIParameter.{i}.` Object Instance be created and configured with the requested parameters. The additional parameters are appended to the required URI query parameters.

Using the example to add the device's current local time to the required URI parameters, the HTTP request URI would be as follows:

    POST https://<bulk data collector url>?oui=00256D&pc=Z&sn=Y&ct=2015-11-01T11:12:13Z

By setting the following Parameters using the Add Message as follows:

    .BulkData.Profile.1.HTTP.RequestURIParameter 1.Name ="ct"
    .BulkData.Profile.1.HTTP.RequestURIParameter.1.Reference ="Device.Time.CurrentLocalTime"

### Use of HTTP Status Codes

The Bulk Data Collector uses standard HTTP status codes, defined in the HTTP specification, to inform the Agent whether a bulk data transfer was successful.  The HTTP status code is set in the response header by the Bulk Data Collector.  For example, "`200 OK`" status code indicates an upload was processed successfully, "`202 Accepted`" status code indicates that the request has been accepted for processing, but the processing has not been completed, "`401 Unauthorized`" status code indicates user authentication failed and a "`500 Internal Server Error`" status code indicates there is an unexpected system error.

#### HTTP Retry Mechanism

**[R-BULK.2]{}** - When the Agent receives an unsuccessful HTTP status code and the HTTP retry behavior is enabled, the Agent MUST try to redeliver the data. The retry mechanism employed for the transfer of bulk data using HTTP uses the same algorithm as is used for [USP Notify retries](#sec:responses-and-retry).

The retry interval range is controlled by two Parameters, the minimum wait interval and the interval multiplier, each of which corresponds to a data model Parameter, and which are described in the table below. The factory default values of these Parameters MUST be the default values listed in the Default column. They MAY be changed by a Controller with the appropriate permissions at any time.

| Descriptive Name | Symbol | Default | Data Model Parameter Name |
| ---------: | :-----: | :------: | :------------ |
|Minimum wait interval | m | 5 seconds |	`Device.BulkData.Profile.{i}.HTTP.RetryMinimumWaitInterval` |
| Interval multiplier |	k | 2000 | `Device.BulkData.Profile.{i}.HTTP.RetryIntervalMultiplier` |

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

**[R-BULK.3]{}** - Beginning with the tenth retry attempt, the Agent MUST choose from the fixed maximum range. The Agent will continue to retry a failed bulk data transfer until it is successfully delivered or until the next reporting interval for the data transfer becomes effective.

**[R-BULK.4]{}** - Once a bulk data transfer is successfully delivered, the Agent MUST reset the retry count to zero for the next reporting interval.

**[R-BULK.5]{}** - If a reboot of the Agent occurs, the Agent MUST reset the retry count to zero for the next bulk data transfer.

#### Processing of Content for Failed Report Transmissions

When the content (report) cannot be successfully transmitted, including retries, to the data collector, the `NumberOfRetainedFailedReports` Parameter of the `BulkData.Profile` Object Instance defines how the content should be disposed based on the following rules:

*	When the value of the `NumberOfRetainedFailedReports` Parameter is greater than `0`, then the report for the current reporting interval is appended to the list of failed reports. How the content is appended is dependent on the type of encoding (e.g., CSV, JSON) and is described further in corresponding encoding section.
*	If the value of the `NumberOfRetainedFailedReports` Parameter is `-1`, then the Agent will retain as many failed reports as possible.
*	If the value of the NumberOfRetainedFailedReports Parameter is `0`, then failed reports are not to be retained for transmission in the next reporting interval.
*	If the Agent cannot retain the number of failed reports from previous reporting intervals while transmitting the report of the current reporting interval, then the oldest failed reports are deleted until the Agent is able to transmit the report from the current reporting interval.
*	If the value `BulkData.Profile` Object Instance’s `EncodingType` Parameter is modified any outstanding failed reports are deleted.

### Use of TLS and TCP

The use of TLS to transport the HTTP Bulk Data is RECOMMENDED, although the protocol MAY be used directly over a TCP connection instead. If TLS is not used, some aspects of security are sacrificed. Specifically, TLS provides confidentiality and data integrity, and allows certificate-based authentication in lieu of shared secret-based authentication.

**[R-BULK.6]{}** - Certain restrictions on the use of TLS and TCP are defined as follows:

*	The Agent MUST support TLS version 1.2 or later (with backward compatibility to TLS 1.2).
*	If the Collection Server URL has been specified as an HTTPS URL, the Agent MUST establish secure connections to the Collection Server, and MUST start the TLS session negotiation with TLS 1.2 or later.

*Note:  If the Collection Server does not support TLS 1.2 or higher with a cipher suite supported by the Agent, it may not be possible for the Agent to establish a secure connection to the Collection Server.*

*Note:  TLS_RSA_WITH_AES_128_CBC_SHA is the only mandatory TLS 1.2 cipher suite.*

*	The Agent SHOULD use the [@RFC6066] Server Name TLS extension to send the host portion of the Collection Server URL as the server name during the TLS handshake.
*	If TLS 1.2 (or a later version) is used, the Agent MUST authenticate the Collection Server using the certificate provided by the Collection Server. Authentication of the Collection Server requires that the Agent MUST validate the certificate against a root certificate. To validate against a root certificate, the Agent MUST contain one or more trusted root certificates that are either pre-loaded in the Agent or provided to the Agent by a secure means outside the scope of this specification. If as a result of an HTTP redirect, the Agent is attempting to access a Collection Server at a URL different from its pre-configured Collection Server URL, the Agent MUST validate the Collection Server certificate using the redirected Collection Server URL rather than the pre-configured Collection Server URL.
*	If the host portion of the Collection Server URL is a DNS name, this MUST be done according to the principles of RFC 6125 [@RFC6125], using the host portion of the Collection Server URL as the reference identifier.
*	If the host portion of the Collection Server URL is an IP address, this MUST be done by comparing the IP address against any presented identifiers that are IP addresses.

*Note:  the terms "reference identifier" and "presented identifier" are defined in RFC 6125 [@RFC6125].*

*Note:  wildcard certificates are permitted as described in RFC 6125 [@RFC6125].*

*	An Agent capable of obtaining absolute time SHOULD wait until it has accurate absolute time before contacting the Collection Server. If a Agent for any reason is unable to obtain absolute time, it can contact the Collection Server without waiting for accurate absolute time. If a Agent chooses to contact the Collection Server before it has accurate absolute time (or if it does not support absolute time), it MUST ignore those components of the Collection Server certificate that involve absolute time, e.g. not-valid-before and not-valid-after certificate restrictions.
*	Support for Agent authentication using client-side certificates is NOT RECOMMENDED.  Instead, the Collection Server SHOULD authenticate the Agent using HTTP basic or digest authentication to establish the identity of a specific Agent.

### Bulk Data Encoding Requirements

When utilizing the HTTP Bulk Data collection option, the encoding type is sent as a media type within the report. For CSV the media type is `text/csv` as specified in RFC 4180 [@RFC4180] and for JSON the media type is `application/json` as specified in RFC 7159 [@RFC7159]. For example, a CSV encoded report using `charset=UTF-8` would have the following Content-Type header:

    Content-Type: text/csv; charset=UTF-8

**[R-BULK.7]{}** - The "`media-type`" field and "`charset`" Parameters MUST be present in the Content-Type header.

In addition the report format that was used for encoding the report is included as an HTTP custom header with the following format:

    BBF-Report-Format: <ReportFormat>

The <ReportFormat> field is represented as a token.

For example a CSV encoded report using a ReportFormat for ParameterPerRow would have the following BBF-Report-Format header:

    BBF-Report-Format: "ParameterPerRow"

**[R-BULK.8]{}** - The BBF-Report-Format custom header MUST be present when transferring data to the Bulk Data Collector from the Agent using HTTP/HTTPS.


## MQTT Bulk Data Collection
The Bulk Data Collection mechanism that utilizes an out-of-band MQTT communications mechanism for delivering the Bulk Data Report.

### Enabling MQTT Bulk Data Communication

Bulk Data communications that utilizes MQTT for transferring the Bulk Data Report between the Agent and a Bulk Data Collector, is enabled by either configuring an existing `BulkData.Profile` Object Instance for the MQTT transport protocol or adding and configuring a new `BulkData.Profile` Object Instance using the [Add Message](#sec:add). For example:

    .BulkData.Profile.1
    .BulkData.Profile.1.Enable = true
    .BulkData.Profile.1.Name = "MQTT Profile 1"
    .BulkData.Profile.1.Protocol = "MQTT"
    .BulkData.Profile.1.EncodingType = "JSON"
    .BulkData.Profile.1.ReportingInterval = 300
    .BulkData.Profile.1.TimeReference = "0001-01-01T00:00:00Z"
    .BulkData.Profile.1.MQTT.Reference =  "Device.MQTT.Client.1"
    .BulkData.Profile.1.MQTT.PublishTopic = "/bulkdata"
    .BulkData.Profile.1.MQTT.PublishQoS = 1
    .BulkData.Profile.1.MQTT.PublishRetain = false

The configuration above defines a profile that transfers data from the Agent to a Bulk Data Collector via the MQTT protocol.  The Agent utilizes the referenced MQTT Client instance to determine the MQTT broker for this Bulk Data Collection Profile.  The Agent sends the Bulk Data Report to the reference MQTT Broker by issuing an MQTT PUBLISH message to the PublishTopic every 300 seconds (ReportingInterval).  The Bulk Data Collector would subscribe to the PublishTopic in order to receive the Bulk Data Reports.

### Determining Successful Transmission

Delivering a Bulk Data Collection report using MQTT means that successful transmission of the report is tied to the successful delivery of the MQTT PUBLISH message, which is determined by the PublishQoS configured as part of the Bulk Data Collection Profile.

#### Retrying Failed Transmissions

Delivering a Bulk Data Collection report using MQTT means that any failed transmissions are retried based on the referenced MQTT Client and the associated QoS value contained within the MQTT PUBLISH message, which is determined by the PublishQoS parmater.  Furthermore, the CleanSession (MQTT 3.1 and MQTT 3.1.1) and CleanStart (MQTT 5.0) flags determine if unacknowledged PUBLISH messages are re-delivered on client reconnect.  For MQTT 3.1 there is also the MessageRetryTime defined in the referenced MQTT Client that determines how frequently an unacknowledged PUBLISH message should be retried.

#### Processing of Content for Failed Report Transmissions

When the content (report) cannot be successfully transmitted, including retries, to the MQTT broker, the `NumberOfRetainedFailedReports` Parameter of the `BulkData.Profile` Object Instance defines how the content should be disposed based on the following rules:

*	When the value of the `NumberOfRetainedFailedReports` Parameter is greater than `0`, then the report for the current reporting interval is appended to the list of failed reports. How the content is appended is dependent on the type of encoding (e.g., CSV, JSON) and is described further in corresponding encoding section.
*	If the value of the `NumberOfRetainedFailedReports` Parameter is `-1`, then the Agent will retain as many failed reports as possible.
*	If the value of the NumberOfRetainedFailedReports Parameter is `0`, then failed reports are not to be retained for transmission in the next reporting interval.
*	If the Agent cannot retain the number of failed reports from previous reporting intervals while transmitting the report of the current reporting interval, then the oldest failed reports are deleted until the Agent is able to transmit the report from the current reporting interval.
*	If the value `BulkData.Profile` Object Instance’s `EncodingType` Parameter is modified any outstanding failed reports are deleted.

### Bulk Data Encoding Requirements

When utilizing the MQTT Bulk Data collection option with a MQTT 5.0 Client connection, the encoding type is sent as a media type within the MQTT PUBLISH message header and the Content Type property. For CSV the media type is `text/csv` as specified in RFC 4180 [@RFC4180] and for JSON the media type is `application/json` as specified in RFC 7159 [@RFC7159]. For example, a CSV encoded report using `charset=UTF-8` would have the following Content Type property:

    text/csv; charset=UTF-8

**[R-BULK.8a]{}** - The "`media-type`" field and "`charset`" parameters MUST be present in the Content Type property when using MQTT 5.0.

When utilizing the MQTT Bulk Data collection option with a MQTT 3.1 or MQTT 3.1.1 client connection, the encoding type is not sent in the MQTT PUBLISH message; instead the receiving Bulk Data Collector will need to know how the `.BulkData.Profile` Object Instance is configured.

In addition the data layout is not included in the MQTT PUBLISH message; instead the receiving Bulk Data Collector will need to know how the `.BulkData.Profile.{i}.CSVEncoding.ReportFormat` or `.BulkData.Profile.{i}.JSONEncoding.ReportFormat` Parameter is configured.


## USPEventNotif Bulk Data Collection
The Bulk Data Collection mechanism that utilizes the existing USP communications channel for delivering the Bulk Data Report via a [Notify Message](#sec:notify) that contains a Push! Event.

### Enabling USPEventNotif Bulk Data Communication

Bulk Data communications using a USP Event notification that utilizes the [Notify Message](#sec:notify) between the Agent and a Controller, acting as a Bulk Data Collector, is enabled by either configuring an existing `BulkData.Profile` Object Instance for the USPEventNotif transport protocol or adding and configuring a new `BulkData.Profile` Object Instance using the [Add Message](#sec:add). For example:

    .BulkData.Profile.1
    .BulkData.Profile.1.Enable = true
    .BulkData.Profile.1.Name = "USP Notif Profile 1"
    .BulkData.Profile.1.Protocol = "USPEventNotif"
    .BulkData.Profile.1.EncodingType = "JSON"
    .BulkData.Profile.1.ReportingInterval = 300
    .BulkData.Profile.1.TimeReference = "0001-01-01T00:00:00Z"

The configuration above defines a profile that transfers data from the Agent to a Controller that is acting as the Bulk Data Collector.  The Controller that receives an Event notification is dictated by the Agent's currently defined Subscriptions [](#sec:notifications-and-subscriptions). The Agent utilizes the existing communications session with the Controller acting as the Bulk Data Collector every 300 seconds in order to transfer the data defined by the `.BulkData.Profile` Object Instance.

The data is transferred from the Agent using the USP Notify Message and a `.BulkData.Profile.1.Push!` Event notification.

### Determining Successful Transmission

Delivering a Bulk Data Collection report using the USP Notify Message and a `.BulkData.Profile.1.Push!` Event notification means that successful transmission of the report is tied to the successful delivery of the notification itself [](#sec:responses-and-retry).

#### Retrying Failed Transmissions

Delivering a Bulk Data Collection report using the USP Notify Message and a `.BulkData.Profile.1.Push!` Event notification means that any failed transmissions are retried based on the notification retry requirements [R-NOT.1]() through [R-NOT.4]() [](#sec:responses-and-retry).

Furthermore, the `NumberOfRetainedFailedReports` Parameter of the `BulkData.Profile` Object Instance does not pertain to the USPEventNotif Bulk Data Collection mechanism as each report is wholly contained within a USP Notify Message.  This means that the notification retry mechanism will determine the life of each individual failed report, and that each reporting interval will generate a new report that is delivered via a new USP Notify Message.

### Bulk Data Encoding Requirements

When utilizing the USPEventNotif Bulk Data collection option, the encoding type is not sent in the USP Event notification; instead the receiving Controller will need to know how the `.BulkData.Profile` Object Instance is configured.

In addition the data layout is not included in the USP Event notification; instead the receiving Controller will need to know how the `.BulkData.Profile.{i}.CSVEncoding.ReportFormat` or `.BulkData.Profile.{i}.JSONEncoding.ReportFormat` Parameter is configured.


## Using Wildcards to Reference Object Instances in the Report

When the Agent supports the use of the Wildcard value "\*"  in place of instance identifiers for the Reference Parameter, then all Object Instances of the referenced Parameter are encoded. For example to encode the "`BroadPktSent`" Parameter for all Object Instances of the MoCA Interface Object the following will be configured:

```
    .BulkData.Profile.1.Parameter.1.Name =  ""
    .BulkData.Profile.1.Parameter.1.Reference =  "Device.MoCA.Interface.*.Stats.BroadPktSent"
```

## Using Alternative Names in the Report

Alternative names can be defined for the Parameter name in order to shorten the name of the Parameter. For example instead of encoding the full Parameter name "`Device.MoCA.Interface.1.Stats.BroadPktSent`" could be encoded with a shorter name "`BroadPktSent`". This allows the encoded data to be represented using the shorter name. This would be configured as:

    .BulkData.Profile.1.Parameter.1.Name =  "BroadPktSent"
    .BulkData.Profile.1.Parameter.1.Reference =  "Device.MoCA.Interface.1.Stats.BroadPktSent"

In the scenario where there are multiple instances of a Parameter (e.g., "`Device.MoCA.Interface.1.Stats.BroadPktSent`", "`Device.MoCA.Interface.2.Stats.BroadPktSent`") in a Report, the content of the Name parameter SHOULD be unique (e.g., `BroadPktSent.1`, `BroadPktSent.2`).

#### Using Object Instance Wildcards and Parameter Partial Paths with Alternative Names

Wildcards for Object Instances can be used in conjunction with the use of alternative names by reflecting Object hierarchy of the value of the Reference Parameter in the value of the Name Parameter.

**[R-BULK.9]{}** - When the value of the Reference Parameter uses a wildcard for an instance identifier, the value of the Name Parameter (as used in a report) MUST reflect the wild-carded instance identifiers of the Parameters being reported on.  Specifically, the value of the Name Parameter MUST be appended with a period (.) and then the instance identifier. If the value of the Reference Parameter uses multiple wildcard then each wild-carded instance identifier MUST be appended in order from left to right.

For example, for a device to report the Bytes Sent for the Associated Devices of the device's Wi-Fi Access Points the following would be configured:

    .BulkData.Profile.1.Parameter.1.Name =  "WiFi_AP_Assoc_BSent"
    .BulkData.Profile.1.Parameter.1.Reference = "Device.WiFi.AccessPoint.*.AssociatedDevice.*.Stats.BytesSent"

Using this configuration a device that has 2 Wi-Fi Access Points (with instance identifiers `1` and `3`) each with 2 Associated Devices (with instance identifiers `10` and `11`), would contain a Report with following Parameter names:

    WiFi_AP_Assoc_BSent.1.10
    WiFi_AP_Assoc_BSent.1.11
    WiFi_AP_Assoc_BSent.3.10
    WiFi_AP_Assoc_BSent.3.11

Object or Object Instance Paths can also be used to report all Parameters of the associated Object.

**[R-BULK.10]{}** - When the value of the Reference Parameter is an Object Path, the value of the Name Parameter (as used in a report) MUST reflect the remainder of the Parameter Path. Specifically, the value of Name Parameter MUST be appended with a "." and then the remainder of the Parameter Path.

For example, for a device to report the statistics of a Wi-Fi associated device Object Instance the following would be configured:

    .BulkData.Profile.1.Parameter.1.Name = "WiFi_AP1_Assoc10"
    .BulkData.Profile.1.Parameter.1.Reference = "Device.WiFi.AccessPoint.1.AssociatedDevice.10.Stats."

Using the configuration the device's report would contain the following Parameter names:

    WiFi_AP1_Assoc10.BytesSent
    WiFi_AP1_Assoc10.BytesReceived
    WiFi_AP1_Assoc10.PacketsSent
    WiFi_AP1_Assoc10.PacketsReceived
    WiFi_AP1_Assoc10.ErrorsSent
    WiFi_AP1_Assoc10.RetransCount
    WiFi_AP1_Assoc10.FailedRetransCount
    WiFi_AP1_Assoc10.RetryCount
    WiFi_AP1_Assoc10.MultipleRetryCount

It is also possible for the value of the Reference Parameter to use both wildcards for instance identifiers and be a partial Path Name. For example, for device to report the statistics for the device's Wi-Fi associated device, the following would be configured:

    .BulkData.Profile.1.Parameter.1.Name = "WiFi_AP_Assoc"
    .BulkData.Profile.1.Parameter.1.Reference = "Device.WiFi.AccessPoint.*.AssociatedDevice.*.Stats."

Using this configuration a device that has 1 Wi-Fi Access Point (with instance identifier `1`) with 2 Associated Devices (with instance identifiers `10` and `11`), would contain a Report with following Parameter names:

    WiFi_AP_Assoc.1.10.BytesSent
    WiFi_AP_Assoc.1.10.BytesReceived
    WiFi_AP_Assoc.1.10.PacketsSent
    WiFi_AP_Assoc.1.10.PacketsReceived
    WiFi_AP_Assoc.1.10.ErrorsSent
    WiFi_AP_Assoc.1.10.RetransCount
    WiFi_AP_Assoc.1.10.FailedRetransCount
    WiFi_AP_Assoc.1.10.RetryCount
    WiFi_AP_Assoc.1.10.MultipleRetryCount
    WiFi_AP_Assoc.1.11.BytesSent
    WiFi_AP_Assoc.1.11.BytesReceived
    WiFi_AP_Assoc.1.11.PacketsSent
    WiFi_AP_Assoc.1.11.PacketsReceived
    WiFi_AP_Assoc.1.11.ErrorsSent
    WiFi_AP_Assoc.1.11.RetransCount
    WiFi_AP_Assoc.1.11.FailedRetransCount
    WiFi_AP_Assoc.1.11.RetryCount
    WiFi_AP_Assoc.1.11.MultipleRetryCount


## Encoding of Bulk Data

### Encoding of CSV Bulk Data

**[R-BULK.11]{}** - CSV Bulk Data SHOULD be encoded as per RFC 4180 [@RFC4180], MUST contain a header line (column headers), and the media type MUST indicate the presence of the header line.

For example: `Content-Type: text/csv; charset=UTF-8; header=present`

In addition, the characters used to separate fields and rows as well as identify the escape character can be configured from the characters used in RFC 4180 [@RFC4180].

Using the HTTP example above, the following configures the Agent to transfer data to the Bulk Data Collector using CSV encoding, separating the fields with a comma and the rows with a new line character, by setting the following Parameters:

    .BulkData.Profile.1.EncodingType =  "CSV"
    .BulkData.Profile.1 CSVEncoding.FieldSeparator = ","
    .BulkData.Profile.1.CSVEncoding.RowSeparator="&#13;&#10;"
    .BulkData.Profile.1.CSVEncoding.EscapeCharacter="&quot;"

#### Defining the Report Layout of the Encoded Bulk Data

The layout of the data in the reports associated with the profiles allows Parameters to be formatted either as part of a column (`ParameterPerColumn`) or as a distinct row (`ParameterPerRow`) as defined below. In addition, the report layout allows rows of data to be inserted with a timestamp stating when the data is collected.

Using the HTTP example above, the following configures the Agent to format the data using a Parameter as a row and inserting a timestamp as the first column entry in each row using the "Unix-Epoch" time. The information is configured by setting the following Parameters:

    .BulkData.Profile.1.CSVEncoding.ReportFormat ="ParameterPerRow"
    .BulkData.Profile.1.CSVEncoding.RowTimestamp ="Unix-Epoch"

**[R-BULK.12]{}** - The report format of "`ParameterPerRow`" MUST format each Parameter using the `ParameterName`, `ParameterValue` and `ParameterType` in that order.

**[R-BULK.13]{}** - The `ParameterType` MUST be the Parameter's base data type as described in TR-106 [@TR-106].

#### Layout of Content for Failed Report Transmissions

*Note: This is only relevant for the HTTP variant of Bulk Data Collection.*

When the value of the `NumberOfRetainedFailedReports` Parameter of the `BulkData.Profile` Object Instance is `-1` or greater than `0`, then the report of the current reporting interval is appended to the failed reports. For CSV Encoded data the content of new reporting interval is added onto the existing content without any header data.

#### CSV Encoded Report Examples

##### CSV Encoded Reporting Using ParameterPerRow Report Format

Using the configuration examples provided in the previous sections the configuration for a CSV encoded HTTP report using the `ParameterPerRow` report format:

    .BulkData.Profile.1
    .BulkData.Profile.1.Enable=true
    .BulkData.Profile.1.Protocol = "HTTP"
    .BulkData.Profile.1.ReportingInterval = 300
    .BulkData.Profile.1.TimeReference = "0001-01-01T00:00:00Z"
    .BulkData.Profile.1.HTTP.URL =  "https://bdc.acme.com/somedirectory"
    .BulkData.Profile.1.HTTP.Username = "username"
    .BulkData.Profile.1.HTTP.Password = "password"
    .BulkData.Profile.1.HTTP.Compression = "Disabled"
    .BulkData.Profile.1.HTTP.Method = "POST"
    .BulkData.Profile.1.HTTP.UseDateHeader = true
    .BulkData.Profile.1.EncodingType =  "CSV"
    .BulkData.Profile.1 CSVEncoding.FieldSeparator = ","
    .BulkData.Profile.1.CSVEncoding.RowSeparator="&#13;&#10;"
    .BulkData.Profile.1.CSVEncoding.EscapeCharacter="&quot;"
    .BulkData.Profile.1.CSVEncoding.ReportFormat ="ParameterPerRow"
    .BulkData.Profile.1.CSVEncoding.ReportTimestamp ="Unix-Epoch"
    .BulkData.Profile.1.Parameter.1.Name =  ""
    .BulkData.Profile.1.Parameter.1.Reference =  "Device.MoCA.Interface.1.Stats.BroadPktSent"
    .BulkData.Profile.1.Parameter.2.Name =  ""
    .BulkData.Profile.1.Parameter.2.Reference =  "Device.MoCA.Interface.1.Stats.BytesReceived"
    .BulkData.Profile.1.Parameter.3.Name =  ""
    .BulkData.Profile.1.Parameter.3.Reference =  "Device.MoCA.Interface.1.Stats.BytesSent"
    .BulkData.Profile.1.Parameter.4.Name =  ""
    .BulkData.Profile.1.Parameter.4.Reference =  "Device.MoCA.Interface.1.Stats.MultiPktReceived"


The resulting CSV encoded data would look like:

    ReportTimestamp,ParameterName,ParameterValue,ParameterType
    1364529149,Device.MoCA.Interface.1.Stats.BroadPktSent,25248,unsignedLong
    1364529149,Device.MoCA.Interface.1.Stats.BytesReceived,200543250,unsignedLong
    1364529149, Device.MoCA.Interface.1.Stats.Stats.BytesSent,7682161,unsignedLong
    1364529149,Device.MoCA.Interface.1.Stats.MultiPktReceived,890682272,unsignedLong

##### CSV Encoded Reporting Using ParameterPerColumn Report Format

Using the configuration examples provided in the previous sections the configuration for a CSV encoded HTTP report using the `ParameterPerColumn` report format:

    .BulkData.Profile.1
    .BulkData.Profile.1.Enable=true
    .BulkData.Profile.1.Protocol = "HTTP"
    .BulkData.Profile.1.ReportingInterval = 300
    .BulkData.Profile.1.TimeReference = "0001-01-01T00:00:00Z"
    .BulkData.Profile.1.HTTP.URL =  "https://bdc.acme.com/somedirectory"
    .BulkData.Profile.1.HTTP.Username = "username"
    .BulkData.Profile.1.HTTP.Password = "password"
    .BulkData.Profile.1.HTTP.Compression = "Disabled"
    .BulkData.Profile.1.HTTP.Method = "POST"
    .BulkData.Profile.1.HTTP.UseDateHeader = true
    .BulkData.Profile.1.EncodingType =  "CSV"
    .BulkData.Profile.1 CSVEncoding.FieldSeparator = ","
    .BulkData.Profile.1.CSVEncoding.RowSeparator="&#13;&#10;"
    .BulkData.Profile.1.CSVEncoding.EscapeCharacter="&quot;"
    .BulkData.Profile.1.CSVEncoding.ReportFormat ="ParameterPerColumn"
    .BulkData.Profile.1.CSVEncoding.ReportTimestamp ="Unix-Epoch"
    .BulkData.Profile.1.Parameter.1.Name =  "BroadPktSent"
    .BulkData.Profile.1.Parameter.1.Reference =  "Device.MoCA.Interface.1.Stats.BroadPktSent"
    .BulkData.Profile.1.Parameter.2.Name =  "BytesReceived"
    .BulkData.Profile.1.Parameter.2.Reference =  "Device.MoCA.Interface.1.Stats.BytesReceived"
    .BulkData.Profile.1.Parameter.3.Name =  "BytesSent"
    .BulkData.Profile.1.Parameter.3.Reference =  "Device.MoCA.Interface.1.Stats.BytesSent"
    .BulkData.Profile.1.Parameter.4.Name =  "MultiPktReceived"
    .BulkData.Profile.1.Parameter.4.Reference =  "Device.MoCA.Interface.1.Stats.MultiPktReceived"


The resulting CSV encoded data with transmission of the last 3 reports failed to complete would look like:

    ReportTimestamp,BroadPktSent,BytesReceived,BytesSent,MultiPktReceived
    1364529149,25248,200543250,7682161,890682272
    1464639150,25249,200553250,7683161,900683272
    1564749151,25255,200559350,7684133,910682272
    1664859152,25252,200653267,7685167,9705982277

### Encoding of JSON Bulk Data

Using the HTTP example above, the Set Message is used to configure the Agent to transfer data to the Bulk Data Collector using JSON encoding as follows:

    .BulkData.Profile.1.EncodingType =  "JSON"

#### Defining the Report Layout of the Encoded Bulk Data

Reports that are encoded with JSON Bulk Data are able to utilize different report format(s) defined by the `JSONEncoding` object’s `ReportFormat` Parameter as defined below.

In addition, a "`CollectionTime`" JSON object can be inserted into the report instance that defines when the data for the report was collected.

The following configures the Agent to encode the data using a Parameter as JSON Object named "`CollectionTime`" using the "Unix-Epoch" time format:

    .BulkData.Profile.1.JSONEncoding.ReportTimestamp ="Unix-Epoch"

Note: The encoding format of "`CollectionTime`" is defined as an JSON Object parameter encoded as: `"CollectionTime":1364529149`

Reports are defined as an Array of Report instances encoded as:

    "Report":[{...},{...}]

*Note: Multiple instances of Report instances may exist when previous reports have failed to be transmitted.*

#### Layout of Content for Failed Report Transmissions

*Note: This is only relevant for the HTTP variant of Bulk Data Collection.*

When the value of the `NumberOfRetainedFailedReports` Parameter of the `BulkData.Profile` Object Instance is `-1` or greater than `0`, then the report of the current reporting interval is appended to the failed reports. For JSON Encoded data the report for the current reporting interval is added onto the existing appended as a new "Data" object array instance as shown below:

    "Report": [
    {Report from a failed reporting interval},
    {Report from the current reporting interval}
    ]

#### Using the ObjectHierarchy Report Format

When a BulkData profile utilizes the JSON encoding type and has a `JSONEncoding.ReportFormat` Parameter value of "`ObjectHierarchy`", then the JSON objects are encoded such that each Object in the Object hierarchy of the data model is encoded as a corresponding hierarchy of JSON Objects with the parameters (i.e., parameterName, parameterValue) of the object specified as name/value pairs of the JSON Object.

For example the translation for the leaf Object "`Device.MoCA.Interface.*.Stats.`" would be:

```
    {
        "Report": [
            {
                "Device": {
                    "MoCA": {
                        "Interface": {
                            "1": {
                                "Stats": {
                                    "BroadPktSent": 25248,
                                    "BytesReceived": 200543250,
                                    "BytesSent": 25248,
                                    "MultiPktReceived": 200543250
                                }
                            },
                            "2": {
                                "Stats": {
                                    "BroadPktSent": 93247,
                                    "BytesReceived": 900543250,
                                    "BytesSent": 93247,
                                    "MultiPktReceived": 900543250
                                }
                            }
                        }
                    }
                }
            }
        ]
    }
```

*Note: The translated JSON Object name does not contain the trailing period "." of the leaf Object.*

#### Using the NameValuePair Report Format

When a BulkData profile utilizes the JSON encoding type and has a `JSONEncoding.ReportFormat` Parameter value of "`NameValuePair`", then the JSON objects are encoded such that each Parameter of the data model is encoded as an array instance with the parameterName representing JSON name token and parameterValue as the JSON value token.

For example the translation for the leaf Object "`Device.MoCA.Interface.*.Stats.`" would be:

    {
        "Report": [
            {
                "Device.MoCA.Interface.1.Stats.BroadPktSent": 25248,
                "Device.MoCA.Interface.1.Stats.BytesReceived": 200543250,
                "Device.MoCA.Interface.1.Stats.BytesSent": 25248,
                "Device.MoCA.Interface.1.Stats.MultiPktReceived": 200543250,
                "Device.MoCA.Interface.2.Stats.BroadPktSent": 93247,
                "Device.MoCA.Interface.2.Stats.BytesReceived": 900543250,
                "Device.MoCA.Interface.2.Stats.BytesSent": 93247,
                "Device.MoCA.Interface.2.Stats.MultiPktReceived": 900543250
            }
        ]
    }

*Note: The translated JSON Object name does not contain the trailing period "." of the leaf Object.*

#### Translating Data Types
JSON has a number of basic data types that are translated from the base data types defined in TR-106 [@TR-106]. The encoding of JSON Data Types MUST adhere to RFC 7159 [@RFC7159].

TR-106 named data types are translated into the underlying base TR-106 data types. Lists based on TR-106 base data types utilize the JSON String data type.

| TR-106 Data Type | JSON Data Type |
| ---------------: | :------------- |
| base64 | String: base64 representation of the binary data. |
| boolean | Boolean |
| dateTime | String represented as an ISO-8601 timestamp. |
| hexBinary | String: hex representation of the binary data. |
| int, long, unsignedInt, unsignedLong | Number |
| string | String |

#### JSON Encoded Report Example

Using the configuration examples provided in the previous sections the configuration for a JSON encoded HTTP report:

```
.BulkData.Profile.1
.BulkData.Profile.1.Enable=true
.BulkData.Profile.1.Protocol = "HTTP"
.BulkData.Profile.1.ReportingInterval = 300
.BulkData.Profile.1.TimeReference = "0001-01-01T00:00:00Z"
.BulkData.Profile.1.HTTP.URL =  "https://bdc.acme.com/somedirectory"
.BulkData.Profile.1.HTTP.Username = "username"
.BulkData.Profile.1.HTTP.Password = "password"
.BulkData.Profile.1.HTTP.Compression = "Disabled"
.BulkData.Profile.1.HTTP.Method = "POST"
.BulkData.Profile.1.HTTP.UseDateHeader = true
.BulkData.Profile.1.EncodingType =  "JSON"
.BulkData.Profile.1.JSONEncoding.ReportFormat ="ObjectHierarchy"
.BulkData.Profile.1.JSONEncoding.ReportTimestamp ="Unix-Epoch"
.BulkData.Profile.1.Parameter.1.Reference =  "Device.MoCA.Interface.*.Stats."
```

The resulting JSON encoded data would look like:

    {
        "Report": [
            {
                "CollectionTime": 1364529149,
                "Device": {
                    "MoCA": {
                        "Interface": {
                            "1": {
                                "Stats": {
                                    "BroadPktSent": 25248,
                                    "BytesReceived": 200543250,
                                    "BytesSent": 25248,
                                    "MultiPktReceived": 200543250
                                }
                            },
                            "2": {
                                "Stats": {
                                    "BroadPktSent": 93247,
                                    "BytesReceived": 900543250,
                                    "BytesSent": 93247,
                                    "MultiPktReceived": 900543250
                                }
                            }
                        }
                    }
                }
            }
        ]
    }

If the value of the `.BulkData.Profile.1.JSONEncoding.ReportFormat` Parameter was "`NameValuePair`", the results of the configuration would be:

    {
        "Report": [
            {
                "CollectionTime": 1364529149,
                "Device.MoCA.Interface.1.Stats.BroadPktSent": 25248,
                "Device.MoCA.Interface.1.Stats.BytesReceived": 200543250,
                "Device.MoCA.Interface.1.Stats.BytesSent": 25248,
                "Device.MoCA.Interface.1.Stats.MultiPktReceived": 200543250,
                "Device.MoCA.Interface.2.Stats.BroadPktSent": 93247,
                "Device.MoCA.Interface.2.Stats.BytesReceived": 900543250,
                "Device.MoCA.Interface.2.Stats.BytesSent": 93247,
                "Device.MoCA.Interface.2.Stats.MultiPktReceived": 900543250
            }
        ]
    }
