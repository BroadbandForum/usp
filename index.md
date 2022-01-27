---
# we don't want the document title on the home page
doctitle: ''

---

:::::: {style="width:45%; float:left;"}

## What is USP? {.unnumbered .unlisted}

The **User Services Platform** is a standardized **protocol for managing,
monitoring, upgrading, and controlling connected devices**. USP allows service
providers and consumer electronics manufacturers to:

* Create interoperable and vendor-independent **managed Wi-Fi systems**.

* Perform **lifecycle management** of consumer connected devices.

* Support **independent applications** for smart networking products.

* Enable **IoT and consumer electronics upgradability** for critical security
  patches.

* Develop applications that gather the telemetry necessary to **mass data
processing, AI, and machine learning**.

* **Bootstrap and configure** newly installed or purchased devices and virtual
  services.

* Let customer support **monitor and troubleshoot** connected devices,
  services, and home network links.

* Easily map the home network to **control service quality and monitor
  threats**.

* Securely **control IoT, smart home, and smart networking functions** locally
  or from the Cloud

USP represents the natural evolution of the Broadband Forum's [CPE WAN Management Protocol](https://www.broadband-forum.org/cwmp) (CWMP), commonly known as TR-069. It uses an expanded version of the Device:2 Data Model to represent device operations (firmware upgrades, reboots, etc.), network interfaces, events, and service functions (IoT functions, VoIP, etc.).

## How to use this site: {.unnumbered .unlisted}

* The *[specification](specification/index.html)* directory contains the full
  text of the current version of the protocol, and the schema (currently in
  Protocol Buffers) for the syntax of USP messages. Use this section when
  developing your USP protocol stack.

* The *[data models](https://usp-data-models.broadband-forum.org)* link will
  take you to the generated versions of the Device:2 data model (also known as
  "TR-181i2 - Device:2 Data Model for TR-069 devices and USP Agents") specific
  to USP. The raw xml used in development can be found in this directory. Use
  these to find the Objects necessary to the USP protocol stack, and when
  developing the Objects, interfaces, services, etc. that you want to manage
  and control with USP.

* The USP Agent *[Test Plan](https://usp-compliance.broadband-forum.org)*
  provides a list of the test cases executed to validate USP Agent
  implementations and seek certification.

* *[Dev Resources](%resurl%)* provides several links for how to
  build, test, certify, and bring to market USP based solutions.

* The *[FAQ](%faqurl%)* page gives information on frequently asked
  questions. Use this section to learn more about USP and getting involved in
  its ongoing development.

::::::

:::::: {style="width:45%; float:right;"}

## Current Version: %versionNumber% {.unnumbered .unlisted}

#### About this version: {.unnumbered .unlisted}

This specification includes:

* Architectural overview
* Discovery mechanisms for Controllers and Agents
* Basic CRUD messages between Controllers and Agents
* Use of USP Record encapsulation for end to end integrity, security, and
  privacy
* Data model Objects specific to protocol functionality, object defined
  operations, and notifications/events
* Protocol buffers encoding schema
* Use of WebSockets, MQTT, and STOMP as message transfer protocols (MTP)
* A system for authentication and authorization
* Extensions for bulk data collection, firmware management, software module
  management, and device proxying
* Theory of operations for using a USP Agent to control IoT devices and systems

::: {style="text-align:center;"}

[![](/broadband-forum-logo.png)](https://www.broadband-forum.org)

USP is developed by the Broadband Forum. For more information, visit [https://www.broadband-forum.org]()

:::

::::::

:::::: {style="clear:both;"}

::::::
