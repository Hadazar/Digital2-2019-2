`timescale 1ns / 1ps
/////////////////////////////////////////////////////////////////////////////////
/*Este modulo se encarga de recibir un dato sucio y filtrarlo convirtiendolo en un solo
pulso de un clock, esto siempre que la duración
del boton sea de al menos 800000 ciclos( para reloj de 50MHZ) 
Cada vez que se filtra el dato se aumenta en 1 el conteo de cifra
*/
//////////////////////////////////////////////////////////////////////////////////
module Debounce(
input clk,
input reset,
input btn_in, //El boton de cuando se detecta una columna
input [3:0] data_in, //El dato asociado al estado de las columnas
output reg [2:0] cifracount,
output reg btn_out, //	Se hace 1 cada vez que se filtra un dato
output reg [3:0] data_out
    );
//parameter cntmax es número de ciclos para validar el dato e ignorar periodos de rebote
//parameter cntmax=800000;
parameter cntmax=4000;
//Contador de ciclos
reg [24:0] cnt;
//Esta clona el estado del boton de entrada
reg key_rst;
//Este es el boton de salida
//reg btn_out;
//En este always, se asigna a la variables key_rst El estado del botón
always@(posedge clk or posedge reset)
if(reset) key_rst<=1'b1;
else key_rst<=btn_in;

// key_rst_r es una version retardada un ciclo del estado del boton
reg key_rst_r;
always@(posedge clk or posedge reset)
if(reset) key_rst_r<=1'b1;
else key_rst_r<=key_rst;

//Esta variable es 1 cada vez que hay un cambio en el estado del boton
//Si hay un cambio quiere decir que hay un rebote y por lo tanto el conteo se debe 
//reiniciar
wire cnt_rst=~key_rst_r&key_rst;
//reg [19:0] cnt;


//El conteo se empieza cada vez que cambia cnt_rst
//Comunmente  varias conmutaciones ocurren en los primeros 50ms

always@(posedge clk or posedge reset)
if(reset) cnt<=11'b0;
else if(cnt_rst) cnt<=11'b0;
else cnt<=cnt+1;


//Este registro se activa cada vez que hayan 
//contado los ciclos que se estiman
reg low_sw;

always@(posedge clk or posedge reset)
if(reset) low_sw<=1'b0;
else if(cnt==cntmax) low_sw<=btn_in;

//Este registro es una versiòn desplazada del flag del contador
reg low_sw_r;

always@(posedge clk or posedge reset)
if(reset) low_sw_r<=1'b0;
else low_sw_r<=low_sw;

//Esta es la bandera del botón de salida, con el ruido filtrado, es solo un ciclo.
always@(posedge clk)
begin
btn_out<=(~low_sw_r)&low_sw;
//Acá se hace la gestiòn de las filas y del conteo de cifras
if(reset) begin
cifracount<=3'b000;
data_out<=4'b1111;
//flagEnd<=1'b0;
end
if(btn_out && cifracount<4) begin
cifracount<=cifracount+1;
data_out<=data_in;
end
end

endmodule

