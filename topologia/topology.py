from mininet.link import TCLink
from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(self, ammount_switches):

        if ammount_switches < 1:
            print("se necesita como minimo un switch")
            return

        Topo.__init__(self)
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")

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
