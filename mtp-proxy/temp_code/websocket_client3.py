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
# File Name: websocket_client.py
#
# Description: A WebSockets Client for sending WebSocket Messages to a USP Endpoint
#
"""

import asyncio
import logging
import threading
import websockets

from mtp_proxy import utils


class WebSocketConnListener(threading.Thread):
    """A Thread that handles incoming WebSocket messages"""
    def __init__(self, address, queue, debug=False):
        """Initialize the CoAP Receiving Thread"""
        threading.Thread.__init__(self, name="WebSockets Receiving Thread: " + str(address))
        self._conn = None
        self._debug = debug
        self._queue = queue
        self._address = address
        self._my_event_loop = None
        self._logger = logging.getLogger(self.__class__.__name__)

    async def _connect(self, event_loop):
        self._logger.info("Trying to connect to: %s", self._address)
        async with websockets.connect(self._address, binaryType="arrayBuffer", subprotocols=["v1.usp"]) as self._conn:
            self._logger.info("Connected to: %s", self._address)
            while True:
                await self._recv_messages()

    async def _recv_messages(self):
#        self._logger.info("Trying to connect to: %s", self._address)
#        async with websockets.connect(self._address, subprotocols=["v1.usp"]) as self._conn:
        msg = await self._conn.recv()
        self._logger.info("Received message: %s", msg)
        queue_item = utils.ExpiringQueueItem(msg, reply_to_addr="")
        self._queue.push(queue_item)

    async def _send_message(self, message):
        self._logger.info("Attempting to send message - 2: %s", message)
        self._logger.info("Attempting to send message - 3: %s", self._conn)
        await self._conn.send(message)
#        self._conn.send(message)

    def send_message(self, message):
        self._logger.info("Attempting to send message - 1: %s", message)
        self._logger.debug("Creating a new AsyncIO Event Loop")
        my_event_loop = asyncio.new_event_loop()
        my_event_loop.set_debug(self._debug)
        asyncio.set_event_loop(my_event_loop)

        my_event_loop.run_until_complete(self._send_message(message))
        my_event_loop.close()

    def run(self):
        """Listen for incoming WebSocket messages"""
        self._logger.debug("Creating a new AsyncIO Event Loop")
        my_event_loop = asyncio.new_event_loop()
        my_event_loop.set_debug(self._debug)
        asyncio.set_event_loop(my_event_loop)

        my_event_loop.run_until_complete(self._connect(my_event_loop))
        my_event_loop.close()


class WebSocketClient:
    """A WebSocket Client that sends WebSocket Messages as requested"""
    def __init__(self, host, port, path, debug=False):
        """Initialize the WebSocket Client"""
        self._conn = None
        self._port = port
        self._debug = debug
        self._address = "ws://" + host + ":" + str(port) + "/" + path
        self._queue = utils.GenericReceivingQueue()
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve a Queue Item from the queue"""
        return self._queue.get_msg(timeout_in_seconds)

    def send_msg(self, payload):
        """Send a WebSocket message (binary only)"""
        self._conn.send_message(payload)
        self._logger.info("Message [%s] Sent as binary!", payload)

    def listen(self):
        """Listen to events from the WebSocket connection"""
        self._logger.info("Starting the WebSocket Connection Listener Thread")
        self._conn = WebSocketConnListener(self._address, self._queue)
        self._conn.start()
