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


class Proxy(object):
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
                    """
                      ProxyPort : CoAP Port that the MTP Proxy is listening on
                      ProxyResource : CoAP Resource associated with the MTP Proxy
                                       This is typically used by the Proxied USP Endpoint when sending Notifications
                      EndpointURL : CoAP URL for the USP Endpoint being proxied
                    """
                    self._logger.info("Found a CoAP MTP")
                    coap_dict = association_dict["Association"]["CoAP"]
                    proxy_addr = "coap://" + self._my_ip_addr + ":" + str(coap_dict["ProxyPort"]) + \
                                 "/" + coap_dict["ProxyResource"]
                    coap_mtp_inst = coap_mtp.CoapMtp(coap_dict["ProxyPort"], coap_dict["ProxyResource"],
                                                     proxy_addr, self._debug)
                    endpoint_addr = coap_dict["EndpointURL"]
                    proxy_thr.add_mtp(coap_mtp_inst, endpoint_addr)

                if "STOMP" in association_dict["Association"]:
                    """
                      Host : Hostname or IP Address of the STOMP Server
                      Port : Port of the STOMP Server
                      VirtualHost : Virtual Host to be used when connecting to the STOMP Server
                      Username : Username to be used when connecting to the STOMP Server
                                  Server will validate as part of credentials
                      Password : Password to be used when connecting to the STOMP Server
                                  Server will validate as part of credentials
                      ProxyDestination : STOMP Destination associated with the MTP Proxy
                                          This is typically used by the Proxied USP Endpoint when sending Notifications
                                          This can be overridden by the STOMP Server via the subscribe-dest header
                      EndpointDestination : STOMP Destination of the USP Endpoint being proxied
                      ProxyEndpointID : Endpoint ID of the USP Endpoint being proxied
                                         This is used in the endpoint-id header within the STOMP CONNECT Frame
                    """
                    self._logger.info("Found a STOMP MTP")
                    stomp_dict = association_dict["Association"]["STOMP"]
                    proxy_addr = stomp_dict["ProxyDestination"]
                    stomp_mtp_inst = stomp_mtp.StompMtp(stomp_dict["Host"], stomp_dict["Port"],
                                                        stomp_dict["Username"], stomp_dict["Password"],
                                                        stomp_dict["VirtualHost"], proxy_addr,
                                                        proxy_endpoint_id=stomp_dict["ProxyEndpointID"],
                                                        fail_bad_content_type=self._fail_bad_content_type)
                    endpoint_addr = stomp_dict["EndpointDestination"]
                    proxy_thr.add_mtp(stomp_mtp_inst, endpoint_addr)

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
        self._mtp1 = None
        self._endpoint_addr1 = None
#        self._last_mtp1_reply_to_addr = None
        self._mtp2 = None
        self._endpoint_addr2 = None
#        self._last_mtp2_reply_to_addr = None
        self._sleep_time_interval = sleep_time_interval
        self._logger = logging.getLogger(self.__class__.__name__)

    def add_mtp(self, mtp, endpoint_addr):
        """Add an MTP configuration to the Proxy Thread"""
        if self._mtp1 is None:
            self._mtp1 = mtp
            self._endpoint_addr1 = endpoint_addr
            self._logger.info("Adding MTP 1")
        elif self._mtp2 is None:
            self._mtp2 = mtp
            self._endpoint_addr2 = endpoint_addr
            self._logger.info("Adding MTP 2")
        else:
            self._logger.warning("Can't add another MTP; all MTPs are already configured")

    def run(self):
        """Start the thread"""
        self._mtp1.listen()
        self._mtp2.listen()

        while True:
            time.sleep(self._sleep_time_interval)
            queue_item = self._mtp1.get_msg()
            payload = queue_item.get_payload()
            if payload is not None:
                to_addr = self._endpoint_addr2
#                if self._last_mtp2_reply_to_addr is not None:
#                    to_addr = self._last_mtp2_reply_to_addr

#                self._last_mtp1_reply_to_addr = reply_to_addr
                self._logger.info("Found a payload on MTP 1; sending it to MTP 2 [%s]", to_addr)
                self._mtp2.send_msg(payload, to_addr)

            queue_item = self._mtp2.get_msg()
            payload = queue_item.get_payload()
            if payload is not None:
                to_addr = self._endpoint_addr1
#                if self._last_mtp1_reply_to_addr is not None:
#                    to_addr = self._last_mtp1_reply_to_addr

#                self._last_mtp2_reply_to_addr = reply_to_addr
                self._logger.info("Found a payload on MTP 2; sending it to MTP 1 [%s]", to_addr)
                self._mtp1.send_msg(payload, to_addr)


def main():
    """Main Processing for the MTP Proxy"""
    my_proxy = Proxy("cfg/proxy.json", "logs/proxy.log", log_level=logging.INFO, fail_bad_content_type=False)
    my_proxy.process_config_file()
    my_proxy.start_threads()

    # Hold main thread open by waiting for threads that never stop
    my_proxy.wait_for_threads()


if __name__ == "__main__":
    main()
