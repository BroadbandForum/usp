# Device Proxy {.appendix1}

This appendix describes a Theory of Operations for the `Device.ProxiedDevice.` Object
defined in the Device:2 Data Model [@TR-181].

The `Device.ProxiedDevice` table is defined as:

> "Each entry in the table is a ProxiedDevice Object that is a mount point. Each ProxiedDevice represents distinct hardware Devices. ProxiedDevice Objects are virtual and abstracted representation of functionality that exists on hardware other than that which the Agent is running."

An implementation of the `Device.ProxiedDevice.` Object may be used in an IoT Gateway that proxies devices that are connected to it via technologies other than USP such as Z-Wave, ZigBee, Wi-Fi, etc. By designating a table of `ProxiedDevice` Objects, each defined as a mount point, this allows a data model with Objects that are mountable to be used to represent the capabilities of each of the `ProxiedDevice` table instances.

For example, if `Device.WiFi.` and `Device.TemperatureStatus.` Objects are modeled by the Agent, then `Device.ProxiedDevice.1.WiFi.Radio.1.` models a distinctly separate hardware device and has no relationship with `Device.WiFi.Radio.1.`. The `ProxiedDevice` Objects may each represent entirely different types of devices each with a different set of Objects. The `ProxiedDevice.1.TemperatureStatus.TemperatureSensor.1.` Object has no physical relationship to `ProxiedDevice.2.TemperatureStatus.TemperatureSensor.1.` as they represent temperature sensors that exist on separate hardware. The mount point allows `Device.ProxiedDevice.1.WiFi.Radio.` and `Device.ProxiedDevice.1.TemperatureStatus.TemperatureSensor.` to represent the full set of capabilities for the device being proxied. This provides a Controller a distinct path to each `ProxiedDevice` Object.
