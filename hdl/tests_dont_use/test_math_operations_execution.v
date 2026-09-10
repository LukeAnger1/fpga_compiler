`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_math_operations_execution(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input [4:0] compiled_name,
	input [4:0] compiled_name_1,
	output reg [4:0] compiled_name_2,
	output reg [4:0] compiled_name_3,
	output reg [4:0] compiled_name_4,
	output reg compiled_name_5,
	output reg compiled_name_6,
	output reg compiled_name_7,
	output reg compiled_name_8,
	output reg [4:0] compiled_name_9,
	output reg [4:0] compiled_name_10,
	output reg compiled_name_11,
	output reg compiled_name_12,
	output reg [4:0] compiled_name_13,
	output reg [4:0] compiled_name_14,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	compiled_name_2 <= (compiled_name + compiled_name_1);
	compiled_name_3 <= (compiled_name - compiled_name_1);
	compiled_name_4 <= (compiled_name * compiled_name_1);
	compiled_name_5 <= (compiled_name > compiled_name_1);
	compiled_name_6 <= (compiled_name < compiled_name_1);
	compiled_name_7 <= (compiled_name >= compiled_name_1);
	compiled_name_8 <= (compiled_name <= compiled_name_1);
	compiled_name_9 <= (~compiled_name);
	compiled_name_10 <= (compiled_name ^ compiled_name_1);
	compiled_name_11 <= (compiled_name == compiled_name_1);
	compiled_name_12 <= (compiled_name != compiled_name_1);
	compiled_name_13 <= (compiled_name & compiled_name_1);
	compiled_name_14 <= (compiled_name | compiled_name_1);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		compiled_name_2 <= 5'd0;
		compiled_name_3 <= 5'd0;
		compiled_name_4 <= 5'd0;
		compiled_name_5 <= 1'd0;
		compiled_name_6 <= 1'd0;
		compiled_name_7 <= 1'd0;
		compiled_name_8 <= 1'd0;
		compiled_name_9 <= 5'd0;
		compiled_name_10 <= 5'd0;
		compiled_name_11 <= 1'd0;
		compiled_name_12 <= 1'd0;
		compiled_name_13 <= 5'd0;
		compiled_name_14 <= 5'd0;
	end
end

endmodule

