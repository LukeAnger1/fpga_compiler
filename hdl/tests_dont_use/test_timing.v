`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_timing(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input signed [4:0] a,
	input signed [4:0] b,
	output reg signed [4:0] a_1,
	output reg signed [4:0] b_1,
	output reg signed [4:0] b_2,
	output reg signed [4:0] b_3,
	output reg signed [4:0] b_4,
	output reg signed [4:0] a_2,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	a_1 <= (a + b);
	b_1 <= b;
	b_2 <= (b_1 + a_1);
	b_3 <= b;
	b_4 <= b_3;
	a_2 <= a_1;
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		a_1 <= 5'sd0;
		b_1 <= 5'sd0;
		b_2 <= 5'sd0;
		b_3 <= 5'sd0;
		b_4 <= 5'sd0;
		a_2 <= 5'sd0;
	end
end

endmodule

