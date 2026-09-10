`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_sign_operations(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input signed [4:0] a,
	input signed [4:0] b,
	input signed [4:0] c,
	input signed [4:0] d,
	output reg signed [4:0] a_1,
	output reg signed [4:0] a_2,
	output reg signed [4:0] a_3,
	output reg signed [4:0] a_4,
	output reg signed [4:0] a_5,
	output reg signed [4:0] a_6,
	output reg signed [4:0] b_1,
	output reg signed [4:0] b_2,
	output reg signed [4:0] b_3,
	output reg signed [4:0] c_1,
	output reg signed [4:0] c_2,
	output reg signed [4:0] c_3,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	a_1 <= (a + b);
	a_2 <= (a - b);
	a_3 <= (a * b);
	a_4 <= (a + c);
	a_5 <= (a - c);
	a_6 <= (a * c);
	b_1 <= (b + c);
	b_2 <= (b - c);
	b_3 <= (b * c);
	c_1 <= (c + d);
	c_2 <= (c - d);
	c_3 <= (c * d);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		a_1 <= 5'sd0;
		a_2 <= 5'sd0;
		a_3 <= 5'sd0;
		a_4 <= 5'sd0;
		a_5 <= 5'sd0;
		a_6 <= 5'sd0;
		b_1 <= 5'sd0;
		b_2 <= 5'sd0;
		b_3 <= 5'sd0;
		c_1 <= 5'sd0;
		c_2 <= 5'sd0;
		c_3 <= 5'sd0;
	end
end

endmodule

