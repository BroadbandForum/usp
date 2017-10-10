<div style="width:100%">          
  <div style="width:45%; float:left;">

    <h2>What is USP?</h2>

    <p>The <strong>User Services Platform</strong> is a standardized <strong>protocol for managing, monitoring, upgrading, and controlling connected devices</strong>. USP allows service providers, consumer electronics manufacturers, and end users to:</p>

    <ul>
    <li>Perform <strong>lifecycle management</strong> of consumer connected devices</li>
    <li>Enable <strong>IoT and consumer electronics upgradability</strong> for critical security patches</li>
    <li><strong>Bootstrap and configure</strong> newly installed or purchased devices and virtual services</li>
    <li>Let customer support <strong>monitor and troubleshoot</strong> connected devices, services, and home network links</li>
    <li>Easily map the home network to <strong>control service quality and monitor threats</strong></li>
    <li>Securely <strong>control IoT, smart home, and smart networking functions</strong> locally or from the Cloud</li>
    <li><strong>Enable multi-tenant</strong> (i.e., multi-stakeholder) management and control</li>
    </ul>

    <p>USP represents the natural evolution of the Broadband Forum's <a href="http://www.broadband-forum.org/cwmp">CPE WAN Management Protocol</a> (CWMP), commonly known as TR-069. It uses an expanded version of the <a href="">Device:2 Data Model for TR-069 Devices</a> to represent device operations (firmware upgrades, reboots, etc.), network interfaces, and service functions (IoT functions, VoIP, etc.).</p>

    <h2>How to use this site:</h2>

    <ul>
    <li>The <a href="/specification/"><em>specification</em></a> directory contains the full text of the current version of the protocol, and the schema (currently in Protocol Buffers) for the syntax of USP messages. Use this section when developing your USP protocol stack.</li>
    <li>The <a href="/data-model/"><em>data models</em></a> link will take you to the generated versions of the Device:2 data model (also known as "TR-181i2 - Device:2 Data Model for TR-069 devices and USP Agents") specific to USP. The raw xml used in development can be found in this directory. Use these to find the objects necessary to the USP protocol stack, and when developing the objects, interfaces, services, etc. that you want to manage and control with USP.</li>
    <li>The <a href="/resources/"><em>resources</em></a> page gives information about upcoming test events, access to training resources, and our frequently asked questions. Use this section to learn more about USP and getting involved in its ongoing development.</li>
    </ul>
  </div>
  <div style="width:45%; float:right;">

    <h2>Current Version:</h2>

    <h3>1.0-DRAFT-04</h3>

    <h4>About this version:</h4>

    <p>This DRAFT version is for <strong>BETA TESTING ONLY</strong> in order to allow development to begin and feedback given to the BBF. It is NOT intended for deployment. It includes:</p>

    <ul>
    <li>Architectural overview</li>
    <li>Discovery mechanisms for Controllers and Agents</li>
    <li>Basic messaging between Controllers and Agents</li>
    <li>Use of USP Record messages for end to end integrity, security, and privacy</li>
    <li>Data model objects specific to protocol functionality, object defined operations, and notifications/events</li>
    <li>Protocol buffers encoding schema</li>
    <li>Use of CoAP as a message transfer protocols (MTP)</li>
    <li>Security at the transport (MTP) layer</li>
    <li>Extensions for bulk data collection</li>
    </ul>

    <h4>Upcoming versions:</h4>

    <p>Additional versions of this DRAFT may be released prior to the 1.0 release.</p>

    <p>Version 1.0 will include additional MTPs (used for crossing NAT/Firewalls) and proxy mechanisms.</p>

    <p style="text-align:center; margin-top:4ex;"><a href="http://www.broadband-forum.org"><img src="/assets/img/broadband-forum-logo.png"></a></p>
    <p style="text-align:center;">USP is developed by the Broadband Forum. For more information, visit <a href="http://www.broadband-forum.org">http://www.broadband-forum.org</a></p>

  </div>
</div>
