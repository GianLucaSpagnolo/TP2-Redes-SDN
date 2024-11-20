# Coursera:
# - Software Defined Networking (SDN) course
# -- Programming Assignment: Layer -2 Firewall Application Professor: Nick Feamster
# Teaching Assistant: Arpit Gupta
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

# Add your imports here ...
log = core.getLogger ()

# Add your global variables here ...
class Firewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling␣Firewall␣Module")
    def _handle_ConnectionUp (self , event):
        # Add your logic here ...
        
        # Rule 1: Block traffic to destination port 80
        block_port_80 = of.ofp_match()
        block_port_80.tp_dst = 80
        block_port_80.dl_type = 0x0800  # IPv4 traffic
        block_port_80.nw_proto = 6  # TCP protocol
        msg = of.ofp_flow_mod()
        msg.priority = 100  # Set a high priority
        msg.match = block_port_80
        event.connection.send(msg)

        # Rule 2: Block traffic from Host 1 to any host on port 5001 (TCP protocol)
        block_host1_to_port_5001 = of.ofp_match()
        block_host1_to_port_5001.dl_type = 0x0800  # IPv4 traffic
        block_host1_to_port_5001.nw_proto = 6  # TCP protocol
        block_host1_to_port_5001.tp_dst = 5001
        block_host1_to_port_5001.nw_src = "10.0.0.1"  # Replace with Host 1 IP
        msg = of.ofp_flow_mod()
        msg.priority = 110
        msg.match = block_host1_to_port_5001
        event.connection.send(msg)

        # Rule 3: Block traffic between Host 1 and Host 2
        block_host1_to_host2 = of.ofp_match()
        block_host1_to_host2.dl_type = 0x0800  # IPv4 traffic
        block_host1_to_host2.nw_src = "10.0.0.1"  # Replace with Host 1 IP
        block_host1_to_host2.nw_dst = "10.0.0.2"  # Replace with Host 2 IP
        msg = of.ofp_flow_mod()
        msg.priority = 120
        msg.match = block_host1_to_host2
        event.connection.send(msg)

        # Block traffic from Host 2 to Host 1 (reverse direction)
        block_host2_to_host1 = of.ofp_match()
        block_host2_to_host1.dl_type = 0x0800  # IPv4 traffic
        block_host2_to_host1.nw_src = "10.0.0.2"  # Replace with Host 2 IP
        block_host2_to_host1.nw_dst = "10.0.0.1"  # Replace with Host 1 IP
        msg = of.ofp_flow_mod()
        msg.priority = 120
        msg.match = block_host2_to_host1
        event.connection.send(msg)
            
    def launch ():
        # Starting the Firewall module
        core.registerNew(Firewall)
        