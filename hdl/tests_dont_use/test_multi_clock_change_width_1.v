`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_multi_clock_change_width_1(
	input [4:0] a,
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] b,
	output reg [4:0] a_1,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	a_1 <= (a + b);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		a_1 <= 5'd0;
	end
end

endmodule

