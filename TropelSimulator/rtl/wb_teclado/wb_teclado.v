`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
//Este es el TOP por: DARIO ARANGO  UNAL
//EL programa toma hasta 4 digitos del teclado y los dibuja en un 7 segmentos.
/*El módulo  llama a dos divisores, uno para que se alteren los 1 en 
 las filas del teclado y otro para el giro de los anodos del 7 segmentos.
Este módulo también realiza la identificación del dato de la tecla presionada
Llama al módulo debouncer que va a filtrar el dato y a contar cifras a medida que 
que se vayan presionando.
El modulo cifras se encarga de tomar los datos filtrados y el contador para 
almacenarlos en las ud,dec,cen y ud de mil, también se encarga de rotar los ánodos
y el dato para que se dibuje en el 7 segmentos.

*/
//////////////////////////////////////////////////////////////////////////////////
module wb_teclado(input clk, 
 	      input reset,
              input wb_stb_i,
              input wb_cyc_i,
              output  wb_ack_o,
              input   wb_we_i,
              input  [31:0] wb_adr_i,
              input  [3:0] wb_sel_i,
              input  [31:0] wb_dat_i,
              output reg  [31:0] wb_dat_o,
              //Propios del periférico
              output teclado_irq,
              input [3:0]  columnas, 
              output [3:0] filas,
              output [6:0] seg,
              output [3:0] anodos
	     
	       );
	

//
reg  ack;
assign wb_ack_o = wb_stb_i & wb_cyc_i & ack;

wire wb_rd = wb_stb_i & wb_cyc_i & ~wb_we_i;
wire wb_wr = wb_stb_i & wb_cyc_i &  wb_we_i;
		 
			 
//los renglones o filas son el registro state					
//reg  [3:0] data; //almacena el dato instantaneo despues de presionar alguna tecla

reg [3:0] state2=4'b0000;
reg [3:0] state1;
reg [3:0] data;

//Instanciación del divisor para sacar reloj de las filas


wire CLK2;
    divisor 
    div(.clk(clk),
    .CLKOUT(CLK2)
    );
//Instanciación del divisor para sacar reloj de  los ánodos

wire CLK3;
div2
    divw(.clk(clk),
    .CLKOUT(CLK3)
    );


//Máquina de estados para las filas
	always@(posedge clk or posedge reset)
   if(reset) state1<=4'b1000;
	else if(CLK2) state1<=state2;

   assign filas=state1;
	
	//Maquina de estados filas
      always@(*)
		case(state1)
		4'b1000: state2<=4'b0100;
		4'b0100: state2<=4'b0010;
		4'b0010: state2<=4'b0001;
		4'b0001: state2<=4'b1000;     
		default: state2<=4'b1000;
		endcase
	

   reg boton; //Este registro es 1 cuando se detecta alguna columna, indica
          //que hay un dato que debe  ser filtrado por el modulo deb.
			 
	always@(posedge clk)
	begin	

	boton=|columnas; //Se activa el boton cada vez que una columna sea 1.
	//Lógica para dato
	
	/* SE PLANTEA DE ACUERDO A LA INTERSECCIÓN DE FILA Y COLUMNA
	POR DEFECTO 15 4'B111 ES UN DATO QUE SE INGORA * Y # se pueden asignar
	*/
	   if(state1==8)begin
		case(columnas)
                4'b1000: data<=1;		
	        4'b0100: data<=2;	
		4'b0010: data<=3;	
		4'b0001: data<=10; //letra A	
		default: data<=15;
		endcase
      end 
	      
		if(state1==4)begin
		 case(columnas)
                 4'b1000: data<=4;		
	         4'b0100: data<=5;	
		 4'b0010: data<=6;	
		 4'b0001: data<=11; //letra B	
		 default: data<=15;
		 endcase
       end 
		 
		if(state1==2)begin
		case(columnas)
      4'b1000: data<=7;		
	   4'b0100: data<=8;	
		4'b0010: data<=9;	
		4'b0001: data<=12; //letra c	
		default: data<=15;
		endcase
      end 	      
		
		if(state1==1)begin
		case(columnas)
                4'b1000: data<=15;  //numeral invalido
	        4'b0100: data<=0;	
		4'b0010: data<=15; //asterisco invalido
		4'b0001: data<=13; //letra D	
		default: data<=15;
		endcase
      end 
  
	
	end
	
/*dataFiltrado y cifracount son el dato filtrado y 
el contador de cifras respectivamente, por ejm si 
se presiona por primera vez 8 entonces cifracount=1
si se presiona luego 7 entonces cifracount=2, y así hasta 
completar 4 cifras. la primera que presiona es udmil, luego cen y asi..
*/	

wire [3:0] dataFiltrado;
wire [2:0] cifracount;
//wire btn_out;
//Instanciación de antirebote
Debounce Deb(
.clk(clk),
.reset(reset),
.btn_in(boton),
.data_in(data), 
.cifracount(cifracount),
.btn_out(teclado_irq),
.data_out(dataFiltrado)
);



//Instanciación  de cifras
/*De acá sale un dato aux, que es el dato a dibujar en el 7 segmentos.
Dependiendo del dato filtrado y del contador de cifras va guardando en las 
variables ud,dec, cen y udmil
recibe CLK3 para rotar los ánodos y los datos
*/



wire [3:0] dataux;
wire [3:0] ud;
wire [3:0] cen;
wire [3:0] udmil;
wire [3:0] dec;

cifras Cif(
.clk(CLK3),
.reset(reset),
.dataFiltrado(dataFiltrado), 
.cifrascount(cifracount),
.ud(ud),
.dec(dec),
.cen(cen),
.udmil(udmil),
.anodos(anodos),
.dataux(dataux)
);

//WISHBONE
always @(posedge clk)
  begin //1
    if (reset) begin 
      ack <= 0;
     
    end else begin 
      ack    <= 0;
     if (wb_rd & ~ack) begin          // read cycle
       ack <= 1;
       case (wb_adr_i[7:0])
       'h00: wb_dat_o<={27'b0,dataFiltrado};
       endcase	
       end  
      if (wb_wr & ~ack) begin          // write cycle
       ack <= 1;
       end  

    end
  end //1



//7 SEGMENTOS recibe el dato dataux y lo dibuja
segmentos Seg(.dataux(dataux),
              .seg(seg)
 );
	
endmodule
