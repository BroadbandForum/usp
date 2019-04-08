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
# File Name: websocket_server.py
#
# Description: A WebSockets Server that receives WebSocket messages from a USP Endpoint
#
"""

import logging
import threading
import simple_websocket_server

from mtp_proxy import utils

# TODO: Create MySimpleWebSocketServer(simple_websocket_server.WebSocketServer)
### __init__ also accepts a queue
### Have it expose a get_websocket() - get first in the list and warn if more than 1; return None if list is empty
### Expand _construct_websocket() to call set_queue after the WebSocket is constructed

#my_global_cli_conn = None
#my_global_queue = utils.GenericReceivingQueue()


#def get_queue():
#    return my_global_queue


#def add_item_to_queue(item):
#    my_global_queue.push(item)


#def client_connected(web_socket_conn):
#    global my_global_cli_conn
#    my_global_cli_conn = web_socket_conn


#def client_disconnected():
#    global my_global_cli_conn
#    my_global_cli_conn = None


#def is_websocket_client_connected():
#    global my_global_cli_conn
#    return my_global_cli_conn is not None


#def get_websocket_client_connection():
#    global my_global_cli_conn
#    return my_global_cli_conn


class WebSocketListeningThread(threading.Thread):
    """A Thread that executes the AsyncIO Event Loop Processing to receive CoAP messages"""
    def __init__(self, host, port, path, queue, debug=False):
        """Initialize the CoAP Receiving Thread"""
        threading.Thread.__init__(self, name="WebSocket Listening Thread: " + str(port))
        self._host = host
        self._port = port
        self._path = path
        self._queue = queue
        self._debug = debug
#        self._client = None
        self._server = None
        self._logger = logging.getLogger(self.__class__.__name__)

    def send_msg(self, payload):
        """Send a WebSocket message (binary only)"""
        client = self._server.get_connected_client()

        if client is not None:
            client.send_message(payload)
#        if is_websocket_client_connected():
#            get_websocket_client_connection().send_message(payload)
            self._logger.info("Message [%s] Sent!", payload)
        else:
            self._logger.warning("No Client connected, skipping message")

    def run(self):
        """Listen for incoming CoAP messages for the Resources provided"""
#        self._server = simple_websocket_server.WebSocketServer(self._host, self._port, WebSocketServerHandler)
        self._server = ExtendedSimpleWebSocketServer(self._host, self._port, self._queue, WebSocketServerHandler)
        self._logger.info("Establishing: ws://%s:%d", self._host, self._port)
        self._server.serve_forever()


class WebSocketServerHandler(simple_websocket_server.WebSocket):
    """A WebSocket Server Handler : defining __init__ seems to always break things, so avoiding it"""
#    def __init__(self, server, sock, address):
#        """Extend the WebSocket to implement the Handler methods and use a Queue"""
#        simple_websocket_server.WebSocket.__init__(self, server, sock, address)
#        self._queue = None
#        self._logger = logging.getLogger(self.__class__.__name__)

#    def set_queue(self, queue):
#        """Set the Queue to use when receiving a message"""
#        self._queue = queue

    def handle(self):
        """Handle incoming WebSocket messages; add them to the global Queue"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Received a WebSocket message")
        logger.info("Payload received: [%s]", self.data)

        if self._queue is not None:
            queue_item = utils.ExpiringQueueItem(self.data, reply_to_addr="")
            self._queue.push(queue_item)
        else:
            logger.warning("Queue has not been set: incoming message dropped")
#        add_item_to_queue(queue_item)

    def connected(self):
        """Handle notification of a new WebSocket Client Connecting"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("New client connected: %s", self.address)
        self._queue = self.server.get_queue()
#        client_connected(self)

    def handle_close(self):
        """Handle notification of a WebSocket Client Disconnecting"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.warning("Client disconnected: %s", self.address)
#        client_disconnected()


class ExtendedSimpleWebSocketServer(simple_websocket_server.WebSocketServer):
    """My extension of the Simple WebSocket Server to prevent globals"""
    def __init__(self, host, port, queue, websocketclass):
        """Initialize the Extended Simple WebSocket Server"""
        simple_websocket_server.WebSocketServer.__init__(self, host, port, websocketclass)
        self._queue = queue
#        self._logger = logging.getLogger(self.__class__.__name__)

    def get_queue(self):
        """Retrieve the Queue"""
        return self._queue

#    def _construct_websocket(self, sock, address):
#        """Extend the WebSocket construction method to provide a Queue to the WebSocket Handler"""
#        ws = simple_websocket_server.WebSocketServer._construct_websocket(self, sock, address)
#        ws.set_queue(self._queue)

    def get_connected_client(self):
        """There should only be 1 connected WebSocket client, so retrieve it"""
        connected_client = None
        logger = logging.getLogger(self.__class__.__name__)

        if len(self.connections) > 0:
            connected_client = next(iter(self.connections.values()))
#            for connected_client in self.connections.values():
#                break

        if len(self.connections) > 1:
            logger.warning("Attempting to retrieve the connected WebSocket; Found more than 1!")

        return connected_client


class WebSocketServer:
    """A WebSocket Server that sends & receives WebSocket Messages"""
    def __init__(self, host, port, path, debug=False):
        """Initialize the WebSocket Client"""
        self._host = host
        self._port = port
        self._path = path
        self._debug = debug
        self._listen_thr = None
        self._queue = utils.GenericReceivingQueue()
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve a Queue Item from the queue"""
#        return get_queue().get_msg(timeout_in_seconds)
        return self._queue.get_msg(timeout_in_seconds)

    def send_msg(self, payload):
        """Send a WebSocket message (binary only)"""
        self._listen_thr.send_msg(payload)

    def listen(self):
        """Listen to events from the WebSocket connection"""
        self._logger.info("Starting the WebSocket Listening Thread...")
#        self._listen_thr = WebSocketListeningThread(self._host, self._port, self._path)
        self._listen_thr = WebSocketListeningThread(self._host, self._port, self._path, self._queue)
        self._listen_thr.start()
