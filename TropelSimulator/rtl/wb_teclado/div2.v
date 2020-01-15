`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// // Este no es como tal un divisor periodico sino saca solo un alto cada vez que se  
//cumplen los ciclos establecidos  y tres ciclos de reloj despues se apaga
// Engineer: 
//////////////////////////////////////////////////////////////////////////////////
module div2(
				input           clk,
				output	reg	CLKOUT
			);
  
 //parameter nciclos=62500;
parameter nciclos=7;
	reg [29:0] contador=0;
	
	always @(posedge clk) 
	begin
		
		if(contador <nciclos+3 && contador >nciclos)
		begin
			contador<=0;
			CLKOUT <= 1;
		end
		else 
		begin
		contador <=contador + 1;
		CLKOUT <= 0;
		end
	end
endmodule
