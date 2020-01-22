#include "LCD.h"
#include <irq.h>
#include <uart.h>
#include <stdio.h>
#include "bloques.h"





void lcd_inic(void){
  	lcd_config();
  	rst_out_write(1);
  	busy_wait(0.01);
  	rst_out_write(0);
  	busy_wait(0.1);
  	rst_out_write(1);
  	busy_wait(0.5);
  	//power_control r:10h-11h-12h-13h-14h
  	//limpia los registros
  	lcd_write(0,0x0010); //
  	lcd_write(1,0x0000);
  	lcd_write(0,0x0011);//
  	lcd_write(1,0x0000);
  	lcd_write(0,0x0012);//
  	lcd_write(1,0x0000);
  	lcd_write(0,0x0013);//
  	lcd_write(1,0x0000);
  	lcd_write(0,0x0014);//
  	lcd_write(1,0x0000);
  	busy_wait(0.4); //microseg //40 mili
  	//secuencia en power_control
  	lcd_write(0,0x0011);//
  	lcd_write(1,0x0018);
  	lcd_write(0,0x0012);//
  	lcd_write(1,0x6121);
  	lcd_write(0,0x0013);//
  	lcd_write(1,0x006f);
  	lcd_write(0,0x0014);//
  	lcd_write(1,0x495f);
  	lcd_write(0,0x0010);//
  	lcd_write(1,0x0800);

  	busy_wait(0.1);//microseg

  	lcd_write(0,0x0011);//
  	lcd_write(1,0x103B);


  	//
  	busy_wait(0.5);
  	//Driver Output Control
  	lcd_write(0,0x0001);//
  	lcd_write(1,0x011C); //r01h ss=1 nl=[1000] lo demas si es estandar como esta en el manual
  	//LCD_AC_DRIVING_CTRL
  	lcd_write(0,0x0002);//
  	lcd_write(1,0x0100); //r01h inv [01]-0 ->Line Inversion – 1 field interlace
    //ENTRY_MODE
  	lcd_write(0,0x0003);//
  	lcd_write(1,0x1038);
  	//DISP_CTRL1
  	lcd_write(0,0x0007);//
  	lcd_write(1,0x0000);
  	//BLANK_PERIOD_CTRL1
  	lcd_write(0,0x0008);//
  	lcd_write(1,0x0802);
  	//FRAME_CYCLE_CTRL
  	lcd_write(0,0x000B);//
  	lcd_write(1,0x1100);
  	//INTERFACE_CTRL
  	lcd_write(0,0x000C);//
  	lcd_write(1,0x0000);
  	//OSC_CTRL
  	lcd_write(0,0x000F);//
  	lcd_write(1,0x0D01);
  	//VCI_RECYCLING
  	lcd_write(0,0x0015);//
  	lcd_write(1,0x0020);
  	//RAM_ADDR_SET1
  	lcd_write(0,0x0020);//
  	lcd_write(1,0x0000);
  	//RAM_ADDR_SET2
  	lcd_write(0,0x0021);//
  	lcd_write(1,0x0000);

  	//Set GRAM area------------------------------------
  	//es como una memoria interna dodne yo puedo dibujar
  	//GATE_SCAN_CTRL
  	lcd_write(0,0x0030);//
  	lcd_write(1,0x0000);
  	//VERTICAL_SCROLL_CTRL1
  	lcd_write(0,0x0031);//
  	lcd_write(1,0x00DB);
  	//VERTICAL_SCROLL_CTRL2
  	lcd_write(0,0x0032);//
  	lcd_write(1,0x0000);
  	//VERTICAL_SCROLL_CTRL3
  	lcd_write(0,0x0033);//
  	lcd_write(1,0x0000);
  	//PARTIAL_DRIVING_POS1
  	lcd_write(0,0x0034);//
  	lcd_write(1,0x00DB);
  	//PARTIAL_DRIVING_POS2
  	lcd_write(0,0x0035);//
  	lcd_write(1,0x0000);


  	//HORIZONTAL_WINDOW_ADDR1
  	lcd_write(0,0x0036);//
  	lcd_write(1,0x00AF);
  	//HORIZONTAL_WINDOW_ADDR2
  	lcd_write(0,0x0037);//
  	lcd_write(1,0x0000);
  	//VERTICAL_WINDOW_ADDR1
  	lcd_write(0,0x0038);//
  	lcd_write(1,0x00DB);
  	//VERTICAL_WINDOW_ADDR2
  	lcd_write(0,0x0039);//
  	lcd_write(1,0x0000);

  	// Set GAMMA curve-------------------------------------
  	//GAMMA_CTRL1
  	lcd_write(0,0x0050);//
  	lcd_write(1,0x0000);
  	//GAMMA_CTRL2
  	lcd_write(0,0x0051);//
  	lcd_write(1,0x0808);
  	//GAMMA_CTRL3
  	lcd_write(0,0x0052);//
  	lcd_write(1,0x080A);
  	//GAMMA_CTRL4
  	lcd_write(0,0x0053);//
  	lcd_write(1,0x000A);
  	//GAMMA_CTRL5
  	lcd_write(0,0x0054);//
  	lcd_write(1,0x0A08);
  	//GAMMA_CTRL6
  	lcd_write(0,0x0055);//
  	lcd_write(1,0x0808);
  	//GAMMA_CTRL7
  	lcd_write(0,0x0056);//
  	lcd_write(1,0x0000);
  	//GAMMA_CTRL8
  	lcd_write(0,0x0057);//
  	lcd_write(1,0x0A00);
  	//GAMMA_CTRL9
  	lcd_write(0,0x0058);//
  	lcd_write(1,0x0710);
  	//GAMMA_CTRL10
  	lcd_write(0,0x0059);//
  	lcd_write(1,0x0710);

  	 //-----------------------------------
  	//DISP_CTRL1
  	lcd_write(0,0x0007);//
  	lcd_write(1,0x0012);
  	busy_wait(0.5);
  	//DISP_CTRL1
  	lcd_write(0,0x0007);//
  	lcd_write(1,0x1017);
  	// Turn on backlight
  	 //setBacklight(true);
  	 //setOrientation(0);

  	 // Initialize variables
  	 //setBackgroundColor( COLOR_BLACK );
  	//ENTRY MODE
  	lcd_write(0,0x0003);//
  	lcd_write(1,0x1018); //r03h -ver documentaciosn
  	//HORIZONTAL_WINDOW_ADDR1
  	lcd_write(0,0x0036);//
  	lcd_write(1,0x00AF); //
  	//HORIZONTAL_WINDOW_ADDR2
  	lcd_write(0,0x0037);//
  	lcd_write(1,0x0000); //
  	//VERTICAL_WINDOW_ADDR1
  	lcd_write(0,0x0038);//
  	lcd_write(1,0x00DB); //
  	//VERTICAL_WINDOW_ADDR2
  	lcd_write(0,0x0039);//
  	lcd_write(1,0x0000); //
  	//RAM_ADDR_SET1
  	lcd_write(0,0x0020);//
  	lcd_write(1,0x0000); //
  	//RAM_ADDR_SET2
  	lcd_write(0,0x0021);//
  	lcd_write(1,0x0000); //

  	 //Inicio de Transferencia de datos
  	 //WRITE DATA TO GRAM
  	 lcd_write(0,0x0022);//
  	 lcd_write(1,0x901A); //

}


void lcd_config(void){
	   lcd_xfer_write(1 | 0x100000); //180001
	   lcd_config_write(0x10300000); //5000 Khz
}


void lcd_write( unsigned char rs, unsigned int info){
		rs_out_write(rs);
		lcd_mosi_data_write(info<<16);
		lcd_start_write(1);
		while (lcd_active_read()){
		};
}

void dib_cua(unsigned int Xmin,unsigned int Ymin,unsigned int Xmax,unsigned int ymax,unsigned int color){
	for (unsigned int x = Xmin ; x < Xmax; x++) {
		lcd_write(0,0x0020);//
		lcd_write(1,x); //
		for (unsigned int y = Ymin; y < ymax; y++) {
				//direccion hoorizontal
				lcd_write(0,0x0021);//
				lcd_write(1,y); //
				lcd_write(0,0x0022);//
				lcd_write(1,color); //
		}
	}
}

void dib_tiles(unsigned int Xmin,unsigned int Ymin, Matriz matris){
  unsigned int m=0;
  unsigned int n=0;
  for (unsigned int x = Xmin ; x <= Xmin+0xD; x++) {
		lcd_write(0,0x0020);//
		lcd_write(1,x); //

		for (unsigned int y = Ymin; y <= Ymin+0xD; y++) {
				//direccion hoorizontal
				lcd_write(0,0x0021);//
				lcd_write(1,y); //ss
				lcd_write(0,0x0022);
       lcd_write(1,matris[m][n]);
       n++;
		}
    n=0;
    m++;
	}
}



void busy_wait(unsigned int ds){
	timer0_en_write(0);
	timer0_reload_write(0);
	timer0_load_write(SYSTEM_CLOCK_FREQUENCY/10*ds);
	timer0_en_write(1);
	timer0_update_value_write(1);
	while(timer0_value_read()) timer0_update_value_write(1);
}
