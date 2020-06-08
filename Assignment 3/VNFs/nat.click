 
// Declarations
//------------------------------------------------------------
// +++++ eth0 interface - Inbound and Outbound +++++
in	::  FromDevice($Name-eth0, METHOD LINUX);
out	::  Queue(200) -> ToDevice($Name-eth1);

// Network Function Logic
//------------------------------------------------------------
//						ipv4		arp req			arp reply
//in -> cl :: Classifier(12/0800, 12/0806 20/0001, 12/0806 20/0002);

//aout :: ARPQuerier(10.5.5.5, 5a:77:b5:7b:85:61);

//cl[2] -> [1]aout; //arp reply goes to the map
//aout[0] -> out;
//cl[1] -> 
// out;
//cl[0] ->
//  Strip(14) ->
//  CheckIPHeader ->
//  IPPrint("in") ->
//  rw1 :: IPAddrRewriter(pattern 10.5.5.5 - 0 1);
//rw1[0] ->
// SetIPAddress(10.5.5.1) ->
//  IPPrint("out0") ->
//  EtherEncap(0x0800, 5a:77:b5:7b:85:61, 00:00:00:00:00:07) ->
//  aout;
//rw1[1] ->
//  SetIPAddress(10.5.5.1) ->
//  IPPrint("out1") ->
//  EtherEncap(0x0800, 5a:77:b5:7b:85:61, 00:00:00:00:00:07) ->
//  aout;
  
  in -> out;   
