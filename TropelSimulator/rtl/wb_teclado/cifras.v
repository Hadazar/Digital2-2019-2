`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:11:09 12/27/2018 
// Design Name: 
//Este módulo toma el dato filtrado del debounce, y la cifra correspondiente.
//De Acuerdo al valor de la cifra va a darle un valor a las ud,dec,cen y udmil 
//Adicionalmente va a rotar los ánodos  y a rotar el dato de acuerdo al anodo
//El dato de salida será el que entra al 7 segmentos en el TOP.
//////////////////////////////////////////////////////////////////////////////////
module cifras( input clk, reset,
               input  [3:0] dataFiltrado, 
               input  [2:0] cifrascount,
               output reg [3:0] ud,
               output reg [3:0] dec,
               output reg [3:0] cen,
               output reg [3:0] udmil,
	       output reg [3:0] anodos,
	       output reg [3:0] dataux
					);

//Primero la máquina de estados de los ánodos
      reg [3:0] anodostate=4'b1110;
		
      always@(posedge clk or posedge reset)
      if(reset) anodos<=4'b1000;
	   else anodos<=anodostate;
	
	
      always@(*)
		case(anodos)
		4'b0111: anodostate<=4'b1110;
		4'b1110: anodostate<=4'b1101;
		4'b1101: anodostate<=4'b1011;
		4'b1011: anodostate<=4'b0111;     
		default: anodostate<=4'b1110;
		endcase

				
//Máquina de estados para el dato de salida que va al 7 segmentos

      always@(*)
		case(anodos)
		4'b1110: dataux<=ud;
		4'b1101: dataux<=dec;
		4'b1011: dataux<=cen;
		4'b0111: dataux<=udmil;     
		default: dataux<=dec;
		endcase


//Proceso para asignación de cifras (EL primer dato es la cifra más significativa)
always@(posedge clk or posedge reset)
begin
      if(reset) begin 
		ud<=4'b1111;
		dec<=4'b1111;
		cen<=4'b1111;
		udmil<=4'b1111;
		
	   end
		else begin
		//dataux<=cifrascount;
		case(cifrascount)
		3'b001: udmil<=dataFiltrado;
		3'b010: cen<=dataFiltrado;
		3'b011: dec<=dataFiltrado;
		3'b100: ud<=dataFiltrado;     
		default: ud<=dataFiltrado;
		endcase
		
		
      end
end
	
		
		

endmodule
