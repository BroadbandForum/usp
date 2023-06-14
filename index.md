---
# we don't want the document title on the home page
doctitle: ''

---

:::::: {style="width:45%; float:left;"}

# The User Services Platform {#executive-summary .unnumbered .hidden-header}

%description%

## How to use this site:

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

* The USP Agent *[Test Plan](https://usp-test.broadband-forum.org)*
  provides a list of the test cases executed to validate USP Agent
  implementations and seek certification.

* *[Dev Resources](%resurl%)* provides several links for how to
  build, test, certify, and bring to market USP based solutions.

* The *[FAQ](%faqurl%)* page gives information on frequently asked
  questions. Use this section to learn more about USP and getting involved in
  its ongoing development.

::::::

:::::: {style="width:45%; float:right;"}

## Current Version: %versionNumber%

### About this version:

This specification includes:

* Architectural overview
* Discovery mechanisms for Controllers and Agents
* Basic CRUD messages between Controllers and Agents
* Use of USP Record encapsulation for end to end integrity, security, and
  privacy
* Data model Objects specific to protocol functionality, object defined
  operations, and notifications/events
* Protocol buffers encoding schema
* Use of WebSockets, MQTT, STOMP, and UNIX Domain Sockets as message transfer
protocols (MTP)
* A system for authentication and authorization
* Extensions for bulk data collection, firmware management, software module
  management, containerized microservices, and device proxying
* Theory of operations for using a USP Agent to control IoT devices and systems

::: {style="text-align:center;"}

[![](broadband-forum-logo.png)](https://www.broadband-forum.org)

USP is developed by the Broadband Forum. For more information, visit [https://www.broadband-forum.org]()

:::

::::::

:::::: {style="clear:both;"}

::::::
