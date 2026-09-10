`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_math_operations_pipeline(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] var,
	input [4:0] var_1,
	output reg [4:0] var_2,
	output reg [4:0] var_3,
	output reg [4:0] var_4,
	output reg [4:0] var_5,
	output reg [4:0] var_6,
	output reg [4:0] var_7,
	output reg [4:0] var_8,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	var_2 <= (var + var_1);
	var_3 <= var_1;
	var_4 <= (var_2 + var_3);
	var_5 <= var_2;
	var_6 <= (var_5 + var_4);
	var_7 <= var_4;
	var_8 <= (var_6 + var_7);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		var_2 <= 5'd0;
		var_3 <= 5'd0;
		var_4 <= 5'd0;
		var_5 <= 5'd0;
		var_6 <= 5'd0;
		var_7 <= 5'd0;
		var_8 <= 5'd0;
	end
end

endmodule

