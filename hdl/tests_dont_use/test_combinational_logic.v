`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_combinational_logic(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] a,
	input [4:0] b,
	output [4:0] a_1,
	output [4:0] a_2,
	output [4:0] a_3,
	output [4:0] a_4,
	output [4:0] a_5,
	output [4:0] a_6,
	input sys_clk,
	input sys_rst
);


// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign a_1 = (a + b);
assign a_2 = (a - b);
assign a_3 = (a * b);
assign a_4 = (a_1 | a_2);
assign a_5 = (a_2 ^ a_3);
assign a_6 = (a_4 + a_5);

always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
	end
end

endmodule

