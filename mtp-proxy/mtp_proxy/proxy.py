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
# File Name: proxy.py
#
# Description: A MTP Proxy to deliver messages across different USP MTPs
#
"""

import json
import time
import logging
import argparse
import threading

from mtp_proxy import utils
from mtp_proxy import coap_mtp
from mtp_proxy import stomp_mtp
from mtp_proxy import websocket_mtp


class Proxy:
    """A Class for proxying messages between USP MTPs"""
    def __init__(self, cfg_file_name, log_file_name, log_level=logging.INFO, fail_bad_content_type=False):
        """Initialize the Proxy Class"""
        self._my_ip_addr = None
        self._proxy_thr_list = []
        self._cfg_file_contents = None
        self._debug = (log_level == logging.DEBUG)
        self._fail_bad_content_type = fail_bad_content_type

        logging.basicConfig(filename=log_file_name, level=log_level,
                            format='%(asctime)-15s %(name)s %(levelname)-8s %(message)s')
        self._logger = logging.getLogger(self.__class__.__name__)

        # Handle Command Line Arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--intf", action="store", nargs="?",
                            type=str, default=None,
                            help="specify the network interface to use")
        args = parser.parse_args()

        self._my_ip_addr = utils.IPAddr.get_ip_addr(args.intf)

        self._logger.info("#######################################################")
        self._logger.info("## Starting MTP Proxy")
        self._logger.info("#######################################################")

        self._read_config_file(cfg_file_name)

    def process_config_file(self):
        """Process the Configuration File Contents to create the Proxy Threads"""
        if "AssociationList" in self._cfg_file_contents:
            association_list = self._cfg_file_contents["AssociationList"]
            for association_dict in association_list:
                proxy_thr = ProxyThread()

                if "CoAP" in association_dict["Association"]:
                    # ProxyPort : CoAP Port that the MTP Proxy is listening on
                    # ProxyResource : Default CoAP Resource associated with the MTP Proxy
                    #                  This is typically used by the Proxied USP Endpoint when sending Notifications
                    # EndpointURL : CoAP URL for the USP Endpoint being proxied
                    self._logger.info("Found a CoAP MTP")
                    coap_dict = association_dict["Association"]["CoAP"]
                    default_resource_path = coap_dict["ProxyResource"]
                    coap_mtp_inst = coap_mtp.CoapMtp(self._my_ip_addr, coap_dict["ProxyPort"],
                                                     default_resource_path, self._debug)
                    endpoint_addr = coap_dict["EndpointURL"]
                    proxy_thr.add_coap_mtp(coap_mtp_inst, endpoint_addr)

                if "STOMP" in association_dict["Association"]:
                    # Host : Hostname or IP Address of the STOMP Server
                    # Port : Port of the STOMP Server
                    # VirtualHost : Virtual Host to be used when connecting to the STOMP Server
                    # Username : Username to be used when connecting to the STOMP Server
                    #             Server will validate as part of credentials
                    # Password : Password to be used when connecting to the STOMP Server
                    #             Server will validate as part of credentials
                    # ProxyDestination : Default STOMP Destination associated with the MTP Proxy
                    #                     This is typically used by the Proxied USP Endpoint when sending Notifications
                    #                     This can be overridden by the STOMP Server via the subscribe-dest header
                    # EndpointDestination : STOMP Destination of the USP Endpoint being proxied
                    # ProxyEndpointID : Endpoint ID of the USP Endpoint being proxied
                    #                    This is used in the endpoint-id header within the STOMP CONNECT Frame
                    self._logger.info("Found a STOMP MTP")
                    stomp_dict = association_dict["Association"]["STOMP"]
                    proxy_addr = stomp_dict["ProxyDestination"]
                    stomp_mtp_inst = stomp_mtp.StompMtp(stomp_dict["Host"], stomp_dict["Port"],
                                                        stomp_dict["Username"], stomp_dict["Password"],
                                                        stomp_dict["VirtualHost"], proxy_addr,
                                                        proxy_endpoint_id=stomp_dict["ProxyEndpointID"],
                                                        fail_bad_content_type=self._fail_bad_content_type)
                    endpoint_addr = stomp_dict["EndpointDestination"]
                    proxy_thr.add_stomp_mtp(stomp_mtp_inst, endpoint_addr)

                if "WebSocket" in association_dict["Association"]:
                    # Name : Unique Name of WebSocket Connection
                    # Host : Hostname or IP Address portion of the WebSocket URL
                    # Port : Port portion of the WebSocket URL
                    # Path : Path portion of the WebSocket URL
                    # Client : True if running as a WebSocket Client; False if running as a WebSocket Server
                    self._logger.info("Found a WebSocket MTP")
                    websocket_dict = association_dict["Association"]["WebSocket"]
                    websocket_name = websocket_dict["Name"]
                    websocket_mtp_inst = websocket_mtp.WebSocketsMtp(websocket_dict["Host"],
                                                                     websocket_dict["Port"],
                                                                     websocket_dict["Path"],
                                                                     websocket_dict["Client"])
                    proxy_thr.add_websocket_mtp(websocket_mtp_inst, websocket_name)

                self._proxy_thr_list.append(proxy_thr)

    def start_threads(self):
        """Start all of the Proxy Threads"""
        for proxy_thr_item in self._proxy_thr_list:
            proxy_thr_item.start()

    def wait_for_threads(self):
        """Wait for all Proxy Threads to stop - Should Never Happen"""
        for proxy_thr_item in self._proxy_thr_list:
            proxy_thr_item.join()

    def _read_config_file(self, cfg_file_name):
        """Read the Config File and Place contents into a Dictionary"""
        try:
            with open(cfg_file_name, "r") as cfg_file:
                try:
                    self._cfg_file_contents = json.load(cfg_file)
                    self._logger.info("Config File %s read successfully", cfg_file_name)
                except ValueError:
                    self._logger.warning("Error reading config file %s - JSON Parse Error", cfg_file_name)
        except FileNotFoundError:
            self._logger.warning("Error reading config file %s - File Read Error", cfg_file_name)


class ProxyThread(threading.Thread):
    """A Threaded MTP Proxy Handler"""
    def __init__(self, sleep_time_interval=1):
        """Initialize the Proxy Thread"""
        threading.Thread.__init__(self)
        self._coap_mtp = None
        self._stomp_mtp = None
        self._websocket_mtp = None
        self._mtp_bitmap = 0   # 1 for CoAP, 2 for STOMP, 4 for WebSockets
        self._websocket_name = None
        self._coap_endpoint_addr = None
        self._stomp_proxy_addr = None
        self._stomp_endpoint_addr = None
        self._last_stomp_reply_to_addr = None
        self._coap_resp_resource_dict = {}  # Map CoAP Resource Paths (Key) to STOMP Destinations (Value)
        self._sleep_time_interval = sleep_time_interval
        self._logger = logging.getLogger(self.__class__.__name__)

    def add_coap_mtp(self, mtp, endpoint_addr):
        """Add a CoAP MTP configuration to the Proxy Thread"""
        if self._coap_mtp is None:
            self._coap_mtp = mtp
            self._mtp_bitmap += 1
            self._coap_endpoint_addr = endpoint_addr
            self._logger.info("Adding a CoAP MTP")
        else:
            self._logger.warning("Can't add another CoAP MTP; the CoAP MTP is already configured")

    def add_stomp_mtp(self, mtp, endpoint_addr):
        """Add a STOMP MTP configuration to the Proxy Thread"""
        if self._stomp_mtp is None:
            self._stomp_mtp = mtp
            self._mtp_bitmap += 2
            self._stomp_endpoint_addr = endpoint_addr
            self._logger.info("Adding a STOMP MTP")
        else:
            self._logger.warning("Can't add another STOMP MTP; the STOMP MTP is already configured")

    def add_websocket_mtp(self, mtp, name):
        """Add a WebSocket MTP configuration to the Proxy Thread"""
        if self._websocket_mtp is None:
            self._websocket_mtp = mtp
            self._mtp_bitmap += 4
            self._websocket_name = name
            self._logger.info("Adding a WebSocket MTP")
        else:
            self._logger.warning("Can't add another WebSocket MTP; the WebSocket MTP is already configured")

    def run(self):
        """Start listening to the appropriate MTPs"""
        if self._coap_mtp is not None:
            self._coap_mtp.listen()

        if self._stomp_mtp is not None:
            self._stomp_mtp.listen()
            self._stomp_proxy_addr = self._stomp_mtp.get_subscribed_to_dest()

        if self._websocket_mtp is not None:
            self._websocket_mtp.listen()

        should_run = self._validate_mtp_combinations()

        while should_run:
            time.sleep(self._sleep_time_interval)

            if self._mtp_bitmap == 3:
                # NOTE: CoAP Controller to STOMP Agent won't work :: No STOMP Broker available
                self._read_coap_send_stomp()
                self._read_stomp_send_coap()
            elif self._mtp_bitmap == 5:
                self._read_coap_send_websocket()
                self._read_websocket_send_coap()
            elif self._mtp_bitmap == 6:
                # NOTE: WebSocket Controller to STOMP Agent won't work :: No STOMP Broker available
                self._read_websocket_send_stomp()
                self._read_stomp_send_websocket()
            else:
                self._logger.error("Unknown MTP Association Configuration")
                break

    def _validate_mtp_combinations(self):
        """Validate the configured MTP Combinations"""
        should_run = False

        if self._mtp_bitmap == 0:
            self._logger.error("No MTPs configured")
        elif self._mtp_bitmap == 1:
            self._logger.error("Only the CoAP MTP was configured")
        elif self._mtp_bitmap == 2:
            self._logger.error("Only the STOMP MTP was configured")
        elif self._mtp_bitmap == 3:
            # NOTE: CoAP Controller to STOMP Agent won't work :: No STOMP Broker available
            should_run = True
            self._logger.info("Found a valid CoAP + STOMP MTP Association")
        elif self._mtp_bitmap == 4:
            self._logger.error("Only the WebSocket MTP was configured")
        elif self._mtp_bitmap == 5:
            should_run = True
            self._logger.info("Found a valid CoAP + WebSocket MTP Association")
        elif self._mtp_bitmap == 6:
            # NOTE: WebSocket Controller to STOMP Agent won't work :: No STOMP Broker available
            should_run = True
            self._logger.info("Found a valid STOMP + WebSocket MTP Association")
        elif self._mtp_bitmap == 7:
            self._logger.error("All 3 MTPs configured")
        else:
            self._logger.error("Unknown MTP Association Configuration")

        return should_run

    def _read_coap_send_stomp(self):
        """Read from the CoAP MTP, and Send to the STOMP MTP"""
        queue_item = self._coap_mtp.get_msg()
        if queue_item is not None:
            payload = queue_item.get_payload()
            coap_resource_path = queue_item.get_coap_resource_path()

            if coap_resource_path in self._coap_resp_resource_dict:
                to_addr = self._coap_resp_resource_dict[coap_resource_path]
            else:
                to_addr = self._stomp_endpoint_addr

            self._logger.info("Found a payload on the CoAP MTP (on resource path: [%s])", coap_resource_path)
            self._logger.info("Sending it to the STOMP MTP (to destination: [%s], with reply-to-dest: [%s])",
                              to_addr, self._stomp_proxy_addr)
            self._stomp_mtp.send_msg(payload, to_addr, self._stomp_proxy_addr)

    def _read_stomp_send_coap(self):
        """Read from the STOMP MTP, and Send to the CoAP MTP"""
        queue_item = self._stomp_mtp.get_msg()
        if queue_item is not None:
            payload = queue_item.get_payload()
            stomp_reply_to_addr = queue_item.get_reply_to_addr()
            coap_resp_resource = stomp_reply_to_addr.replace("#", ".")

            if coap_resp_resource in self._coap_resp_resource_dict:
                coap_reply_to_addr = self._coap_mtp.get_addr(coap_resp_resource)
            else:
                self._coap_resp_resource_dict[coap_resp_resource] = stomp_reply_to_addr
                self._coap_mtp.add_resource(coap_resp_resource)
                coap_reply_to_addr = self._coap_mtp.get_addr(coap_resp_resource)

            to_addr = self._coap_endpoint_addr
            self._logger.info("Found a payload on the STOMP MTP (with reply-to-dest: [%s])", stomp_reply_to_addr)
            self._logger.info("Sending it to the CoAP MTP (to URL: [%s], with reply-to: [%s])",
                              to_addr, coap_reply_to_addr)
            self._coap_mtp.send_msg(payload, to_addr, coap_reply_to_addr)

    def _read_coap_send_websocket(self):
        """Read from the CoAP MTP, and Send to the WebSocket MTP"""
        queue_item = self._coap_mtp.get_msg()
        if queue_item is not None:
            payload = queue_item.get_payload()
            coap_resource_path = queue_item.get_coap_resource_path()

            self._logger.info("Found a payload on the CoAP MTP (on resource path: [%s])", coap_resource_path)
            self._logger.info("Sending it to the WebSocket MTP")
            self._websocket_mtp.send_msg(payload, to_addr="", reply_to_addr="")

    def _read_websocket_send_coap(self):
        """Read from the WebSocket MTP, and Send to the CoAP MTP"""
        queue_item = self._websocket_mtp.get_msg()
        if queue_item is not None:
            payload = queue_item.get_payload()
            coap_resp_resource = self._websocket_name.replace("#", ".")

            if coap_resp_resource in self._coap_resp_resource_dict:
                coap_reply_to_addr = self._coap_mtp.get_addr(coap_resp_resource)
            else:
                self._coap_resp_resource_dict[coap_resp_resource] = self._websocket_name
                self._coap_mtp.add_resource(coap_resp_resource)
                coap_reply_to_addr = self._coap_mtp.get_addr(coap_resp_resource)

            to_addr = self._coap_endpoint_addr
            self._logger.info("Found a payload on the WebSocket MTP")
            self._logger.info("Sending it to the CoAP MTP (to URL: [%s], with reply-to: [%s])",
                              to_addr, coap_reply_to_addr)
            self._coap_mtp.send_msg(payload, to_addr, coap_reply_to_addr)

    def _read_websocket_send_stomp(self):
        """Read from the WebSocket MTP, and Send to the STOMP MTP"""
        queue_item = self._websocket_mtp.get_msg()
        if queue_item is not None:
            payload = queue_item.get_payload()

            if self._last_stomp_reply_to_addr is not None:
                to_addr = self._last_stomp_reply_to_addr
                self._logger.debug("'last_stomp_reply_to_addr' found, using 'to_addr' of [%s]", to_addr)
                self._last_stomp_reply_to_addr = None
                self._logger.debug("Clearing out the 'last_stomp_reply_to_addr'")
            else:
                to_addr = self._stomp_endpoint_addr
                self._logger.debug("'last_stomp_reply_to_addr' not found, using 'to_addr' of [%s]", to_addr)

            self._logger.info("Found a payload on the WebSocket MTP")
            self._logger.info("Sending it to the STOMP MTP (to destination: [%s], with reply-to-dest: [%s])",
                              to_addr, self._stomp_proxy_addr)
            self._stomp_mtp.send_msg(payload, to_addr, self._stomp_proxy_addr)

    def _read_stomp_send_websocket(self):
        """Read from the STOMP MTP, and Send to the WebSocket MTP"""
        queue_item = self._stomp_mtp.get_msg()
        if queue_item is not None:
            payload = queue_item.get_payload()
            stomp_reply_to_addr = queue_item.get_reply_to_addr()
            self._last_stomp_reply_to_addr = stomp_reply_to_addr
            self._logger.debug("Setting the 'last_stomp_reply_to_addr' to [%s]", self._last_stomp_reply_to_addr)

            self._logger.info("Found a payload on the STOMP MTP (with reply-to-dest: [%s])", stomp_reply_to_addr)
            self._logger.info("Sending it to the WebSocket MTP")
            self._websocket_mtp.send_msg(payload, to_addr="", reply_to_addr="")


def main():
    """Main Processing for the MTP Proxy"""
    my_proxy = Proxy("cfg/proxy.json", "logs/proxy.log", log_level=logging.INFO, fail_bad_content_type=False)
    my_proxy.process_config_file()
    my_proxy.start_threads()

    # Hold main thread open by waiting for threads that never stop
    my_proxy.wait_for_threads()


if __name__ == "__main__":
    main()
