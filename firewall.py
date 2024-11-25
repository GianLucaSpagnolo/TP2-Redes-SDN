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
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
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
        
        host1 = "10.0.0.1"
        host2 = "10.0.0.2"
        host3 = "10.0.0.3"
        host4 = "10.0.0.4"
        
        # Regla 1: Descartar mensajes con puerto destino 80
        self.trafficRule(event, port=80)

        # Regla 2: Descartar mensajes desde el host 1 al puerto 5001 usando UDP   
        self.trafficRule(event, src_ip=host1, port=5001, transport_protocol=pkt.ipv4.UDP_PROTOCOL)

        # Regla 3: Bloqueo de comunicacion entre 2 hosts cualquiera (bilateral).
        self.trafficRule(event, src_ip=host3, dest_ip=host2)
        self.trafficRule(event, src_ip=host2, dest_ip=host3)

    def trafficRule (self, event, port=None, src_ip=None, dst_ip=None, transport_protocol=None, ip_protocol=pkt.ethernet.IP_PROTOCOL):
        rule = of.ofp_flow_mod()
        rule.match.dl_type = ip_protocol
        if port : rule.match.tp_dst = port
        if src_ip : rule.match.nw_src = IPAddr(src_ip)
        if dst_ip: rule.match.nw_dst = IPAddr(dst_ip)
        if transport_protocol: rule.match.nw_proto = transport_protocol
        event.connection.send(rule)
        
        log.info("Firewall rule added: %s on switch %s" % rule, dpidToStr(event.dpid))

    def launch ():
        # Starting the Firewall module
        core.registerNew(Firewall)
        