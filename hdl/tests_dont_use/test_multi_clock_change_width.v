`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_multi_clock_change_width(
	input [4:0] a,
	input [4:0] b,
	input [4:0] e,
	output reg [4:0] a_1,
	output reg [4:0] a_2,
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input sys_clk,
	input sys_rst
);

reg var0_stupid_only_needed_for_clk_dont_ever_use = 1'd0;
reg [4:0] var0_a1 = 5'd0;
wire [4:0] var2_a;
wire [4:0] var3_e0;
reg [4:0] var3_e1 = 5'd0;
wire [4:0] var3_e2;
reg [4:0] multiclockpipelinecompiler_a0 = 5'd0;
reg [1:0] multiclockpipelinecompiler_ring_2 = 2'd1;
wire [4:0] a_copy0;
reg stupid_only_needed_for_clk_dont_ever_use_copy0 = 1'd0;
wire [4:0] e_copy0;
wire [4:0] e_copy0_1;
reg [4:0] a_copy0_1 = 5'd0;
wire [4:0] a_copy1;
reg stupid_only_needed_for_clk_dont_ever_use_copy1 = 1'd0;
wire [4:0] e_copy1;
wire [4:0] e_copy1_1;
reg [4:0] a_copy1_1 = 5'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign a_copy0 = var2_a;
assign e_copy0 = e;
assign e_copy0_1 = var3_e2;
assign a_copy1 = var2_a;
assign e_copy1 = e;
assign e_copy1_1 = var3_e2;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	a_1 <= 5'd0;
	a_1 <= 1'd0;
	if (multiclockpipelinecompiler_ring_2[0]) begin
		a_1 <= a_copy0_1;
	end
	if (multiclockpipelinecompiler_ring_2[1]) begin
		a_1 <= a_copy1_1;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign var2_a = var0_a1;
assign var3_e0 = e;
assign var3_e2 = var3_e1;

always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	var0_stupid_only_needed_for_clk_dont_ever_use <= var0_stupid_only_needed_for_clk_dont_ever_use;
	var0_a1 <= (a + b);
	var3_e1 <= var3_e0;
	multiclockpipelinecompiler_a0 <= var0_a1;
	a_2 <= multiclockpipelinecompiler_a0;
	multiclockpipelinecompiler_ring_2 <= {multiclockpipelinecompiler_ring_2[0], multiclockpipelinecompiler_ring_2[1]};
	if (multiclockpipelinecompiler_ring_2[0]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy0 <= stupid_only_needed_for_clk_dont_ever_use_copy0;
		a_copy0_1 <= (a_copy0 + e_copy0_1);
	end
	if (multiclockpipelinecompiler_ring_2[1]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy1 <= stupid_only_needed_for_clk_dont_ever_use_copy1;
		a_copy1_1 <= (a_copy1 + e_copy1_1);
	end
	if (sys_rst) begin
		var0_stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		var0_a1 <= 5'd0;
		var3_e1 <= 5'd0;
		multiclockpipelinecompiler_a0 <= 5'd0;
		a_2 <= 5'd0;
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		multiclockpipelinecompiler_ring_2 <= 2'd1;
		stupid_only_needed_for_clk_dont_ever_use_copy0 <= 1'd0;
		a_copy0_1 <= 5'd0;
		stupid_only_needed_for_clk_dont_ever_use_copy1 <= 1'd0;
		a_copy1_1 <= 5'd0;
	end
end

endmodule

