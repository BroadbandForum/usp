# **************************************************************************
# WT-369 USP Message Protocol Buffer Schema
#
#  Copyright (c) 2017, Broadband Forum
#
#  The undersigned members have elected to grant the copyright to
#  their contributed material used in this software:
#    Copyright (c) 2017 ARRIS Enterprises, LLC.
#
# This is draft software, is subject to change, and has not been approved
#  by members of the Broadband Forum. It is made available to non-members
#  for internal study purposes only. For such study purposes, you have the
#  right to make copies and modifications only for distributing this software
#  internally within your organization among those who are working on it
#  (redistribution outside of your organization for other than study purposes
#  of the original or modified works is not permitted). For the avoidance of
#  doubt, no patent rights are conferred by this license.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.
#
# Unless a different date is specified upon issuance of a draft software
#  release, all member and non-member license rights under the draft software
#  release will expire on the earliest to occur of (i) nine months from the
#  date of issuance, (ii) the issuance of another version of the same software
#  release, or (iii) the adoption of the draft software release as final.
#
# BBF software release registry: http:##www.broadband-forum.org/software
# **************************************************************************

"""
#
# File Name: test_utils.py
#
# Description: Unit tests for utils
#
# Functionality: Test the GenericReceivingQueue Class
#
"""

import time

import unittest.mock as mock

from mtp_proxy import utils


def test_empty_pop():
    queue = utils.GenericReceivingQueue()
    received_payload = queue.pop()

    assert received_payload is None


def test_one_entry():
    payload = "TEST"
    queue = utils.GenericReceivingQueue()
    queue.push(payload)
    received_payload = queue.pop()

    assert payload == received_payload


def test_multiple_entries_seq():
    payload1 = "TEST1"
    payload2 = "TEST2"
    payload3 = "TEST3"
    payload4 = "TEST4"
    queue = utils.GenericReceivingQueue()
    queue.push(payload1)
    queue.push(payload2)
    queue.push(payload3)
    queue.push(payload4)
    received_payload1 = queue.pop()
    received_payload2 = queue.pop()
    received_payload3 = queue.pop()
    received_payload4 = queue.pop()

    assert payload1 == received_payload1
    assert payload2 == received_payload2
    assert payload3 == received_payload3
    assert payload4 == received_payload4


def test_multiple_entries_not_seq():
    payload1 = "TEST1"
    payload2 = "TEST2"
    payload3 = "TEST3"
    payload4 = "TEST4"
    queue = utils.GenericReceivingQueue()
    queue.push(payload1)
    queue.push(payload2)
    received_payload1 = queue.pop()
    queue.push(payload3)
    received_payload2 = queue.pop()
    received_payload3 = queue.pop()
    queue.push(payload4)
    received_payload4 = queue.pop()

    assert payload1 == received_payload1
    assert payload2 == received_payload2
    assert payload3 == received_payload3
    assert payload4 == received_payload4


def test_get_msg_found():
    timeout = 15
    payload = "TEST"
    time_mock = mock.Mock()
    time_mock.return_value = None

    queue = utils.GenericReceivingQueue(5)
    queue.push(payload)

    with mock.patch("time.sleep", time_mock):
        received_payload = queue.get_msg(timeout)

    assert payload == received_payload


def test_get_msg_not_found_empty_queue():
    timeout = 15
    time_mock = mock.Mock()
    time_mock.return_value = None

    queue = utils.GenericReceivingQueue(5)

    with mock.patch("time.sleep", time_mock):
        received_payload = queue.get_msg(timeout)

    assert received_payload is None


def test_get_msg_no_timeout():
    payload = "TEST"

    queue = utils.GenericReceivingQueue()
    queue.push(payload)

    received_payload = queue.get_msg()

    assert received_payload is payload


def test_get_msg_expired():
    timeout = 15
    payload = "TEST"
    time_mock = mock.Mock()
    time_mock.return_value = None
    time_time_mock = mock.Mock()
    time_time_mock.return_value = time.time() + 61

    queue = utils.GenericReceivingQueue(5)
    queue.push(payload)

    with mock.patch("time.sleep", time_mock):
        with mock.patch("time.time", time_time_mock):
            received_payload = queue.get_msg(timeout)

    assert received_payload is None
