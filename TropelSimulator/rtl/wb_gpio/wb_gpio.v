/*
 *
 * Simple 24-bit wide GPIO module
 * 
 * Can be made wider as needed, but must be done manually.
 * 
 * First lot of bytes are the GPIO I/O regs
 * Second lot are the direction registers
 * 
 * Set direction bit to '1' to output corresponding data bit.
 *
 * Register mapping:
 *  
 * For 8 GPIOs we would have
 * adr 0: gpio data 7:0
 * adr 1: gpio data 15:8
 * adr 2: gpio data 23:16
 * adr 3: gpio dir 7:0
 * adr 4: gpio dir 15:8
 * adr 5: gpio dir 23:16
 * 
 * Backend pinout file needs to be updated for any GPIO width changes.
 * 
 */ 

module wb_gpio(
              input clk, 
              input reset,
              input wb_stb_i,
              input wb_cyc_i,
              output  wb_ack_o,
              input   wb_we_i,
              input  [31:0] wb_adr_i,
              input  [3:0] wb_sel_i,
              input  [31:0] wb_dat_i,
              output reg  [31:0] wb_dat_o,
              output reg [7:0] gpio_out,
              input [7:0] gpio_in
	   
);




   wire wb_rd = wb_stb_i & wb_cyc_i & ~wb_we_i;
   wire wb_wr = wb_stb_i & wb_cyc_i &  wb_we_i;
   reg  ack;
   assign wb_ack_o = wb_stb_i & wb_cyc_i & ack;
    
 
always @(posedge clk)
  begin //1
    if (reset) begin 
      ack <= 0;
     
    end else begin 
      ack    <= 0;
     if (wb_rd & ~ack) begin          // read cycle
       ack <= 1;
       case (wb_adr_i[7:0])
       'h04: wb_dat_o[7:0]<=gpio_in;
       endcase	
       end  
      if (wb_wr & ~ack) begin          // write cycle
       ack <= 1;
       case (wb_adr_i[7:0])
       'h00:  gpio_out<= wb_dat_i[7:0];
       endcase	
       end  

    end
  end //1

  

endmodule 
        

