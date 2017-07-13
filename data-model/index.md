Several data models are defined for use with the User Services Platform. These data models contain the Objects, Parameters, Commands, and Events that describe the many different functions and capabilities available to devices and services exposed by a USP Agent.  

USP data models are divided into two types: *Root* and *Service*. The root data model, "Device", is used to describe the major functions of a network aware device, including interfaces, Controllers, security, software/firmware, diagnostics, hosts and proxy devices, and the basic information necessary to USP.

Service data models describe modular functionality that allow the extension of the root data model (under Device.Services.) to provide particular services, such as voice, set-top-box functionality, storage, small cell interface modeling, etc.

## How do I use these?

Use the USP data model files to determine what exists in your solution's *Supported Data Model*. This will help Controllers learn what your solution is capable of. The data models will also describe how your solution's *Instantiated Data Model* will behave during operation.

* View the html files on this page for a human-readable look at the data model documentation.
* Use the xml files in this repository when generating code and performing data validation.

These data models are based off of the [Broadband Forum](http://www.broadband-forum.org)'s data models for the [CPE WAN Management Protocol](http://www.broadband-forum.org/cwmp), also known as "TR-069", with a robust development history.

## Data Model Repository

<a href="https://github.com/BroadbandForum/usp/tree/master/data-model" class="btn-success">Data Models for USP (repository)</a>

## Root Data Model Documentation

<a href="/data-model/tr-181-2-12-usp-full.html" class="btn-success">Device:2 Data Model for USP (HTML)</a>

## Service Data Model Documentation

The service data models defined for CWMP are compatible with USP. These include Objects and Paramters for set-top-box functions, VoIP functions, network attached storage functions, and femto/small cell functions. These data models may be optimized for USP in the future (taking advantage of DM defined operations, event, etc.).

* [STBService:1.4 Data Model](tr-135-1-4-0.html)
* [VoiceService:2.0 Data Model](tr-104-2-0-0.html)
* [StorageService:1.3 Data Model](tr-140-1-3-0.html)
* [FAPService:2.1 Data Model](tr-196-2-1-0.html)
