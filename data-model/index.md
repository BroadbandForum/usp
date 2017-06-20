The Broadband Forum defines several data models for use with the User Services Platform. These data models contain the Objects, Parameters, Commands, and Events that describe the many different functions and capabilities available to devices and services exposed by a USP Agent.  

USP data models are divided into two types: *Root* and *Service*. The root data model, "Device", is used to describe the major functions of a network aware device, including interfaces, Controllers, security, software/firmware, diagnostics, hosts and proxy devices, and the basic information necessary to USP.

Service data models describe modular functionality that allow the extension of the root data model on a device (under Device.Services.) to provide particular services, such as voice, set-top-box functionality, storage, small cell interface modeling, etc.

## How do I use these?

Use the USP data model files to determine what exists in your solution's *Supported Data Model*. This will help Controllers learn what your solution is capable of. The data models will also describe how your solution's *Instantiated Data Model* will behave during operation.

* View the html files on this page for a human-readable look at the data model documentation.
* Use the xml files in this repository when generating code and performing data validation.

These data models are based off of the [Broadband Forum](http://www.broadband-forum.org)'s data models for the [CPE WAN Management Protocol](http://www.broadband-forum.org/cwmp), also known as "TR-069", with a robust development history.

## Data Model Repository

<a href="" class="btn-success">Data Models for USP (repository)</a>

## Root Data Model Documentation

<a href="/usp/data-model/tr-181-2-12-usp-full.html" class="btn-success">Device:2 Data Model for USP (HTML)</a>

## Service Data Model Documentation

Coming soon. You can find the versions of these data models developed for CWMP [here](http://www.broadband-forum.org/cwmp).
