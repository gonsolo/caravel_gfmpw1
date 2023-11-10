// Copyright 2023 Andreas Wendleder

`default_nettype none

`timescale 1 ns / 1 ps 
                          
module gonsolo_tb;    
	reg clock;
	reg power1;
	reg resetb;

	initial begin
		$dumpfile("gonsolo.vcd");
		$dumpvars(0, gonsolo_tb);
		$display("gonsolo: begin");
                repeat (10) begin
			repeat (1000) @(posedge clock);
                        $display("+1000 cycles");
                end
                $display ("gonsolo: timeout");
		$finish;
	end

	wire VDD5V;
	wire VSS;
	wire gpio;
	wire [37:0] mprj_io;
	wire flash_csb;
	wire flash_clk;
	wire flash_io0;
	wire flash_io1;

	assign VDD5V = power1;
	assign VSS = 1'b0;

	always #12.5 clock <= (clock === 1'b0);

        initial begin
		clock = 0;
        end

	initial begin
		resetb <= 1'b0;
                #2000;
                resetb <= 1'b1;
        end

	initial begin
                  power1 <= 1'b0;
                  #100;
                  power1 <= 1'b1;
        end

	caravel uut(
		.VDD(VDD5V),
		.VSS(VSS),
		.gpio(gpio),
		.mprj_io(mprj_io),
		.clock(clock),
		.resetb(resetb),
		.flash_csb(flash_csb),
		.flash_clk(flash_clk),
    		.flash_io0(flash_io0),
    		.flash_io1(flash_io1)
	);

endmodule
`default_nettype wire

