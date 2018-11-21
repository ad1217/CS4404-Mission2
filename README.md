# DNS Modification and Redirection

This repository contains two simple scripts that modify DNS requests going through a router.
* `dns-modify.py` changes 

## Dependencies

`dns-modify.py` and `dns-redirect.py` both require [pypacker](https://gitlab.com/mike01/pypacker). and `dns-redirect.py` additionally requires [python-netfilterqueue](https://github.com/kti/python-netfilterqueue). Both also require Python 3.

## Usage
Both need some setup (below), but then can be run as `sudo python3 <scriptname.py>`.

### `dns-modify.py`
Redirect forwarded packets into a netfilter queue

example:
```
# put all forwarded packets (ie packets not from or to the router) from port 53 into netfilter queue 0
sudo iptables -t filter -A FORWARD -p udp --sport 53 -j NFQUEUE --queue-num 0
```

### `dns-redirect.py`
Redirect packets into a netfilter queue, then redirect packets with a mark to localhost

example:
```
# put all packets to port 53 from client network into netfilter queue 1
sudo iptables -t mangle -A PREROUTING -p udp --dport 53 -s 10.4.16.240/28 -j NFQUEUE --queue-num 1

# Redirect all packets with mark 1234 to localhost
sudo iptables -t nat -A PREROUTING -m mark --mark 1234 -j REDIRECT
```

Also requires a DNS server, such as dnsmasq, with the following example config:
```
# /etc/dnsmasq.conf
no-resolv
server=10.4.16.6
address=/nonbast.com/10.4.16.1
log-queries
```
