<!-- do not edit! this file was created from PROJECT.yaml by project-parser.py -->

### Issue History {.unnumbered .unlisted .new-page}

::: {.list-table .usp-revision-history aligns=l,l widths=14,65}

* - Issue Number
  - Changes

* - [Release 1.0][TR-369 Issue 1]
  - Release contains specification for the User Services Platform 1.0
    
    Corresponds to [TR-181 Issue 2 Amendment 12](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.0.0)

* - [Release 1.0.1][TR-369 Corrigendum 1]
  - * Added examples and clarifications to end-to-end messaging, use of
      endpoint ID, typographical fixes

* - [Release 1.0.2][TR-369 Corrigendum 2]
  - * Typographical and example fixes

* - [Release 1.1][TR-369 Amendment 1]
  - Release contains specification for the User Services Platform 1.1
    
    * Adds MQTT support as a Message Transfer Protocol
    * Adds a theory of operations for IoT control using USP Agents
    * Clarifications on protocol functions, error messages, and updates
      to examples
    
    Corresponds to [TR-181 Issue 2 Amendment 13](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.0)

* - Release 1.1.1
  - Regenerated data model HTML using fixed version of the BBF report tool

* - Release 1.1.2
  - Clarifies several examples, requirements, and error types

* - Release 1.1.3
  - Corresponds to [TR-106 Amendment 10](https://github.com/BroadbandForum/data-model-template/releases/tag/v1.10.0) and
    [TR-181 Issue 2 Amendment 14](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.3)

* - Release 1.1.4
  - Corresponds to [TR-181 Issue 2 Amendment 14 Corrigendum 1](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.1.4)

* - [Release 1.2][TR-369 Amendment 2]
  - Release contains specification for the User Services Platform 1.2
    
    * Clarify the expected responses in result of an `Operate` message
      (R-OPR.4)
    * Deprecates the use of COAP as an MTP
    * GetSupportedDM
      - now provides the data types for parameter values
      - now allows the Agent to provide information about whether or not
        it will ignore ValueChange subscriptions on a given parameter
      - now provides information about whether a command is synchronous
        vs. asynchronous
      - now allows requests on specific object instances and handles
        divergent data models
    * Defines discovery mechanisms for Endpoints connected to STOMP and
      MQTT brokers
    * Clarifies the use of search paths vs. unique key addressing in the
      Add message
    * Clarifies the use of required parameters and defaults for unique
      keys in the Add message
    * Annex A
      - now provides a theory of operations for use of the USPEventNotif
        mechanism for bulk data collection using the Push! event
      - defines a new bulk data collection over MQTT mechanism
    * DHCP discovery mechanism now provides a Controller Endpoint ID to
      the Agent
    * Enhances ease of use and clarifies requirements for use of TLS in
      USP Record integrity
    * New USP records
      - adds USP connect and disconnect records for use independent of
        MTP
      - adds USP Record specific error mechanism and error codes
      - MQTT and STOMP no longer silently drop errors; they now report
        errors in the USP Record.
      - USP Records can now include an empty payload
    * Get requests
      - can now include a max_depth flag to limit response size
      - Get response format has been clarified to return separate
        elements for sub-object
    * Clarifies the requirements around processing an entire message in
      the event of a failed operation when allow_partial is true vs.
      false
    * Clarifies the response behavior for Get, Set, and Delete when
      using a path that matches no instances
    * Fixes and enhances the use of error codes for the Operate message
    * Clarifies and updates Controller credential/authentication theory
      of operations and flow diagrams
    * Clarifies the use of subjectAltName in certificates
    * Clarifies R-E2E.4
    * Deprecated and Obsolete terms are now defined in the References and
      Terminology section
    * Updated R-E3E.43
    * Deprecates R-MSG.2
    * Deprecates R-E2E.2
    * R-E2E.42 now makes TLS renegotiation forbidden
    * Modifies R-NOT.9 and adds R-NOT.10 adjusting how the Agent and
      Controller should handle the subscription_id field
    
    Corresponds to
    [TR-106 Amendment 11](https://github.com/BroadbandForum/data-model-template/releases/tag/v1.11.0) and
    [TR-181 Issue 2 Amendment 15](https://github.com/BroadbandForum/usp-data-models/releases/tag/v1.2.0)

* - [Release 1.3][TR-369 Amendment 3]
  - Release contains the specification for the User Services Platform 1.3
    
    * Adds Appendix VI, "Software Modularization and USP-Enabled
      Applications Theory of Operation"
    * Adds new Unix Domain Socket MTP
    * Adds two new messages, "Register" and "Deregister", and associated
      error codes (primarily for use with Appendix VI but can be
      used in many scenarios)
    * Adds new Software Module Management features
    * Adds a note about the use of the new TriggerAction parameter in
      Subscription objects
    * Updates "Authentication and Authorization" to include the use of
      new SecuredRole
    * Updates the Add message to allow for Search Paths and clarifies the
      application of permissions during Add messages
    * Obsoletes CoAP as an MTP
    * Adds two new requirements regarding Unique Key immutability
    * Clarifies how Set should respond when using a Search Path where one
      or more objects fail to update
    * Updates the use of EndpointID in WebSocket arguments
      and adds an fqdn authority scheme
    * Addesses a potential attack vector with using MQTT, and updates other
      MQTT behavior
    * Updates Annex A to explain use of the "Exclude" parameter
    * Updates Discovery to include the use of DHCP options for agent-device
      association
    * Adds a note about USP protocol versioning and Controller/Agent
      behavior
    * Clarifies and updates the use of certain error codes
    * Clarifies the behavior of Get messages when asking for specific
      Multi-Instance Objects that don't exist
    * Clarifies some behavior when responding via USP Records
    * Updates message flow diagrams to remove the implication of ordered
      responses
    * Adds new requirement R-SEC.4b for Trusted Brokers

:::

### Editors {.unnumbered .unlisted}

::: {.list-table .usp-editors aligns=l,l,l,l widths=12,10,15,21}

* - Name
  - Company
  - Email
  - Role

* - Barbara Stark
  - AT&T
  - barbara.stark@att.com
  - Editor/USP Project Lead

* - Tim Spets
  - Assia
  - tspets@assia-inc.com
  - Editor/USP Project Lead

* - Jason Walls
  - QA Cafe, LLC
  - jason@qacafe.com
  - Editor/Broadband User Services Work Area Director

* - John Blackford
  - Commscope
  - john.blackford@commscope.com
  - Editor/Broadband User Services Work Area Director

:::

### Acknowledgments {.unnumbered .unlisted}

::: {.list-table .usp-acknowledgments aligns=l,l,l widths=12,10,15}

* - Name
  - Company
  - Email

* - Jean-Didier Ott
  - Orange
  - jeandidier.ott@orange.com

* - Timothy Carey
  - Nokia
  - timothy.carey@nokia.com

* - Steven Nicolai
  - Arris
  - Steven.Nicolai@arris.com

* - Apostolos Papageorgiou
  - NEC
  - apostolos.Papageorgiou@neclab.eu

* - Mark Tabry
  - Google
  - mtab@google.com

* - Klaus Wich
  - Huawei
  - klaus.wich@huawei.com

* - Daniel Egger
  - Axiros
  - daniel.egger@axiros.com

* - Bahadir Danisik
  - Nokia
  - bahadir.danisik@nokia.com

* - William Lupton
  - Broadband Forum
  - wlupton@broadband-forum.org

* - Matthieu Anne
  - Orange
  - matthieu.anne@orange.com

* - Thales Fragoso
  - Axiros
  - thales.fragoso@axiros.com

:::

[TR-369 Amendment 1]: https://www.broadband-forum.org/download/TR-369_Amendment-1.pdf
[TR-369 Amendment 2]: https://www.broadband-forum.org/download/TR-369_Amendment-2.pdf
[TR-369 Amendment 3]: https://www.broadband-forum.org/download/TR-369_Amendment-3.pdf
[TR-369 Corrigendum 1]: https://www.broadband-forum.org/download/TR-369_Corrigendum-1.pdf
[TR-369 Corrigendum 2]: https://www.broadband-forum.org/download/TR-369_Corrigendum-2.pdf
[TR-369 Issue 1]: https://www.broadband-forum.org/download/TR-369_Issue-1.pdf
