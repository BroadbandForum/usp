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
#
"""


import time
import logging
import collections


class GenericReceivingQueue(object):
    """A Generic Receiving Queue to be used as a holding place before re-sending the message"""
    def __init__(self, sleep_time_interval=1):
        """Initialize the Generic Receiving Queue"""
        self._incoming_queue = collections.deque()
        self._sleep_time_interval = sleep_time_interval
        self._logger = logging.getLogger(self.__class__.__name__)

    def push(self, payload):
        """Push the provided message payload onto the end of the incoming message queue"""
        self._logger.debug("Pushing a payload onto the end of the incoming message queue")
        self._incoming_queue.append(ExpiringQueueItem(payload))

    def pop(self):
        """Pop the next payload off of the front of the incoming message queue"""
        payload = None

        if len(self._incoming_queue) > 0:
            queue_item = self._incoming_queue.popleft()
            if not queue_item.is_expired():
                payload = queue_item.get_payload()
                self._logger.debug("Popped the next payload from the front of the incoming message queue")
            else:
                self._logger.info("Popped an expired payload, try again!")

        return payload

    def get_msg(self, timeout_in_seconds=-1):
        """Retrieve the next incoming message from the Queue"""
        payload = None
        sleep_time = 0

        if timeout_in_seconds > 0:
            while payload is None and sleep_time < timeout_in_seconds:
                time.sleep(self._sleep_time_interval)
                sleep_time += self._sleep_time_interval
                payload = self.pop()
        else:
            payload = self.pop()

        return payload


class ExpiringQueueItem(object):
    """A Queue Item that has a TTL and a Payload"""
    def __init__(self, payload, ttl=60):
        """Initialize the ExpiringQueueItem with the payload and a TTL (default of 60 seconds)"""
        self._ttl = ttl
        self._payload = payload
        self._create_time = time.time()
        self._logger = logging.getLogger(self.__class__.__name__)

    def is_expired(self):
        """Return true if the Queue Item is older than its TTL"""
        if (self._create_time + self._ttl) < time.time():
            self._logger.info("Expiring a Queue Item")
            return True

        return False

    def get_payload(self):
        """Retrieve the Payload"""
        return self._payload
