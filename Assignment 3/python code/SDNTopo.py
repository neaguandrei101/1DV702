from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info, error
from mininet.node import Controller
def int2dpid( dpid ):
   try:
      dpid = hex( dpid )[ 2: ]
      dpid = '0' * ( 16 - len( dpid ) ) + dpid
      return dpid
   except IndexError:
      raise Exception( 'Unable to derive default datapath ID - '
                       'please either specify a dpid or use a '
               'canonical switch name such as s23.' )


class SDNTopo(Topo):
   def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches   
        cli = self.addHost('cli', ip='172.20.1.1/24', defaultRoute = "via 172.20.1.2")
        srv1 = self.addHost('srv1', ip='10.4.4.1/24', defaultRoute = "via 10.4.4.2")
        srv2 = self.addHost('srv2', ip='10.5.5.1/24', defaultRoute = "via 10.5.5.2")
        pp1 = self.addHost('pp1', ip='1.1.1.1/24', defaultRoute = "via 1.1.1.2")
        pp2 = self.addHost('pp2', ip='2.2.2.1/24', defaultRoute = "via 2.2.2.2")
        firewall = self.addHost('firewall', ip='3.3.3.1/24', defaultRoute = "via 3.3.3.2")
        nat = self.addHost("nat", ip='4.4.4.1/24')

        br1 = self.addSwitch('br1',dpid=int2dpid(1))
        br2 = self.addSwitch('br2',dpid=int2dpid(2))
        br3 = self.addSwitch('br3',dpid=int2dpid(3))
        br4 = self.addSwitch('br4',dpid=int2dpid(4))

        self.addLink(cli,br1,0,1)
        self.addLink(pp1,br2,0,3)
        self.addLink(br1,br2,2,1)
        self.addLink(br2,br3,2,1)
        self.addLink(firewall,br2,0,4)
        self.addLink(firewall,br2,1,5)
        self.addLink(br3,srv1,2,0)
        self.addLink(br1,br4,3,4)
        self.addLink(br4,br3,3,4)
        self.addLink(nat,br4,0,6)
        self.addLink(nat,br4,1,7)
        self.addLink(pp2,br4,0,5)
        self.addLink(br3,srv2,3,0)
                
topos = { 'sdntopo': ( lambda : SDNTopo() ) }



