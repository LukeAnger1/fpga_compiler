`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_math_operations_2(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input signed [4:0] var,
	output reg signed [4:0] var_1,
	input sys_clk,
	input sys_rst
);


// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on


// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	var_1 <= 5'sd0;
	if (var[4]) begin
		var_1 <= (-var);
	end else begin
		var_1 <= var;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end

always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
	end
end

endmodule

