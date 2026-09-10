`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_math_operations_execution(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] var,
	input [4:0] var_1,
	output [4:0] var_2,
	output [4:0] var_3,
	output [4:0] var_4,
	output var_5,
	output var_6,
	output var_7,
	output var_8,
	output [4:0] var_9,
	output [4:0] var_10,
	output var_11,
	output var_12,
	output [4:0] var_13,
	output [4:0] var_14,
	input sys_clk,
	input sys_rst
);


// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign var_2 = (var + var_1);
assign var_3 = (var - var_1);
assign var_4 = (var * var_1);
assign var_5 = (var > var_1);
assign var_6 = (var < var_1);
assign var_7 = (var >= var_1);
assign var_8 = (var <= var_1);
assign var_9 = (~var);
assign var_10 = (var ^ var_1);
assign var_11 = (var == var_1);
assign var_12 = (var != var_1);
assign var_13 = (var & var_1);
assign var_14 = (var | var_1);

always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
	end
end

endmodule

