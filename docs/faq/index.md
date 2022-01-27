
# FAQ {.unnumbered}

## What is USP? {.unnumbered}

USP stands for the User Services Platform, a standardized platform to manage, monitor, update, and control connected devices, services, IoT, and home networks. USP consists of an architecture, protocol, and set of data models that create a network of Controllers and Agents that allow applications to manipulate the hardware and software capabilities of an end-user's network and devices (network interfaces, consumer electronics platforms, smart objects, virtualized network functions, etc.).

## What do I need to get started? {.unnumbered}

Checkout our [development resources](/resources/) for schemas, code, certification, and more.

## What are the major features of USP? {.unnumbered}

The User Services Protocol is designed with four major features in mind:

* Flexibility - USP is applicable to many different use cases or deployment scenarios, and able to be implemented by new and varied kinds of devices.
* Scaling - With the increase in the kinds of devices that can now be managed, monitored, or controlled, comes an increase in the raw numbers of those devices. USP is able to scale to a very large number of managed devices, services, and connections.
* Standardization and ease of migration - USP meets the challenges of connected device (network gateways, whole-home and enterprise Wi-Fi, and IoT) management and control with an interoperable, non-proprietary standard, that easily evolves from existing TR-069 deployments.
* Security - USP is designed with application layer security, authentication, integrity, and privacy from the ground up.

For an in-depth look at the high level benefits of USP, read our whitepaper, "[Realizing the Promise of the Connected Home with USP](https://www.broadband-forum.org/technical/download/MU-461.pdf)".

## Who makes the User Services Platform? {.unnumbered}

![](./broadband-forum-logo.png)

USP is developed by the [Broadband Forum](http://www.broadband-forum.org), an international standards organization of network service providers/MSOs, end user device manufacturers, government and university organizations, and test laboratories. It is developed in the "Broadband User Services" [Work Area](https://www.broadband-forum.org/standards-and-software/downloads/work-areas-projects).

## How does USP relate to TR-069? {.unnumbered}

USP is a natural evolution of the [CPE WAN Management Protocol](https://www.broadband-forum.org/technical/download/TR-069.pdf) (more commonly known as TR-069). It was developed to improve on the use cases met by TR-069, expand the number and kinds of devices it can be deployed on, and leverage the lessons learned in the 15 years of TR-069 being deployed in real-world environments.

## Is USP a replacement for TR-069? {.unnumbered}

While USP represents significant advancements in scalability and scope over TR-069, it is designed to co-exist with TR-069 and offer an easy migration path for those who want to make the switch.

## Is the BBF deprecating or ending support for TR-069? {.unnumbered}

No. The TR-069 project is still accepting new contributions and has had its most recent version (Amendment 6, defining CWMP 1.5) published at the same time as USP.

## Is BBF building a new data model for USP? {.unnumbered}

No. USP is designed to re-use the [Device:2 data model](http://usp-data-models.broadband-forum.org) and associated Service data models produced for TR-069. There are minor alterations to the way USP handles commands, events, and proxying, but it is otherwise identical. This helps those looking to migrate to USP make the change with little alteration to back-end services that rely on the Device:2 data model.

## What sorts of devices can implement USP? {.unnumbered}

Any device capable of an IP connection can implement a USP Agent, including Wi-Fi, fixed wireline, and fixed wireless (i.e. 5G) devices. In addition, smart hubs that aggregate other connection schemes such as ZigBee, Zwave, Bluetooth, and others can be easily managed via USP's proxy mechanism. USP Controllers can be implemented anywhere from large scale management servers (like TR-069 ACS) or to enable user applications on a smart phone or other user-facing interfaces.

## Can USP be used to managed virtual network functions or containers? {.unnumbered}

USP objects can represent hardware-independent elements via either abstraction or proxy, and re-uses the Software Module Management mechanism designed for TR-069 to manage both execution and deployment units.

## Do I need to support all of USP's message transfer protocols to be compliant? {.unnumbered}

No. Each supported transport is meant for a different core use case. In addition, transport proxy functions are in development that will make co-existence and interoperability of implementations of different transports simple.

## I'm building a USP Agent. How do I get certified? {.unnumbered}

The conformance test plan for USP Agents is defined in [TP-469](https://usp-compliance.broadband-forum.org). This test plan evolves, and forms the basis for the Broadband Forum's [USP Agent Certification Program](https://www.broadband-forum.org/testing-and-certification-programs/bbf-369-usp-certification).

## I have suggestions on USP or things that I would like to see added to the data models. How do I get involved? {.unnumbered}

Feedback and questions can always be given via [GitHub](https://github.com/BroadbandForum/usp). Due to the standards process adopted by the Broadband Forum, a contributing Broadband Forum member must adopt suggested changes and present them to the Forum as a contribution from their company. An even easier way is to [become a member](https://www.broadband-forum.org/about-the-broadband-forum/membership/becoming-a-bbf-member) and contribute directly. The Broadband Forum has membership levels for large businesses, small businesses, and individuals.

