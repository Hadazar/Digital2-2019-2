`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    07:34:58 12/28/2018 
// Design Name: 
// Module Name:    segmentos 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module segmentos( input [3:0] dataux,
                  output reg [6:0] seg
    );


always @(*)
case(dataux)
0: seg=7'b0000001;
1: seg=7'b1001111;
2: seg=7'b0010010;
3: seg=7'b0000110;
4: seg=7'b1001100;
5: seg=7'b0100100;
6: seg=7'b0100000;
7: seg=7'b0001110;
8: seg=7'b0000000;
9: seg=7'b0000100;
10: seg=7'b0001000;//A
11: seg=7'b1100000;//b
12: seg=7'b0110001;//C
13: seg=7'b1000010;//d
14: seg=7'b0110000;//E
15: seg=7'b1111110;//F
default: seg=7'b1111111;
endcase
endmodule
