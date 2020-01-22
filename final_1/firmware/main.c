#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>
#include "LCD.h"
#include "juego.h"
#include "bloques.h"


//Funciones para la memoria SD
unsigned OFFLINE      = (1 << 0);
unsigned CS_POLARITY  = (1 << 3);
unsigned CLK_POLARITY = (1 << 4);
unsigned CLK_PHASE    = (1 << 5);
unsigned LSB_FIRST    = (1 << 6);
unsigned HALF_DUPLEX  = (1 << 7);
unsigned DIV_READ     = (1 << 16);
unsigned DIV_WRITE    = (1 << 24);

// xfer mapping
unsigned WRITE_LENGTH = (1 << 16);
unsigned READ_LENGTH  = (1 << 24);


static void SD_configure(void) {
  unsigned config = 0*OFFLINE;
  config |= 0*CS_POLARITY | 0*CLK_POLARITY | 0*CLK_PHASE;
  config |= 0*LSB_FIRST | 0*HALF_DUPLEX;
	config |= 300*DIV_READ | 300*DIV_WRITE;//Divisior para
  //config |= 248*DIV_READ | 248*DIV_WRITE;//Divisior para
	//																			reloj de 5MHz(16)
	//				100M/400k = div_write + 2...248
  SD_config_write(config);
	SD_xfer_write(1 | 24*WRITE_LENGTH);
  printf("Configuracion finalizada: %x\n",config);
}

static void SD_write_24(unsigned long int value){

	SD_mosi_data_write(value << 8) ;
	SD_start_write(1);
}

static void SD_write_48(unsigned long int value1, unsigned long int value2){
	SD_xfer_write(1 | 24*WRITE_LENGTH);
	SD_write_24(value1);
	while (SD_pending_read() & 0x1){};
	SD_write_24(value2);
	while (SD_active_read() & 0x1){};

}

static void botones(void)
{
	botones_ev_pending_write(0xff); //flag
	botones_ev_enable_write(0xff);
	irq_setmask(irq_getmask() | (1 << BOTONES_INTERRUPT));
}



int main(void)
{
	irq_setmask(0);
	irq_setie(1); //habilita las interrupciones
	botones();
	uart_init();
	lcd_config();
	lcd_inic();
	juego(0XC618);
	while(1) {

	}

	return 0;
}
