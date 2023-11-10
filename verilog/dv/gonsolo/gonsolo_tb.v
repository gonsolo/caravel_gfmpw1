// Copyright 2023 Andreas Wendleder

`default_nettype none

`timescale 1 ns / 1 ps 
                          
module gonsolo_tb;    
	reg clock;

	initial begin
		$dumpfile("gonsolo.vcd");
		$dumpvars(0, gonsolo_tb);
		$display("bla");
		$finish;
	end
endmodule
`default_nettype wire

