# The GetInstances Message

The GetInstances message takes a Path Name to an Object and requests that the Agent return the Instances of that Object that exist and *possibly* any Multi-Instance sub-Objects that exist as well as their Instances. This is used for getting a quick map of the Mutli-Instance Objects (i.e., tables) the Agent currently represents, and their unique keys, so that they can be addressed and manipulated later.

GetInstances takes one or more Path Names to Multi-Instance Objects in a Request to an Agent. In addition, both GetInstances and GetSupportedDM (below) make use of a flag called `next_level`, which determines whether or not the Response should include all of the sub-Objects that are children of the Object specified in `obj_path`. A value of `true` means that the Response should return data *only* for the Object specified. A value of false means that all sub-Objects should be resolved and returned.

For example, if a Controller wanted to know *only* the current instances of Wifi SSID Objects that exist on an Agent (that has 3 SSIDs), it would send a GetInstances Request as:

    GetInstances {
      obj_path_list : Device.Wifi.SSID.
      bool next_level : true
    }

The Agent's Response would contain:

    GetInstancesResp {
      req_path_result_list {
        requested_path : Device.Wifi.SSID.
        err_code : 0
        err_msg :
        curr_inst_list {
          instantiated_obj_path : Device.Wifi.SSID.1.
          unique_key_map :

            key : Alias
            value : UserWifi1

            key : Name
            value : UserWifi1

            key : SSID
            value : SecureProviderWifi

            key : BSSID
            value : 00:11:22:33:44:55

          instantiated_obj_path : Device.Wifi.SSID.2.
          unique_key_map :

            key : Alias
            value : UserWifi2

            key : Name
            value : UserWifi2

            key : SSID
            value : GuestProviderWifi

            key : BSSID
            value : 00:11:22:33:44:55

        }
      }
    }

In another example, the Controller wants to get all of  the Instances of the `Device.Wifi.AccessPoint` table, plus all of the instances of the AssociatedDevice Object and AC Object (sub-Objects of AccessPoint). It would issue a GetInstances Request with the following:

    GetInstances {
      obj_path_list : Device.Wifi.AccessPoint.
      bool next_level : false
    }

The Agent's Response will contain an entry in curr_inst_list for all of the Instances of the `Device.Wifi.AccessPoint` table, plus the Instances of the Multi-Instance sub-Objects `.AssociatedDevice.` and `.AC.`:

    GetInstancesResp {
      req_path_result_list {
        requested_path : Device.Wifi.AccessPoint.
        err_code : 0
        err_msg :
        curr_inst_list {
          instantiated_obj_path : Device.Wifi.AccessPoint.1.
          unique_key_map :

            key : Alias
            value : SomeAlias

            key : SSIDReference
            value : Device.Wifi.SSID.1

          instantiated_obj_path : Device.Wifi.AccessPoint.2.
          unique_key_map :

            key : Alias
            value : SomeAlias

            key : SSIDReference
            value : Device.Wifi.SSID.2

          instantiated_obj_path : Device.Wifi.AccessPoint.1.AssociatedDevice.1.
          unique_key_map :

            key : MACAddress
            value : 11:22:33:44:55:66

          instantiated_obj_path : Device.Wifi.AccessPoint.1.AC.1.
          unique_key_map :

            key : AccessCategory
            value : BE

          instantiated_obj_path : Device.Wifi.AccessPoint.2.AssociatedDevice.1.
          unique_key_map :

            key : MACAddress
            value : 11:22:33:44:55:66

          instantiated_obj_path : Device.Wifi.AccessPoint.2.AC.1.
          unique_key_map :

            key : AccessCategory
            value : BE
          }
        }
      }

Or more, if more Object Instances exist.

## GetInstances Request Elements

`repeated string obj_path_list`

This element contains a repeated set of Path Names or Search Paths to Multi-Instance Objects in the Agent's Instantiated Data Model.

`bool next_level`

This element, if `true`, indicates that the Agent should return only those instances in the Object(s) matched by the Path Name or Search Path in `obj_path`, and not return any child objects.

## GetInstances Response Elements

`repeated RequestedPathResult req_path_result_list`

This element contains a RequestedPathResult message for each Path Name or Search

`string requested_path`

This element contains one of the Path Names or Search Paths given in `obj_path` of the associated GetInstances Request.

`fixed32 err_code`

This element contains a [numeric code](/messages/error-codes/) indicating the type of error that caused the Get to fail on this path. A value of 0 indicates the path could be read successfully.

**R-GIN.0** - If the Controller making the Request does not have Read permission on an Object or Parameter matched through the `requested_path` element, the Object or Parameter MUST be treated as if it is not present in the Agent’s instantiated data model.

`string err_msg`

This element contains additional information about the reason behind the error.

`repeated CurrInstance curr_inst_list`

This element contains a message of type `CurrInstance` for each Instance of *all* of the Objects matched by `requested_path` that exists in the Agent's Instantiated Data Model.

#### CurrInstance Elements

`string instantiated_obj_path`

This element contains the Instance Number of the Object Instance.

`map<string, string> unique_key_map`

This element contains a map of key/value pairs for all supported parameters that are part of any of this Object's unique keys.

**R-GIN.1** - If the Controller does not have Read permission on any of the parameters specified in `unique_key_map`, these parameters MUST NOT be returned in this element.

## GetInstances Error Codes

Appropriate error codes for the GetInstances message include `7000-7006`, `7008`, `7016`, `7018` and `7800-7999`.
