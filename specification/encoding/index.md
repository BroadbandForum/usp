# Message Encoding {#sec:encoding}

USP requires a mechanism to serialize data to be sent over a Message Transfer Protocol. The description of each individual Message and the USP Record encoding scheme is covered in a section of this document and/or in the referenced specification. This version of the specification includes support for:

* Protocol Buffers Version 3 [@PROTOBUF]

**[R-ENC.0]{}** - An implementation using protocol buffers encoding to encode USP Messages (Requests, Responses, and Errors) MUST conform to the schema defined in [%usp-msg-proto-file%](%usp-msg-proto-url%).

**[R-ENC.1]{}** - An implementation using protocol buffers encoding to encode USP Records MUST conform to the schema defined in [%usp-record-proto-file%](%usp-record-proto-url%).

Protocol Buffers Version 3 uses a set of enumerated elements to coordinate encoding and decoding during transmission. It is intended that these remain backwards compatible, but new versions of the schema may contain new enumerated elements.

**[R-ENC.2]{}** - If an Endpoint receives a USP payload containing an unknown enumeration value for a known field, the Endpoint MUST report the failure to the receiving MTP to indicate a “bad request” and do no further processing of the USP Record or USP Message.

Protocol Buffers uses a datatype called `oneof`. This means that the element
contains elements of one or more varying types.

**[R-ENC.3]{}** - USP Records and USP Messages that contain an element of type
`oneof` MUST include 1 and only 1 instance of the element, which MUST contain
one of the possible elements.

**[R-ENC.4]{}** - A USP Record that violates [R-ENC.3]() MUST be discarded.

**[R-ENC.5]{}** - A USP Message that violates [R-ENC.3]() SHOULD return an error of
type 7004 (Invalid Arguments).

## Parameter and Argument Value Encoding {#parameter-value-encoding}

[%usp-msg-proto-file%](%usp-msg-proto-url%) specifies that Parameter
and argument values in USP Messages are represented as Protocol Buffers Version
3 strings (which are UTF-8-encoded).

This section specifies how Parameter and argument values are converted to and
from Protocol Buffers Version 3 strings.

**[R-ENC.6]{}** - Parameter and argument values MUST be converted to and from
Protocol Buffers Version 3 strings using the string representations of the
TR-106 Appendix I.4 [@TR-106] data types.

TR-106 Appendix I.4 states that "Parameters make use of a limited subset of the
default SOAP data types". The
SOAP 1.1 specification [@SOAP-1-1] states
that all SOAP simple types are defined by the
XML Schema Part 2: Datatypes specification [@XMLSCHEMA-2],
and this is the ultimate reference.

In practice there should be few surprises, e.g.,
XML Schema Part 2, Section 3.3.22 [@XMLSCHEMA-2]
states that it has a lexical representation consisting of a finite-length
sequence of decimal digits (#x30-#x39).

Some of the encoding rules are quite complicated,
e.g. SOAP 1.1, Section 5.2.3 [@SOAP-1-1]
states that `base64` line length restrictions don't apply to SOAP, and
XML Schema Part 2, Section 3.2.7 [@XMLSCHEMA-2]
has a lot of detail about which aspects of ISO 8601 are and are not supported
by the `dateTime` data type.
