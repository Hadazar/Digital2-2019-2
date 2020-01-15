//----------------------------------------------------------------------------
//
//----------------------------------------------------------------------------
`timescale 1 ns / 100 ps

module system_tb;

//----------------------------------------------------------------------------
// Parameter (may differ for physical synthesis)
//----------------------------------------------------------------------------
parameter tck              = 20;       // clock period in ns
parameter uart_baud_rate   = 1152000;  // uart baud rate for simulation 

parameter clk_freq = 1000000000 / tck; // Frequenzy in HZ
//----------------------------------------------------------------------------
//INPUTS
//----------------------------------------------------------------------------
reg        clk;
reg        rst;
reg     [3:0] columnas;
wire    [7:0] gpio_out;
wire    [3:0] filas;
wire    [6:0] seg;
wire    [3:0] an;

//----------------------------------------------------------------------------
// UART STUFF (testbench uart, simulating a comm. partner)
//----------------------------------------------------------------------------
wire         uart_rxd;
wire         uart_txd;

//----------------------------------------------------------------------------
// Device Under Test 
//----------------------------------------------------------------------------
system #(
	.clk_freq(           clk_freq         ),
	.uart_baud_rate(     uart_baud_rate   )
) dut  (
	.clk(clk), 
	.rst(rst),
        .gpio_out(gpio_out),
        .columnas(columnas),
        .filas(filas),
        .seg(seg),
        .an(an)
);

/* Clocking device */
initial         clk <= 0;
always #(tck/2) clk <= ~clk;

/* Simulation setup */
initial begin



	$dumpfile("system_tb.vcd");
	//$monitor("%b,%b,%b,%b",clk,rst,uart_txd,uart_rxd);
	$dumpvars(-1, dut);
	//$dumpvars(-1,clk,rst,uart_txd);
	// reset
	#0  rst <= 0;
	#80 rst <=1;
        #10000 columnas=4; 
        #10000 columnas=0;
        #10000 columnas=4;
#10000 columnas=0;
#10000 columnas=4;
#10000 columnas=0;
#10000 columnas=4;
#100000 columnas=0;

	#(tck*10000) $finish;
end



endmodule
