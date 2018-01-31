<!-- Reference Links -->
[1]:	https://github.com/BroadbandForum/usp/tree/master/data-model "TR-181 Issue 2 Device:2 Data Model"
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
[13]: https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries "IEEE Registration Authority"
[14]: https://tools.ietf.org/html/rfc4122 "RFC 4122 A Universally Unique IDentifier (UUID) URN Namespace"
[15]: https://tools.ietf.org/html/rfc5280 "RFC 5290 Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[16]: https://tools.ietf.org/html/rfc6818 "RFC 6818 Updates to the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile"
[17]: https://tools.ietf.org/html/rfc2234 "RFC 2234 Augmented BNF for Syntax Specifications: ABNF"
[18]: https://tools.ietf.org/html/rfc3986 "RFC 3986 Uniform Resource Identifier (URI): Generic Syntax"
[19]: https://tools.ietf.org/html/rfc2141 "RFC 2141 URN Syntax"
[20]: https://tools.ietf.org/html/rfc6455 "RFC 6455 The WebSocket Protocol"
[21]: https://stomp.github.io/stomp-specification-1.2.html "Simple Text Oriented Message Protocol"
[22]: https://tools.ietf.org/html/rfc5246 "The Transport Layer Security (TLS) Protocol Version 1.2"
[23]: https://tools.ietf.org/html/rfc6347 "Datagram Transport Layer Security Version 1.2"
[Conventions]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"


# Appendix I - Firmware Management of Devices with USP Agents

1. [Getting the firmware image onto the device](#getting_the_firmware_image_onto_the_device)
2. [Using multiple firmware images](#using_multiple_firmware_images)
    1. [Switching firmware images](#switching_firmware_images)
    2. [Performing a delayed firmware upgrade](#performing_a_delayed_firmware_upgrade)
    3. [Recovering from a failed upgrade](#recovering_from_a_failed_upgrade)

Many manufacturers build and deploy devices that are able to support multiple firmware images (i.e. multiple firmware images can be installed on an Agent at the same time). There are at least a couple of advantages to this strategy:

1. Having multiple firmware images installed improves the robustness and stability of the device because, in all likelihood, one of the installed images will be stable and bootable. Should a device not be able to boot a newly installed firmware image, it could have the ability to attempt to boot from a different firmware image, thus allowing the device to come back online.

2. Support for multiple firmware images offers the ability for the service provider to have a new firmware downloaded (but not activated) to the device at any point during the day, then perhaps requiring only a Set message and an Operate message to invoke the Reboot command at some later time (perhaps during a short maintenance window or when the device is idle) to cause the device to switch over to the new firmware. Along with reducing the impact on the subscriber, the ability to spread the download portion a firmware upgrade over a longer period of time (eg, the entire day or over several days) can help minimize the impact of the upgrade on the provider’s network.

This Appendix discusses how to utilize the firmware image table on a device to support firmware upgrades whether the device supports multiple instances or just a single instance.

<a id='getting_the_firmware_image_onto_the_device' />

## Getting the firmware image onto the device

A Controller can download a firmware image to an Agent by invoking the `Download()` command (via the Operate message) found within an instance of the `Device.FirmwareImage.{i}.` data model table. The `Download()` command will cause the referenced file to be downloaded into the firmware image instance being operated on, and it will cause that file to be validated by the Agent (the validation process would include any normal system validate of a firmware image as well as the check sum validation provided in the `Download()` command).

If an Agent only supports a single firmware image instance then a Controller would invoke the `Download()` command on that active firmware image instance using the `AutoActivate` argument to immediately activate the new firmware after it has been downloaded.  Neither the `Device.DeviceInfo.BootFirmwareImage` parameter nor the `Device.DeviceInfo.FirmwareImage.{i}.Activate()` command would typically be implemented by a device that only supports a single firmware image instance.

If an Agent supports more than a single firmware image instance then a Controller would typically invoke the `Download()` command on a non-active firmware image instance in an effort of preserving the current firmware image in case of an error while upgrading the firmware. A firmware image instance is considered active if it is the currently running firmware image.

<a id='using_multiple_firmware_images' />

## Using multiple firmware images

This section discusses the added functionality available when a device supports two or more instances in the `Device.FirmwareImage.{i}.` data model table.

<a id='switching_firmware_images' />

### Switching firmware images

Once a device has multiple firmware images downloaded, validated, and available, a Controller can use the data model to query what images are on the device, which image is active, and configure which image to activate.

A Controller can activate a new firmware image by following one of two different procedures: (A) the Controller can modify the `Device.DeviceInfo.BootFirmwareImage` parameter to point to the `Device.DeviceInfo.FirmwareImage.{i}.` object instance that contains the desired firmware image and then reboot the device by invoking an `Operate` message with a `Reboot()` command or (B) the Controller can invoke an Operate message with an `Activate()` command against the desired `FirmwareImage` instance.

When attempting to get a device to switch to a different firmware image, it is recommended that the Controller either subscribe to a `ValueChange` notification on the `DeviceInfo.SoftwareVersion` parameter or subscribe to the `Boot!` Event notification. If the Software Version value has not changed or the `Boot!` Event's `FirmwareUpdated` argument is false, it could be an indication that the device had problems booting the target firmware image.

<a id='performing_a_delayed_firmware_upgrade' />

### Performing a delayed firmware upgrade

One of the benefits to having support for multiple firmware images on a device is that it provides an opportunity to push a firmware image to a device and then have the device switch to that image at a later time. This functionally allows a service provider to push a firmware image to a set of devices at any point during the day and then use a maintenance window to switch all of the target devices to the target firmware.

This ability is of value because normally the download of the firmware and the switch to the new image would both have to take place during the maintenance window. Bandwidth limitations may have an impact on the number of devices that can be performing the download at the same time. If this is the case, the number of devices that can be upgrading at the same time may be lower than desired, requiring multiple maintenance windows to complete the upgrade. However, support for multiple firmware images allows for the service provider to push firmware images over a longer period of time and then use a smaller maintenance window to tell the device to switch firmware images. This can result is shorter system-wide firmware upgrades.

<a id='recovering_from_a_failed_upgrade' />

### Recovering from a failed upgrade

Another benefit of having multiple firmware images on a device is that if a device cannot boot into a target firmware image because of some problem with the image, the device could then try to boot one of the other firmware images.

When there are two images, the device would simply try booting the alternate image (which, ideally, holds the previous version of the firmware). If there are more than two images, the device could try booting from any of the other available images. Ideally, the device would keep track of and try to boot from the previously known working firmware (assuming that firmware is still installed on the device).

Should the device boot a firmware image other than that specified via the `Device.DeviceInfo.BootFirmwareImage` parameter, it is important that the device not change the value of the `Device.DeviceInfo.BootFirmwareImage` parameter to point to the currently-running firmware image object. If the device was to change this parameter value, it could make troubleshooting problems with a firmware image switch more difficult.

It was recommended above that the Controller keep track of the value of `Device.DeviceInfo.SoftwareVersion` parameter or the `FirmwareActivation` enumerated value in the `Boot!` Event's `Cause` argument. If the version changes unexpectedly or a `FirmwareActivation` cause is detected, it could be an indication that the device had problems booting a particular firmware image.
