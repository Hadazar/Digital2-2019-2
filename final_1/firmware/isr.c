
#include <irq.h>
#include <uart.h>
#include <generated/csr.h>

#include "bloques.h"
#include "LCD.h"
#include "juego.h"

extern void periodic_isr(void);
void botton_isr(void);
void isr(void);
void isr(void)
{
	unsigned int irqs;

	irqs = irq_pending() & irq_getmask();

	if(irqs & (1 << UART_INTERRUPT))
		uart_isr();
	if(irqs & (1 << 4))
	 botton_isr();


}
void botton_isr(void){
	// borrador por soft la interrupción del periferico
	unsigned int pednig = botones_ev_pending_read();

	//00000001		start
		if (pednig & 1) {
			
		}
		//00000010  reset
		if (pednig & 1 << 0x1) {

			while (1) {
				dib_cua(0x00,0x00,0x8c,0x9c,0x0000);
				if (botones_in_read() & 1 << 2) {
					goto termina_pausa;
				}
			}
			termina_pausa:
			margenes();



		}
		//00000100  derechasss
		if (pednig & 1 << 2) {

		}
		//00001000 izqueirdassss
		if (pednig & 1 << 0x3) {

		}
		//00010000
		if (pednig & 1 << 0x04) {
			izquierda();
		}
		//00100000
		if (pednig & 1 << 0x05) {
			abajo ();
			if(velocidad  >= 0.4 ){
				velocidad =5;
			}
		}
		//0100000
		if (pednig & 1 << 0x06) {
			derecha();
		}
		//0100000
		if (pednig & 1 << 0x07) {
			arriba();
			if(velocidad  >= 0x00 ){
				velocidad =1;
			}
			//dib_cua(Xmin,Ymin,Xmax,Ymax,color);
		}
  botones_ev_pending_write (0xff);
  botones_ev_enable_write(0xff);

}
