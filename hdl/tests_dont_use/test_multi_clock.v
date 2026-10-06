`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_multi_clock(
	input [7:0] a,
	input [7:0] b,
	input [7:0] e,
	output reg [7:0] e_1,
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input sys_clk,
	input sys_rst
);

reg var0_stupid_only_needed_for_clk_dont_ever_use = 1'd0;
reg [7:0] var0_a1 = 8'd0;
wire [7:0] var3_a;
wire [7:0] var2_e1;
reg [7:0] var2_e2 = 8'd0;
wire [7:0] var2_e3;
wire [7:0] var4_var2_a0;
reg [7:0] var4_var2_a1 = 8'd0;
wire [7:0] var4_var2_a2;
wire [7:0] var4_var4_a0;
reg [7:0] var4_var4_a1 = 8'd0;
wire [7:0] var4_var4_a2;
reg [7:0] var4_e;
wire [7:0] var5_e;
reg [7:0] var6_e;
wire [7:0] var7_e;
reg [7:0] var8_var0_a = 8'd0;
reg [7:0] var8_var7_a = 8'd0;
reg [7:0] var8_var8_a = 8'd0;
reg [7:0] var8_var9_a = 8'd0;
reg [7:0] var8_var10_a = 8'd0;
reg [7:0] var8_var11_a = 8'd0;
reg [7:0] var8_var12_a = 8'd0;
reg [7:0] var8_var13_a = 8'd0;
reg [7:0] var8_var14_a = 8'd0;
reg [1:0] multiclockpipelinecompiler_ring_2 = 2'd1;
wire [7:0] a_copy0;
reg [7:0] e_copy0 = 8'd0;
wire [7:0] e_copy0_1;
reg stupid_only_needed_for_clk_dont_ever_use_copy0 = 1'd0;
wire [7:0] a_copy0_1;
wire [7:0] e_copy0_2;
reg [7:0] e_copy0_3 = 8'd0;
wire [7:0] a_copy0_2;
wire [7:0] a_copy1;
reg [7:0] e_copy1 = 8'd0;
wire [7:0] e_copy1_1;
reg stupid_only_needed_for_clk_dont_ever_use_copy1 = 1'd0;
wire [7:0] a_copy1_1;
wire [7:0] e_copy1_2;
reg [7:0] e_copy1_3 = 8'd0;
wire [7:0] a_copy1_2;
reg [3:0] multiclockpipelinecompiler_ring_4 = 4'd1;
wire [7:0] e_copy0_4;
reg stupid_only_needed_for_clk_dont_ever_use_copy0_1 = 1'd0;
reg [7:0] e_copy0_5 = 8'd0;
wire [7:0] e_copy1_4;
reg stupid_only_needed_for_clk_dont_ever_use_copy1_1 = 1'd0;
reg [7:0] e_copy1_5 = 8'd0;
wire [7:0] e_copy2;
reg stupid_only_needed_for_clk_dont_ever_use_copy2 = 1'd0;
reg [7:0] e_copy2_1 = 8'd0;
wire [7:0] e_copy3;
reg stupid_only_needed_for_clk_dont_ever_use_copy3 = 1'd0;
reg [7:0] e_copy3_1 = 8'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign a_copy0 = var4_var4_a2;
assign e_copy0_1 = e;
assign a_copy0_1 = var3_a;
assign e_copy0_2 = var2_e3;
assign a_copy0_2 = var4_var2_a2;
assign a_copy1 = var4_var4_a2;
assign e_copy1_1 = e;
assign a_copy1_1 = var3_a;
assign e_copy1_2 = var2_e3;
assign a_copy1_2 = var4_var2_a2;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	var4_e <= 8'd0;
	var4_e <= 1'd0;
	if (multiclockpipelinecompiler_ring_2[0]) begin
		var4_e <= e_copy0;
	end
	if (multiclockpipelinecompiler_ring_2[1]) begin
		var4_e <= e_copy1;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign e_copy0_4 = var5_e;
assign e_copy1_4 = var5_e;
assign e_copy2 = var5_e;
assign e_copy3 = var5_e;

// synthesis translate_off
reg dummy_d_1;
// synthesis translate_on
always @(*) begin
	var6_e <= 8'd0;
	var6_e <= 1'd0;
	if (multiclockpipelinecompiler_ring_4[0]) begin
		var6_e <= e_copy0_5;
	end
	if (multiclockpipelinecompiler_ring_4[1]) begin
		var6_e <= e_copy1_5;
	end
	if (multiclockpipelinecompiler_ring_4[2]) begin
		var6_e <= e_copy2_1;
	end
	if (multiclockpipelinecompiler_ring_4[3]) begin
		var6_e <= e_copy3_1;
	end
// synthesis translate_off
	dummy_d_1 <= dummy_s;
// synthesis translate_on
end
assign var3_a = var0_a1;
assign var2_e1 = e;
assign var2_e3 = var2_e2;
assign var4_var2_a0 = var3_a;
assign var4_var2_a2 = var4_var2_a1;
assign var4_var4_a0 = var4_var2_a2;
assign var4_var4_a2 = var4_var4_a1;
assign var5_e = var4_e;
assign var7_e = var6_e;

always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	var0_stupid_only_needed_for_clk_dont_ever_use <= var0_stupid_only_needed_for_clk_dont_ever_use;
	var0_a1 <= (a + b);
	var2_e2 <= var2_e1;
	var4_var2_a1 <= var4_var2_a0;
	var4_var4_a1 <= var4_var4_a0;
	var8_var0_a <= a;
	var8_var7_a <= var8_var0_a;
	var8_var8_a <= var8_var7_a;
	var8_var9_a <= var8_var8_a;
	var8_var10_a <= var8_var9_a;
	var8_var11_a <= var8_var10_a;
	var8_var12_a <= var8_var11_a;
	var8_var13_a <= var8_var12_a;
	var8_var14_a <= var8_var13_a;
	e_1 <= (var7_e + var8_var14_a);
	multiclockpipelinecompiler_ring_2 <= {multiclockpipelinecompiler_ring_2[0], multiclockpipelinecompiler_ring_2[1]};
	if (multiclockpipelinecompiler_ring_2[0]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy0 <= stupid_only_needed_for_clk_dont_ever_use_copy0;
		e_copy0_3 <= (e_copy0_2 + a_copy0_1);
		e_copy0 <= (e_copy0_3 + a_copy0);
	end
	if (multiclockpipelinecompiler_ring_2[1]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy1 <= stupid_only_needed_for_clk_dont_ever_use_copy1;
		e_copy1_3 <= (e_copy1_2 + a_copy1_1);
		e_copy1 <= (e_copy1_3 + a_copy1);
	end
	multiclockpipelinecompiler_ring_4 <= {multiclockpipelinecompiler_ring_4[2:0], multiclockpipelinecompiler_ring_4[3]};
	if (multiclockpipelinecompiler_ring_4[0]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy0_1 <= stupid_only_needed_for_clk_dont_ever_use_copy0_1;
		e_copy0_5 <= (e_copy0_4 + e_copy0_4);
	end
	if (multiclockpipelinecompiler_ring_4[1]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy1_1 <= stupid_only_needed_for_clk_dont_ever_use_copy1_1;
		e_copy1_5 <= (e_copy1_4 + e_copy1_4);
	end
	if (multiclockpipelinecompiler_ring_4[2]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy2 <= stupid_only_needed_for_clk_dont_ever_use_copy2;
		e_copy2_1 <= (e_copy2 + e_copy2);
	end
	if (multiclockpipelinecompiler_ring_4[3]) begin
		stupid_only_needed_for_clk_dont_ever_use_copy3 <= stupid_only_needed_for_clk_dont_ever_use_copy3;
		e_copy3_1 <= (e_copy3 + e_copy3);
	end
	if (sys_rst) begin
		var0_stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		var0_a1 <= 8'd0;
		var2_e2 <= 8'd0;
		var4_var2_a1 <= 8'd0;
		var4_var4_a1 <= 8'd0;
		var8_var0_a <= 8'd0;
		var8_var7_a <= 8'd0;
		var8_var8_a <= 8'd0;
		var8_var9_a <= 8'd0;
		var8_var10_a <= 8'd0;
		var8_var11_a <= 8'd0;
		var8_var12_a <= 8'd0;
		var8_var13_a <= 8'd0;
		var8_var14_a <= 8'd0;
		e_1 <= 8'd0;
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		multiclockpipelinecompiler_ring_2 <= 2'd1;
		e_copy0 <= 8'd0;
		stupid_only_needed_for_clk_dont_ever_use_copy0 <= 1'd0;
		e_copy0_3 <= 8'd0;
		e_copy1 <= 8'd0;
		stupid_only_needed_for_clk_dont_ever_use_copy1 <= 1'd0;
		e_copy1_3 <= 8'd0;
		multiclockpipelinecompiler_ring_4 <= 4'd1;
		stupid_only_needed_for_clk_dont_ever_use_copy0_1 <= 1'd0;
		e_copy0_5 <= 8'd0;
		stupid_only_needed_for_clk_dont_ever_use_copy1_1 <= 1'd0;
		e_copy1_5 <= 8'd0;
		stupid_only_needed_for_clk_dont_ever_use_copy2 <= 1'd0;
		e_copy2_1 <= 8'd0;
		stupid_only_needed_for_clk_dont_ever_use_copy3 <= 1'd0;
		e_copy3_1 <= 8'd0;
	end
end

endmodule

