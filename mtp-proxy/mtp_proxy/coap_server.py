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
# File Name: coap_server.py
#
# Description: A CoAP Server that receives CoAP messages from a USP Endpoint
#
"""

import logging
import threading

import asyncio
from asyncio import ensure_future as asyncio_ensure_future
import aiocoap
import aiocoap.resource

from mtp_proxy import utils


class MyCoapResource(aiocoap.resource.Resource):
    """A CoAP Resource for receiving USP messages"""
    def __init__(self, resource_path, queue):
        """Initialize our USP CoAP Resource"""
        aiocoap.resource.Resource.__init__(self)
        self._queue = queue
        self._resource_path = resource_path
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("New CoAP Resource created for Resource: %s", resource_path)

    @asyncio.coroutine
    def render_get(self, request):
        """CoAP Resource for USP - handle the GET Method"""
        self._logger.warning("GET:: Received a CoAP Request on Resource [%s]; only POST is allowed",
                             self._resource_path)
        return aiocoap.Message(code=aiocoap.Code.METHOD_NOT_ALLOWED)

    @asyncio.coroutine
    def render_put(self, request):
        """CoAP Resource for USP - handle the PUT Method"""
        self._logger.warning("PUT:: Received a CoAP Request on Resource [%s]; only POST is allowed",
                             self._resource_path)
        return aiocoap.Message(code=aiocoap.Code.METHOD_NOT_ALLOWED)

    @asyncio.coroutine
    def render_delete(self, request):
        """CoAP Resource for USP - handle the DELETE Method"""
        self._logger.warning("DELETE:: Received a CoAP Request on Resource [%s]; only POST is allowed",
                             self._resource_path)
        return aiocoap.Message(code=aiocoap.Code.METHOD_NOT_ALLOWED)

    @asyncio.coroutine
    def render_post(self, request):
        """CoAP Resource for USP - handle the POST Method"""
        self._logger.info("POST:: Received a CoAP Request on Resource: %s", self._resource_path)
        self._logger.debug("Payload received: [%s]", request.payload)
        self._logger.debug("Incoming Request opt.uri_path: [%s]", request.opt.uri_path)
        self._logger.debug("Incoming Request opt.uri_query: [%s]", request.opt.uri_query)
        self._logger.debug("Incoming Request opt.uri_host: [%s]", request.opt.uri_host)
        self._logger.debug("Incoming Request opt.uri_port: [%s]", request.opt.uri_port)

        if request.opt.content_format == 42:
            self._logger.debug("Incoming CoAP POST Request Content-Format Validated")

            reply_to_addr = self._retrieve_reply_to_addr(request.opt.uri_query)
            if reply_to_addr is not None:
                self._logger.debug("Incoming CoAP POST Request URI-Query Validated")

                queue_item = utils.ExpiringQueueItem(request.payload, reply_to_addr)
                queue_item.set_coap_details(self._resource_path)
                asyncio.get_event_loop().call_soon(self._queue.push, queue_item)
                response = aiocoap.Message(code=aiocoap.Code.CHANGED)
                self._logger.info("Responding to the CoAP Request with a 2.04 Status Code")
            else:
                # Failed 'reply-to' URI-Query Validation, respond with 4.00
                self._logger.warning("The 'reply-to' address on the Incoming CoAP Request is missing")
                response = aiocoap.Message(code=aiocoap.Code.BAD_REQUEST)
                self._logger.info("Responding to the CoAP Request with a 4.00 Status Code")
        else:
            # Failed Content Format (expected: application/octet-stream), respond with 4.15
            self._logger.warning("Incoming CoAP Request contained an Unsupported Content-Format: %s",
                                 str(request.opt.content_format))
            response = aiocoap.Message(code=aiocoap.Code.UNSUPPORTED_MEDIA_TYPE)
            self._logger.info("Responding to the CoAP Request with a 4.15 Status Code")

        return response

    def get_link_description(self):
        """"Configure the link description as a USP Controller, even though we are really an MTP Proxy"""
        link = aiocoap.resource.Resource.get_link_description(self)

        link['rt'] = "usp.endpoint"
        link['if'] = "usp.c"

        return link

    def get_queue(self):
        """Retrieve the internal Queue"""
        return self._queue

    def _retrieve_reply_to_addr(self, uri_query):
        """Retreive the reply-to address from the URI-Query of the incoming CoAP message"""
        reply_to_addr = None

        for query_item in uri_query:
            self._logger.debug("Processing URI-Query Item: %s", query_item)
            query_item_parts = query_item.split("=")

            if query_item_parts[0] == "reply-to":
                reply_to_addr = "coap://" + query_item_parts[1]
                self._logger.debug("Found 'reply-to' URI Query; value altered to: %s", reply_to_addr)

        return reply_to_addr


class CoapReceivingThread(threading.Thread):
    """A Thread that executes the AsyncIO Event Loop Processing to receive CoAP messages"""
    def __init__(self, resource_tree, ip_addr, listening_port, debug=False):
        """Initialize the CoAP Receiving Thread"""
        threading.Thread.__init__(self, name="CoAP Receiving Thread: " + str(listening_port))
        self._debug = debug
        self._ip_addr = ip_addr
        self._resource_tree = resource_tree
        self._listening_port = listening_port
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        """Listen for incoming CoAP messages for the Resources provided"""
        # The server context contains the "usp" resource, which ties back to our MyCoapResource, so when
        #  the event loop receives a message against the "usp" resource the render_XXX method in the
        #  MyCoapResource instance is called, which will push the message onto the binding (if appropriate)
        self._logger.debug("Creating a new AsyncIO Event Loop")
        my_event_loop = asyncio.new_event_loop()
        my_event_loop.set_debug(self._debug)
        asyncio.set_event_loop(my_event_loop)
        self._logger.info("Creating a CoAP Server Context for the Resource Tree with IP [%s] and Port [%d]",
                          self._ip_addr, self._listening_port)
        asyncio_ensure_future(
            aiocoap.Context.create_server_context(self._resource_tree, bind=(self._ip_addr, self._listening_port)))

        self._logger.info("Starting the AsyncIO CoAP Event Loop")
        my_event_loop.run_forever()
        self._logger.info("The AsyncIO CoAP Event Loop has Terminated")
        my_event_loop.close()


class CoapServer:
    """A CoAP Server that receives CoAP Messages for re-distribution"""
    def __init__(self, ip_addr, listen_port=5683, sending_thr_timeout=5, debug=False):
        """Initialize the CoAP USP Binding for a USP Endpoint
            - 5683 is the default CoAP port, but 5684 is the default CoAPS port"""
        self._debug = debug
        self._ip_addr = ip_addr
        self._address_dict = {}
        self._resource_dict = {}
        self._listen_thread = None
        self._listen_port = listen_port
        self._sending_thr_timeout = sending_thr_timeout
        self._resource_tree = aiocoap.resource.Site()
        self._logger = logging.getLogger(self.__class__.__name__)

        # Initial population of the Server Resource Tree
        self._resource_tree.add_resource(('.well-known', 'core'),
                                         aiocoap.resource.WKCResource(self._resource_tree.get_resources_as_linkheader))

    def listen(self):
        """Listen for incoming CoAP messages"""
        # An Endpoint needs a Server Context for the Resource Tree
        self._logger.info("Starting the CoAP Receiving Thread")
        self._listen_thread = CoapReceivingThread(self._resource_tree, self._ip_addr, self._listen_port, self._debug)
        self._listen_thread.start()

    def add_resource(self, resource_path):
        """Add a new CoAP Resource to the Resource Tree"""
        queue = utils.GenericReceivingQueue()
        resource = MyCoapResource(resource_path, queue)
        addr = "coap://" + self._ip_addr + ":" + str(self._listen_port) + "/" + resource_path
        self._logger.info("Adding a New CoAP Resource: %s", resource_path)
        self._resource_tree.add_resource((resource_path,), resource)
        self._resource_dict[resource_path] = resource
        self._address_dict[resource_path] = addr
        self._logger.info("Listening at URL: %s", addr)

    def get_addr_by_resource_path(self, resource_path):
        """Retrieve the CoAP Address associated with the given resource_path"""
        addr = None

        if resource_path in self._address_dict:
            addr = self._address_dict[resource_path]

        return addr

    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve a Queue Item from the queue"""
        queue_item = None
        for resource_path in self._resource_dict:
            queue = self._resource_dict[resource_path].get_queue()
            queue_item = queue.get_msg(timeout_in_seconds)
            if queue_item is not None:
                break

        return queue_item
