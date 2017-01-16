#!/usr/bin/env python3

# Copyright 2017 ARRIS Enterprises, LLC.

"""Simple USP protobuf test program."""

import usp_pb2 as usp

import google.protobuf as protobuf

msg = usp.Msg()
msg.header.msg_id = "1"
msg.header.msg_type = msg.header.GET
msg.body.request.get.param_path.append("a")
msg.body.request.get.param_path.append("b")
msg.body.request.get.param_path.append("c")

print(msg)
