#!/usr/bin/env python3

from netfilterqueue import NetfilterQueue

from pypacker.layer3 import ip
from pypacker.layer567 import dns

TARGET_HOSTNAMES = set(['nonbast.com.'])

def handle_pkt(pkt):
    ip1 = ip.IP(pkt.get_payload())
    if dns.DNS in ip1:
        dns1 = ip1[dns.DNS]

        # this is a query that we would like to rewrite
        if (not dns1.answers
            and set(q.name_s for q in dns1.queries) & TARGET_HOSTNAMES
            and ip1.src[-1] > 240): # only redirect packets from the client net
            pkt.set_mark(1234)
            print("Marked packet originally destined for", ip1.dst_s)

    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, handle_pkt)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
