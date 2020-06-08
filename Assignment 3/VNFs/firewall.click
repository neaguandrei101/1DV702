 

// Declarations
//------------------------------------------------------------
// +++++ eth0 interface - Inbound and Outbound +++++
E0_IN	::  FromDevice($Name-eth0, METHOD LINUX);
E0_OUT	::  Queue(200) -> ToDevice($Name-eth1);

// Network Function Logic
//------------------------------------------------------------
//						ipv4	tcp	  dst 10.4.4.1 port5000
blockTcp :: Classifier(12/0800 23/06 30/0A040401 36/1388, -)

E0_IN -> blockTcp;
blockTcp[0] -> Print("Dropped an IPV4 packet DST SRV1 with the TCP port 5000") -> Discard();
blockTcp[1] -> E0_OUT;
