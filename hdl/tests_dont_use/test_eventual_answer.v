`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_eventual_answer(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] a,
	input [4:0] b,
	output reg [4:0] a_1,
	output reg [4:0] a_2,
	output reg [4:0] a_3,
	output reg [4:0] a_4,
	output reg [4:0] a_5,
	output reg [4:0] a_6,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	a_1 <= (a + b);
	a_2 <= (a - b);
	a_3 <= (a * b);
	a_4 <= (a_1 | a_2);
	a_5 <= (a_2 ^ a_3);
	a_6 <= (a_4 + a_5);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		a_1 <= 5'd0;
		a_2 <= 5'd0;
		a_3 <= 5'd0;
		a_4 <= 5'd0;
		a_5 <= 5'd0;
		a_6 <= 5'd0;
	end
end

endmodule

