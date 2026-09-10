`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_math_operations_execution(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] var,
	input [4:0] var_1,
	output reg [4:0] var_2,
	output reg [4:0] var_3,
	output reg [4:0] var_4,
	output reg var_5,
	output reg var_6,
	output reg var_7,
	output reg var_8,
	output reg [4:0] var_9,
	output reg [4:0] var_10,
	output reg var_11,
	output reg var_12,
	output reg [4:0] var_13,
	output reg [4:0] var_14,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	var_2 <= (var + var_1);
	var_3 <= (var - var_1);
	var_4 <= (var * var_1);
	var_5 <= (var > var_1);
	var_6 <= (var < var_1);
	var_7 <= (var >= var_1);
	var_8 <= (var <= var_1);
	var_9 <= (~var);
	var_10 <= (var ^ var_1);
	var_11 <= (var == var_1);
	var_12 <= (var != var_1);
	var_13 <= (var & var_1);
	var_14 <= (var | var_1);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		var_2 <= 5'd0;
		var_3 <= 5'd0;
		var_4 <= 5'd0;
		var_5 <= 1'd0;
		var_6 <= 1'd0;
		var_7 <= 1'd0;
		var_8 <= 1'd0;
		var_9 <= 5'd0;
		var_10 <= 5'd0;
		var_11 <= 1'd0;
		var_12 <= 1'd0;
		var_13 <= 5'd0;
		var_14 <= 5'd0;
	end
end

endmodule

