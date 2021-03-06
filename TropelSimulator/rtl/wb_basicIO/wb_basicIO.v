//---------------------------------------------------------------------------
//
// Wishbone BasicIO
//
// Register Description:
//
//    0x00 BasicIO_Leds
//    0x04 BasicIO_Switches
//    0x08 BasicIO_Buttons
//
//---------------------------------------------------------------------------

module wb_basicIO (
   input              clk,
   input              reset,
   // Wishbone interface
   input              wb_stb_i,
   input              wb_cyc_i,
   output             wb_ack_o,
   input              wb_we_i,
   input       [31:0] wb_adr_i,
   input        [3:0] wb_sel_i,
   input       [31:0] wb_dat_i,
   output reg  [31:0] wb_dat_o,
   // BasicIO Output
   output reg [7:0] basicIO_led,
   output basicIO_btn_intr,
   // BasicIO Input
   input      [7:0]  sw,	//Switch
   input basicIO_btn		//Boton
);

//---------------------------------------------------------------------------
// 
//---------------------------------------------------------------------------
reg  ack;
assign wb_ack_o = wb_stb_i & wb_cyc_i & ack;

wire wb_rd = wb_stb_i & wb_cyc_i & ~wb_we_i;
wire wb_wr = wb_stb_i & wb_cyc_i &  wb_we_i;

  debouncer debouncer0(
  .clk(clk),
  .PB(basicIO_btn),
  .PB_state(),
  .PB_up(basicIO_btn_intr),
  .PB_down()
  );

  always @(posedge clk)
  begin
    if (reset) begin
      ack <= 0;
      basicIO_led <= 0;
    end else begin

      // Handle WISHBONE access
      ack    <= 0;

     if (wb_rd & ~ack) begin           // read cycle
       ack <= 1;
       case (wb_adr_i[7:0])
       'h04: wb_dat_o <= {24'b0,sw};
       endcase	
     end else if (wb_wr & ~ack ) begin // write cycle
       ack <= 1;
       case (wb_adr_i[7:0])
       'h00: basicIO_led[7:0] <= wb_dat_i[7:0];
       endcase
     end
    end
  end

endmodule
