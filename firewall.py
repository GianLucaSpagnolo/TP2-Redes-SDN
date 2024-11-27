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

# Add your imports here ...
log = core.getLogger ()

# Constants 

MAIN_SWITCH_ID = 1

IPv4_CONFIG = "v4"
IPv6_CONFIG = "v6"
UDP_PROTOCOL = "UDP"
TCP_PROTOCOL = "TCP"

IP_FIELD = "ip_version"
PORT_FIELD = "dst_port"
SRC_IP_FIELD = "src_ip"
DST_IP_FIELD = "dst_ip"
TRANSPORT_PROTOCOL_FIELD = "transport_protocol"

# Auxiliary functions

def read_ip_address(ip):
    """Read an IP address from the input string and return it as an IPAddr object.
        
        Args:
            ip (str): The IP address as a string.
        
        Returns:
            IPAddr: The IP address as an IPAddr object.
            
    """
    return IPAddr(ip)
def read_port(port):
    """Read a port number from the input string and return it as an integer.
        
    Args:
        port (str): The port number as a string.
    
    Returns:
        int: The port number as an integer.
        
    """
    return int(port)

def read_transport_protocol(protocol):
    """Read a transport protocol from the input string and return it as a constant.
        
    Args:
        protocol (str): The transport protocol as a string.
        
    Returns:
        int: The transport protocol as a constant.
        None: If the protocol is not recognized.
            
    """
    if protocol == UDP_PROTOCOL:
        return pkt.ipv4.UDP_PROTOCOL
    elif protocol == TCP_PROTOCOL:
        return pkt.ipv4.TCP_PROTOCOL
    return None

def read_ip_version(version):
    """Read an IP version from the input string and return it as a constant.
        
    Args:
        version (str): The IP version as a string.
        
    Returns:
        int: The IP version as a constant.
        None: If the version is not recognized.
            
    """
    if version == IPv4_CONFIG:
        return pkt.ethernet.IP_TYPE
    elif version == IPv6_CONFIG:
        return pkt.ethernet.IPV6_TYPE
    return None

def read_field(rule, field):
    """Read a field from the input rule and return it as the corresponding type.
        
    Args:
        rule (dict): The rule as a dictionary.
        field (str): The field name.
    
    Returns:
        object: The field value as the corresponding type.
        None: If the field is not recognized.
            
    """
    if field in rule:
        if field == IP_FIELD:
            return read_ip_version(rule[field])
        elif field == TRANSPORT_PROTOCOL_FIELD:
            return read_transport_protocol(rule[field])
        elif field == SRC_IP_FIELD or field == DST_IP_FIELD:
            return read_ip_address(rule[field])
        elif field == PORT_FIELD:
            return read_port(rule[field])
    return None

def genericRule (port=None, src_ip=None, dst_ip=None, transport_protocol=None, ip_protocol=IPv4_CONFIG):
    """Set a generic rule for a given port, source IP, destination IP, transport protocol and IP protocol.

    Args:
        port (_type_, optional): block the traffic from specific port . Defaults to None.
        src_ip (_type_, optional): block the traffic from specific host recongnized by the ip. Defaults to None.
        dst_ip (_type_, optional): block the traffic to specific host recongnized by the ip. Defaults to None.
        transport_protocol (_type_, optional): block the traffic with some transport protocol (UDP or TCP). Defaults to None.
        ip_protocol (_type_, optional): ip version recognized for the hosts. Defaults to IPv4_CONFIG.

    Returns:
        rule: The rule to block the traffic. Must be an ofp_flow_mod object and send it to the switch.
    """
    rule = of.ofp_flow_mod()
    rule.match.dl_type = ip_protocol
    rule.match.tp_dst = port
    rule.match.nw_src = src_ip
    rule.match.nw_dst = dst_ip
    rule.match.nw_proto = transport_protocol
    return rule

def read_config_file(filename):
    """Read the rules from a json file.

    Args:
        filename (String): path to the json file with rules as a list of dictionaries.
    
    Fields available:
        - dst_port: block the traffic from specific port.
        - src_ip: block the traffic from specific host recongnized by the ip.
        - dst_ip: block the traffic to specific host recongnized by the ip.
        - transport_protocol: block the traffic with some transport protocol (UDP or TCP).
        - ip_version: ip version recognized for the hosts.

    Returns:
        rules: A list of rules to block the traffic.
    """
    file = open(filename)
    config = json.load(file)
    file.close()
    return config["rules"]

# Add your global variables here ...
class Firewall (EventMixin):
    def __init__ (self):
        self.listenTo(core.openflow)
        self.setRules('config.json')
        log.debug("Enabling Firewall Module")
        
    def _handle_ConnectionUp (self , event):
        # Add your logic here ...
        log.info("Switch {} is connected with controller: ".format(event.dpid))
        if event.dpid == self.swith_id: 
            self.loadRules(event)
    
    def loadRules(self, event):
        for rule in self.rules:
            rule = genericRule(port=read_field(rule, PORT_FIELD), 
                               src_ip=read_field(rule, SRC_IP_FIELD), 
                               dst_ip=read_field(rule, DST_IP_FIELD), 
                               transport_protocol=read_field(rule, TRANSPORT_PROTOCOL_FIELD), 
                               ip_protocol=read_field(rule, IP_FIELD))
            event.connection.send(rule)
    
        log.info("Firewall rules installed on %s switch", dpidToStr(event.dpid))  

    def setRules (self, filename):
        # Identificador del switch donde se instalaran las reglas
        self.swith_id = MAIN_SWITCH_ID 
        # Lee las reglas de un json
        self.rules = read_config_file(filename)
        
        for rule, i in enumerate(self.rules):
            print("Rule {}: {}".format(rule, i))
    
def launch ():
    # Starting the Firewall module
    core.registerNew(Firewall)