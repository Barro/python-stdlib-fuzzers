#!/usr/bin/env python3

import afl
import ipaddress
import os
import sys


def fuzz():
    with open(sys.argv[1], errors="surrogateescape") as fp:
        data = fp.read()

    try:
        address = ipaddress.ip_address(data)
    except ValueError:
        address = None

    try:
        network = ipaddress.ip_network(data)
    except ValueError:
        network = None

    try:
        interface = ipaddress.ip_interface(data)
    except ValueError:
        interface = None

    if address is not None:
        address.version
        address.max_prefixlen
        address.compressed
        address.exploded
        address.packed
        address.reverse_pointer
        address.is_multicast
        address.is_private
        address.is_global
        address.is_unspecified
        address.is_loopback
        address.is_link_local

        if isinstance(address, ipaddress.IPv6Address):
            address.is_site_local
            address.ipv4_mapped
            address.sixtofour
            address.teredo
        str(address)

    if network is not None:
        network.version
        network.max_prefixlen
        network.is_multicast
        network.is_private
        network.is_unspecified
        network.is_reserved
        network.is_loopback
        network.is_link_local
        network.network_address
        network.broadcast_address
        network.hostmask
        network.netmask
        network.with_prefixlen
        network.compressed
        network.exploded
        network.with_netmask
        network.with_hostmask
        network.num_addresses
        network.prefixlen
        for _ in network.hosts():
            break
        network.overlaps(network)
        for _ in network.subnets():
            break
        network.supernet()

        if isinstance(address, ipaddress.IPv6Network):
            network.is_site_local

    if interface is not None:
        interface.ip
        interface.network
        interface.with_prefixlen
        interface.with_netmask
        interface.with_hostmask


# @functools.lru_cache usage makes ipaddress module unstable
afl.init()
fuzz()
os._exit(0)
