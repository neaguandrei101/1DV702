from pox.core import core
from forwarding.l2_learning import LearningSwitch
from lib.util import dpid_to_str
from pox.lib.packet import *
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr, EthAddr
import pox.openflow.libopenflow_01 as of
from cgi import log
from mininet.util import dumpNetConnections, numCores

log = core.getLogger()

class ControllerApp(object):
    
        def __init__(self):
                print "Controlapp started"
                core.openflow.addListeners(self)
                #You may want to store each event.connection in an array
                self.connections=[]
                #maps the ip of a host to its gateway
                self.ip2gateway = {"172.20.1.1" : "172.20.1.2",
                                   "10.4.4.1" : "10.4.4.2",
                                   "10.5.5.1" : "10.5.5.2",
                                    }
                
        def _handle_ConnectionUp(self, event):      
                data_path_id = dpid_to_str(event.dpid)
                self.connections.append(event.connection)
                if data_path_id == "00-00-00-00-00-02":
                    self._flow_from_port_to_port(event=event, from_port=1, to_port=4, dst="10.4.4.1")
                    self._flow_from_port_to_port(event=event, from_port=4, to_port=5, dst="10.4.4.1")
                    self._flow_from_port_to_port(event=event, from_port=5, to_port=3, dst="10.4.4.1")
                    self._flow_from_port_to_port(event=event, from_port=3, to_port=2, dst="10.4.4.1")
                    self._flow_from_port_to_port(event=event, from_port=2, to_port=4, dst="172.20.1.1")
                    self._flow_from_port_to_port(event=event, from_port=5, to_port=1, dst="172.20.1.1")

                if data_path_id == "00-00-00-00-00-01" or data_path_id == "00-00-00-00-00-03":
                    self._flow_from_port_to_port(event=event, from_port=1, to_port=2, dst="10.4.4.1")
                    self._flow_from_port_to_port(event=event, from_port=2, to_port=1, dst="172.20.1.1")
                    
                #the DPID in string form is dash separated like "00-00-00-00-00-00"
                log.debug("Handling the connection up event for DPID : %s" % data_path_id)
        
        def _flow_from_port_to_port(self,event, from_port, to_port, dst):
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match(in_port = from_port, dl_type = 0x800, nw_dst = IPAddr(dst))
                msg.actions.append(of.ofp_action_output(port = to_port))
                event.connection.send(msg)
            
        def _flow_from_port_to_port_reactive(self,event, from_port, to_port, dst):
            if event.port == from_port and event.parsed.find('ipv4').dstip == dst:
                msg = of.ofp_packet_out()
                msg.data = event.parsed
                msg.actions.append(of.ofp_action_output(port = to_port)) #Port towards the host
                event.connection.send(msg)      
                
        #put the gateway ip as the source IP of the reply        
        def _replyArp(self, packet, gateway, event):        
                #log.debug("ARP: %s" % packet.payload)
                arp_reply = arp()
                arp_reply.hwsrc = EthAddr("77:77:77:77:77:77")#Bullshit MAC, irrelevant
                arp_reply.hwdst = packet.src
                arp_reply.opcode = arp.REPLY
                arp_reply.protosrc = IPAddr(gateway) #Gateway of host  that sends the request
                arp_reply.protodst = packet.payload.protosrc
                ether = ethernet()
                ether.type = ethernet.ARP_TYPE
                ether.dst = packet.src
                ether.src = EthAddr("77:77:77:77:77:77")
                ether.payload = arp_reply
                msg = of.ofp_packet_out()
                msg.data = ether.pack()
                msg.actions.append(of.ofp_action_output(port = event.port)) #Port towards the host
                event.connection.send(msg)
                #log.debug("Packet sent    %s" % msg.data)
                #og.debug("ARP: %s" % ether.payload)
                                            
        def _handle_PacketIn (self, event):
                from __builtin__ import str
                data_path_id = dpid_to_str(event.dpid)
                packet = event.parsed
                #log.debug("Packet payload  %s" % packet.payload)
                arphdr = packet.find('arp')
                if arphdr is not None:
                    if packet.payload.opcode == arp.REQUEST:
                        self._replyArp(packet, self.ip2gateway[str(arphdr.protosrc)], event)
                    pass
                else:
                    iphdr = packet.find('ipv4')
                    if iphdr is not None:
                        #Handle IPv4 here
                        log.debug("DPID: %s IN_PORT %i IPV4 %s -> %s " % (data_path_id, event.port, iphdr.srcip, iphdr.dstip) )
    
                        if data_path_id == "00-00-00-00-00-01" :
                            self._flow_from_port_to_port_reactive(event=event, from_port=1, to_port=3, dst="10.5.5.1")
                            self._flow_from_port_to_port_reactive(event=event, from_port=3, to_port=1, dst="172.20.1.1")
    
                        if data_path_id == "00-00-00-00-00-03":
                            self._flow_from_port_to_port_reactive(event=event, from_port=4, to_port=3, dst="10.5.5.1")
                            self._flow_from_port_to_port_reactive(event=event, from_port=3, to_port=4, dst="172.20.1.1")
    
                        if data_path_id == "00-00-00-00-00-04":  
                            self._flow_from_port_to_port_reactive(event=event, from_port=4, to_port=6, dst="10.5.5.1")
                            self._flow_from_port_to_port_reactive(event=event, from_port=7, to_port=5, dst="10.5.5.1")
                            self._flow_from_port_to_port_reactive(event=event, from_port=5, to_port=3, dst="10.5.5.1")
                            self._flow_from_port_to_port_reactive(event=event, from_port=3, to_port=6, dst="172.20.1.1")
                            self._flow_from_port_to_port_reactive(event=event, from_port=7, to_port=4, dst="172.20.1.1")
    
                        #iphdr.srcip
                        #iphdr.dstip
                        pass   
            
def launch():
        core.registerNew(ControllerApp) 
