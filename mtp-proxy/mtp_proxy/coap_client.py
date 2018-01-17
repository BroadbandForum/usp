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
# File Name: coap_client.py
#
# Description: A CoAP Client for sending CoAP Messages to a USP Endpoint
#
"""

import logging
import threading

import asyncio
import aiocoap
import aiocoap.error


class CoapSendingThread(threading.Thread):
    """A Thread that executes the AsyncIO Event Loop Processing to send a single CoAP message"""
    def __init__(self, payload, my_addr, to_addr, debug=False):
        """Initialize the CoAP Sending Thread"""
        threading.Thread.__init__(self, name="CoAP Sending Thread - " + to_addr)
        self._debug = debug
        self._payload = payload
        self._to_addr = to_addr
        self._logger = logging.getLogger(self.__class__.__name__)

        self._reply_to = my_addr.split("://")[1]
        self._logger.debug("Using [%s] as the value of the reply-to URI Query Option", self._reply_to)

    def run(self):
        """Send a CoAP message to the specified address"""
        self._logger.debug("Creating a new AsyncIO Event Loop")
        my_event_loop = asyncio.new_event_loop()
        my_event_loop.set_debug(self._debug)
        asyncio.set_event_loop(my_event_loop)

        my_event_loop.run_until_complete(self._issue_request(self._payload, self._to_addr))
        my_event_loop.close()

    @asyncio.coroutine
    def _issue_request(self, payload, to_addr):
        """Send the specified payload to the specified CoAP URL via the POST Method"""
        msg = aiocoap.Message(code=aiocoap.Code.POST, payload=payload)
        msg.opt.content_format = 42
        msg.set_request_uri(to_addr + "?reply-to=" + self._reply_to)

        self._logger.debug("Creating a CoAP Client Context")
        context = yield from aiocoap.Context.create_client_context()

        self._logger.info("Sending a CoAP message to the following address: %s", to_addr)
        try:
            resp = yield from context.request(msg).response
            self._logger.info("CoAP Message Sent and [%s] Response received", resp.code)
        except aiocoap.error.RequestTimedOut:
            self._logger.warning("CoAP Message Sent, but no Response received due to a Timeout Error")


class CoapClient(object):
    """A CoAP Client that sends CoAP Messages as requested"""
    def __init__(self, my_addr, to_addr, thr_timeout=10, debug=False):
        """Initialize the CoAP Client with the address to use when sending messages"""
        self._debug = debug
        self._my_addr = my_addr
        self._to_addr = to_addr
        self._thr_timeout = thr_timeout
        self._logger = logging.getLogger(self.__class__.__name__)

    def send_msg(self, payload):
        """Send a CoAP Message"""
        self._logger.info("Starting a CoAP Sending Thread")
        coap_send_thr = CoapSendingThread(payload, self._my_addr, self._to_addr, self._debug)
        coap_send_thr.start()
        coap_send_thr.join(self._thr_timeout)
