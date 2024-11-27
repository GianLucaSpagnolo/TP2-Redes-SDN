# Coursera:
# - Software Defined Networking (SDN) course
# -- Programming Assignment: Layer -2 Firewall Application Professor: Nick Feamster
# Teaching Assistant: Arpit Gupta
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr
import pox.lib.packet as pkt
import json

IPv4_CONFIG = "ipv4"
UDP_PROTOCOL = "UDP"

def read_field(rule, field):
    if field in rule:
        return rule[field]
    return None

# Add your imports here ...
log = core.getLogger ()

# Add your global variables here ...
class Firewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
        self.setRules()
        log.debug("Enabling Firewall Module")
        
    def _handle_ConnectionUp (self , event):
        # Add your logic here ...
                
        for rule in self.rules:
            self.trafficRule(event, port=read_field(rule, "dst_port"), 
                                    src_ip=read_field(rule, "src_ip"), 
                                    dst_ip=read_field(rule, "dst_ip"), 
                                    transport_protocol=read_field(rule, "transport_protocol"), 
                                    ip_protocol=read_field(rule, "ip_version"))
   
        """
        host1 = "10.0.0.1"
        host2 = "10.0.0.2"
        host4 = "10.0.0.4"
    
        # Regla 1: Descartar mensajes con puerto destino 80
        self.trafficRule(event, port=80)

        # Regla 2: Descartar mensajes desde el host 1 al puerto 5001 usando UDP   
        self.trafficRule(event, src_ip=host1, port=5001, transport_protocol=pkt.ipv4.UDP_PROTOCOL)

        # Regla 3: Bloqueo de comunicacion entre 2 hosts cualquiera (bilateral).
        self.trafficRule(event, src_ip=host4, dest_ip=host2)
        self.trafficRule(event, src_ip=host2, dest_ip=host4)
        
        """
        
    def trafficRule (self, event, port=None, src_ip=None, dst_ip=None, transport_protocol=None, ip_protocol=IPv4_CONFIG):
        rule = of.ofp_flow_mod()
        rule.match.dl_type = pkt.ethernet.IP_TYPE if ip_protocol == IPv4_CONFIG else pkt.ethernet.IPV6_TYPE
        if port : rule.match.tp_dst = port
        if src_ip : rule.match.nw_src = IPAddr(src_ip)
        if dst_ip: rule.match.nw_dst = IPAddr(dst_ip)
        if transport_protocol: rule.match.nw_proto = pkt.ipv4.UDP_PROTOCOL if transport_protocol == UDP_PROTOCOL else pkt.ipv4.TCP_PROTOCOL
        event.connection.send(rule)
        
        log.info("Firewall rule added: %s on switch %s" % rule, dpidToStr(event.dpid))

    def setRules (self):
        # Lee las reglas de un json
        file = open('config.json')
        config = json.load(file)
        file.close()
        self.rules = config["rules"]
    
    def launch ():
        # Starting the Firewall module
        core.registerNew(Firewall)