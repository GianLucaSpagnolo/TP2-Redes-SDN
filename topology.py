from mininet.link import TCLink
from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(
        self,
        ammount_switches,
        ip1="10.0.0.1",
        ip2="10.0.0.2",
        ip3="10.0.0.3",
        ip4="10.0.0.4",
    ):
        if ammount_switches < 1:
            print("se necesita como minimo un switch")
            return

        Topo.__init__(self)
        h1 = self.addHost("h1", ip=ip1)
        h2 = self.addHost("h2", ip=ip2)
        h3 = self.addHost("h3", ip=ip3)
        h4 = self.addHost("h4", ip=ip4)

        switch = self.addSwitch("s1")
        self.addLink(switch, h1)
        self.addLink(switch, h2)

        prev_switch = switch
        for i in range(2, ammount_switches + 1):
            next_switch = self.addSwitch(f"s{i}")
            self.addLink(prev_switch, next_switch)
            prev_switch = next_switch

        self.addLink(prev_switch, h3)
        self.addLink(prev_switch, h4)


topos = {"mytopo": MyTopo}
