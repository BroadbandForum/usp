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

import logging
import threading
import lomond

from mtp_proxy import utils


class WebSocketConnListener(threading.Thread):
    """A Thread that handles incoming WebSocket messages"""
    def __init__(self, conn, queue, listening_port, debug=False):
        """Initialize the CoAP Receiving Thread"""
        threading.Thread.__init__(self, name="WebSockets Receiving Thread: " + str(listening_port))
        self._conn = conn
        self._debug = debug
        self._queue = queue
        self._listening_port = listening_port
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        """Listen for incoming WebSocket messages"""
        for event in self._conn:
            if event.name == "connecting":
                self._logger.info("Connecting...")
            elif event.name == "connected":
                self._logger.info("Connected!")
            elif event.name == "ready":
                self._logger.info("And... Ready!")
            elif event.name == "binary":
                self._logger.info("Received a Binary Message; maybe it is a USP Record")
                self._logger.debug("Binary Message Contents: %s", str(event.data))
                queue_item = utils.ExpiringQueueItem(event.data, reply_to_addr="")
                self._queue.push(queue_item)
            elif event.name == "text":
                self._logger.info("Received a Text Message; Discarding...")
                self._logger.debug("Text Message Contents: %s", event.text)
            elif event.name == "poll":
                self._logger.debug("Received a Poll event... ignoring")
            elif event.name == "ping":
                self._logger.debug("Received a Ping event... auto-pong enabled, ignoring")
            elif event.name == "pong":
                self._logger.debug("Received a Pong event... ignoring")
            elif event.name == "closed":
                self._logger.info("Closed!")
            elif event.name == "disconnected":
                self._logger.info("Disconnected!")
            else:
                self._logger.warning("Unknown event received: %s", event.name)


class WebSocketClient:
    """A WebSocket Client that sends WebSocket Messages as requested"""
    def __init__(self, host, port, path, debug=False):
        """Initialize the WebSocket Client"""
        self._port = port
        self._debug = debug
        self._address = "ws://" + host + ":" + str(port) + "/" + path
        self._queue = utils.GenericReceivingQueue()
        self._logger = logging.getLogger(self.__class__.__name__)

        self._conn = lomond.WebSocket(self._address, protocols=["v1.usp"])
        self._logger.info("Trying to connect to: %s", self._address)

    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve a Queue Item from the queue"""
        return self._queue.get_msg(timeout_in_seconds)

    def send_msg(self, payload):
        """Send a WebSocket message (binary only)"""
        self._conn.send_binary(payload, compress=False)
        self._logger.info("Message [%s] Sent as binary!", payload)

    def listen(self):
        """Listen to events from the WebSocket connection"""
        self._logger.info("Starting the WebSocket Connection Listener Thread")
        conn_listener = WebSocketConnListener(self._conn, self._queue, self._port)
        conn_listener.start()
