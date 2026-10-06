`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_multi_cycle_same_cycle(
	input [4:0] a,
	input [4:0] b,
	output reg [4:0] a_1,
	output reg [4:0] a_2,
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input sys_clk,
	input sys_rst
);

reg var0_stupid_only_needed_for_clk_dont_ever_use = 1'd0;
reg [4:0] var0_a1 = 5'd0;
reg [4:0] var2_b = 5'd0;
reg [4:0] var2_a0 = 5'd0;
reg [4:0] var2_a1 = 5'd0;
reg [4:0] var3_a0 = 5'd0;
reg [4:0] var3_a1 = 5'd0;


always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	var0_stupid_only_needed_for_clk_dont_ever_use <= var0_stupid_only_needed_for_clk_dont_ever_use;
	var0_a1 <= (a + b);
	var2_b <= b;
	var2_a0 <= (var0_a1 + var2_b);
	var2_a1 <= var0_a1;
	var3_a0 <= (var2_a1 + var2_a0);
	var3_a1 <= var2_a0;
	a_1 <= (var3_a0 + var3_a1);
	a_2 <= var3_a0;
	if (sys_rst) begin
		var0_stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		var0_a1 <= 5'd0;
		var2_b <= 5'd0;
		var2_a0 <= 5'd0;
		var2_a1 <= 5'd0;
		var3_a0 <= 5'd0;
		var3_a1 <= 5'd0;
		a_1 <= 5'd0;
		a_2 <= 5'd0;
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
	end
end

endmodule

