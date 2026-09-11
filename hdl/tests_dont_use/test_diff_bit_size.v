`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_diff_bit_size(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input signed [4:0] a,
	input signed [9:0] b,
	input signed [4:0] c,
	input signed [9:0] d,
	output reg signed [9:0] a_1,
	output reg signed [9:0] a_2,
	output reg signed [9:0] a_3,
	output reg signed [9:0] a_4,
	output reg signed [9:0] a_5,
	output reg signed [9:0] a_6,
	output reg signed [4:0] a_7,
	output reg signed [4:0] a_8,
	output reg signed [4:0] a_9,
	output reg signed [9:0] c_1,
	output reg signed [9:0] b_1,
	output reg signed [9:0] c_2,
	output reg signed [9:0] b_2,
	output reg signed [9:0] c_3,
	output reg signed [9:0] b_3,
	output reg signed [9:0] c_4,
	output reg signed [9:0] c_5,
	output reg signed [9:0] c_6,
	output reg signed [9:0] c_7,
	output reg signed [9:0] c_8,
	output reg signed [9:0] c_9,
	output reg signed [9:0] a_10,
	output reg signed [9:0] a_11,
	output reg signed [9:0] a_12,
	output reg signed [9:0] a_13,
	output reg signed [9:0] a_14,
	output reg signed [9:0] a_15,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	if (a[4]) begin
		a_1 <= {{5{1'd1}}, a};
	end else begin
		a_1 <= {{5{1'd0}}, a};
	end
	a_2 <= (a_1 + b);
	if (a[4]) begin
		a_3 <= {{5{1'd1}}, a};
	end else begin
		a_3 <= {{5{1'd0}}, a};
	end
	a_4 <= (a_3 - b);
	if (a[4]) begin
		a_5 <= {{5{1'd1}}, a};
	end else begin
		a_5 <= {{5{1'd0}}, a};
	end
	a_6 <= (a_5 * b);
	a_7 <= (a + c);
	a_8 <= (a - c);
	a_9 <= (a * c);
	if (c[4]) begin
		c_1 <= {{5{1'd1}}, c};
	end else begin
		c_1 <= {{5{1'd0}}, c};
	end
	b_1 <= (b + c_1);
	if (c[4]) begin
		c_2 <= {{5{1'd1}}, c};
	end else begin
		c_2 <= {{5{1'd0}}, c};
	end
	b_2 <= (b - c_2);
	if (c[4]) begin
		c_3 <= {{5{1'd1}}, c};
	end else begin
		c_3 <= {{5{1'd0}}, c};
	end
	b_3 <= (b * c_3);
	if (c[4]) begin
		c_4 <= {{5{1'd1}}, c};
	end else begin
		c_4 <= {{5{1'd0}}, c};
	end
	c_5 <= (c_4 + d);
	if (c[4]) begin
		c_6 <= {{5{1'd1}}, c};
	end else begin
		c_6 <= {{5{1'd0}}, c};
	end
	c_7 <= (c_6 - d);
	if (c[4]) begin
		c_8 <= {{5{1'd1}}, c};
	end else begin
		c_8 <= {{5{1'd0}}, c};
	end
	c_9 <= (c_8 * d);
	if (a[4]) begin
		a_10 <= {{5{1'd1}}, a};
	end else begin
		a_10 <= {{5{1'd0}}, a};
	end
	a_11 <= (a_10 + d);
	if (a[4]) begin
		a_12 <= {{5{1'd1}}, a};
	end else begin
		a_12 <= {{5{1'd0}}, a};
	end
	a_13 <= (a_12 - d);
	if (a[4]) begin
		a_14 <= {{5{1'd1}}, a};
	end else begin
		a_14 <= {{5{1'd0}}, a};
	end
	a_15 <= (a_14 * d);
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
		a_1 <= 10'sd0;
		a_2 <= 10'sd0;
		a_3 <= 10'sd0;
		a_4 <= 10'sd0;
		a_5 <= 10'sd0;
		a_6 <= 10'sd0;
		a_7 <= 5'sd0;
		a_8 <= 5'sd0;
		a_9 <= 5'sd0;
		c_1 <= 10'sd0;
		b_1 <= 10'sd0;
		c_2 <= 10'sd0;
		b_2 <= 10'sd0;
		c_3 <= 10'sd0;
		b_3 <= 10'sd0;
		c_4 <= 10'sd0;
		c_5 <= 10'sd0;
		c_6 <= 10'sd0;
		c_7 <= 10'sd0;
		c_8 <= 10'sd0;
		c_9 <= 10'sd0;
		a_10 <= 10'sd0;
		a_11 <= 10'sd0;
		a_12 <= 10'sd0;
		a_13 <= 10'sd0;
		a_14 <= 10'sd0;
		a_15 <= 10'sd0;
	end
end

endmodule

