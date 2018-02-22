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
# File Name: utils.py
#
# Description: Defines utility classes for generic use.
#
# Contained Classes:
#  - GenericReceivingQueue(object)
#    - Used by MTP Bindings that listen for incoming messages
#  - ExpiringQueueItem(object)
#    - Used by the GenericReceivingQueue
#  - IPAddr(object)
#    - Used by the Proxy to retrieve the local IP Address for the CoAP MTP
#
"""


import time
import logging
import subprocess
import collections


class GenericReceivingQueue(object):
    """A Generic Receiving Queue to be used as a holding place before re-sending the message"""
    def __init__(self, sleep_time_interval=1):
        """Initialize the Generic Receiving Queue"""
        self._incoming_queue = collections.deque()
        self._sleep_time_interval = sleep_time_interval
        self._logger = logging.getLogger(self.__class__.__name__)

    def push(self, queue_item):
        """Push the provided Queue Item onto the end of the incoming message queue"""
        self._logger.debug("Pushing a Queue Item onto the end of the incoming message queue")
        self._incoming_queue.append(queue_item)

    def pop(self):
        """Pop the next Queue Item off of the front of the incoming message queue"""
        non_expired_queue_item = None

        if len(self._incoming_queue) > 0:
            queue_item = self._incoming_queue.popleft()
            if queue_item.is_expired():
                self._logger.info("Popped an expired payload, try again!")
            else:
                non_expired_queue_item = queue_item
                self._logger.debug("Popped the next payload from the front of the incoming message queue")

        return non_expired_queue_item

    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve the next incoming Queue Item from the Queue"""
        sleep_time = 0
        queue_item = None

        if timeout_in_seconds > 0:
            while queue_item is None and sleep_time < timeout_in_seconds:
                time.sleep(self._sleep_time_interval)
                sleep_time += self._sleep_time_interval
                queue_item = self.pop()
        else:
            queue_item = self.pop()

        return queue_item


class ExpiringQueueItem(object):
    """A Queue Item that has a TTL and a Payload"""
    def __init__(self, payload, reply_to_addr="", ttl=60):
        """Initialize the ExpiringQueueItem with the payload and a TTL (default of 60 seconds)"""
        self._ttl = ttl
        self._payload = payload
        self._is_coap_msg = False
        self._coap_resource_path = None
        self._create_time = time.time()
        self._reply_to_addr = reply_to_addr
        self._logger = logging.getLogger(self.__class__.__name__)

    def is_expired(self):
        """Return true if the Queue Item is older than its TTL"""
        if (self._create_time + self._ttl) < time.time():
            self._logger.info("Expiring a Queue Item")
            return True

        return False

    def is_coap_msg(self):
        """Retrieve whether or not this Queue Item is from a CoAP MTP"""
        return self._is_coap_msg

    def get_payload(self):
        """Retrieve the Payload"""
        return self._payload

    def get_reply_to_addr(self):
        """Retrieve the Reply-To-Address"""
        return self._reply_to_addr

    def get_coap_resource_path(self):
        """Retreive the CoAP Resource Path"""
        return self._coap_resource_path

    def set_coap_details(self, resource_path):
        """Set the CoAP Resource Path"""
        self._is_coap_msg = True
        self._coap_resource_path = resource_path


class IPAddr:
    """IP Address Retrieval Tool"""
    @staticmethod
    def get_ip_addr(intf=None):
        """Retrieve the IP Address after determining the underlying OS"""
        arg = "uname -a"
        proc = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        data = proc.communicate()
        uname_out = data[0].decode("utf-8")

        if uname_out.startswith("Darwin"):
            if intf is None:
                ip_addr = IPAddr._get_mac_ip_address()
            else:
                ip_addr = IPAddr._get_mac_ip_address(intf)
        else:
            if intf is None:
                ip_addr = IPAddr._get_rpi_ip_address()
            else:
                ip_addr = IPAddr._get_rpi_ip_address(intf)

        return ip_addr

    @staticmethod
    def _get_rpi_ip_address(netdev='eth0'):
        """Retrieve the IP Address on Raspberry Pi"""
        cmd = 'ip addr show ' + netdev
        return IPAddr._get_ipv4_address(cmd)

    @staticmethod
    def _get_mac_ip_address(netdev='en0'):
        """Retrieve the IP Address on Mac OS X"""
        cmd = 'ifconfig ' + netdev
        return IPAddr._get_ipv4_address(cmd)

    @staticmethod
    def _get_ipv4_address(command):
        """Retrieve the first IPv4 Address based on the provided RPi/MacOS command"""
        ipaddr = None
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        data = proc.communicate()
        sdata = data[0].decode("utf-8").split('\n')
        for line in sdata:
            if line.strip().startswith("inet "):
                # Retrieve an IPv4 address (ignore IPv6 addresses)
                ipaddr = line.strip().split(' ')[1].split('/')[0]
        return ipaddr
