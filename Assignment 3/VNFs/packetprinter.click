// Declarations
//------------------------------------------------------------
// +++++ eth0 interface - Inbound and Outbound +++++
E0_IN	::  FromDevice($Name-eth0, METHOD LINUX);
E0_OUT	::  Queue(200) -> ToDevice($Name-eth0);

// Network Function Logic
//------------------------------------------------------------
E0_IN -> Print(CONTENTS true, MAXLENGTH 1500) -> E0_OUT;

 
