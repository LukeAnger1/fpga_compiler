`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_math_operations(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] var,
	input [4:0] var_1,
	output [4:0] var_2,
	output [4:0] var_3,
	output [4:0] var_4,
	output [4:0] var_5,
	output [4:0] var_6,
	output [4:0] var_7,
	output [4:0] var_8,
	input sys_clk,
	input sys_rst
);


// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign var_2 = (var + var_1);
assign var_3 = (var - var_1);
assign var_4 = (var_2 * var_3);
assign var_5 = (var_4 > var);
assign var_6 = (var < var_5);
assign var_7 = (var <= var_6);
assign var_8 = (var >= var_1);

always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
	end
end

endmodule

