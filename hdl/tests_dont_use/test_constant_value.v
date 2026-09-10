`timescale 1ns / 1ps

/* Machine-generated using Migen */
module test_constant_value(
	output reg stupid_only_needed_for_clk_dont_ever_use,
	input sys_clk,
	input sys_rst
);



always @(posedge sys_clk) begin
	stupid_only_needed_for_clk_dont_ever_use <= stupid_only_needed_for_clk_dont_ever_use;
	if (sys_rst) begin
		stupid_only_needed_for_clk_dont_ever_use <= 1'd0;
	end
end

endmodule

