#include "soc-hw.h"

uart_t     *uart0    = (uart_t *)    0x20000000;
timer_t    *timer0   = (timer_t *)   0x30000000;
gpio_t     *gpio0    = (gpio_t *)    0x40000000;
teclado_t  *teclado0 =(teclado_t *)  0x50000000;

//spi_t      *spi0     = (spi_t *)     0x50000000;


isr_ptr_t isr_table[32];  // isr_table será un arreglo de procedimientos, para cada bit de interrupción

void tic_isr();
/***************************************************************************
 * IRQ handling
 */
void isr_null()
{
}









//Recorre la tabla de procedimientos asociados a cada bit de interrupcion y la ejecuta
//Luego corre el valor de pending para recorrer todas las posibles interrupciones
/*void irq_handler(uint32_t pending)
{
    int i;

    for(i=0; i<32; i++) {
        if (pending & 0x01) (*isr_table[i])(); //si es uno el bit de interrupción ejecuta el procedimiento.
        pending >>= 1;
    }
}*/

void isr_init()
{
    int i;
    for(i=0; i<32; i++)
        isr_table[i] = &isr_null;
}

void isr_register(int irq, isr_ptr_t isr)
{
    isr_table[irq] = isr;
}

void isr_unregister(int irq)
{
    isr_table[irq] = &isr_null;
}

/***************************************************************************
 * TIMER Functions
 */
uint32_t tic_msec;

void msleep(uint32_t msec)
{
    uint32_t tcr;

    // Use timer0.1
    timer0->compare1 = (FCPU/1000)*msec;
    timer0->counter1 = 0;
    timer0->tcr1 = TIMER_EN;

    do {
        //halt();
         tcr = timer0->tcr1;
     } while ( ! (tcr & TIMER_TRIG) );
}

void nsleep(uint32_t nsec)
{
    uint32_t tcr;

    // Use timer0.1
    timer0->compare1 = (FCPU/1000000)*nsec;
    timer0->counter1 = 0;
    timer0->tcr1 = TIMER_EN;

    do {
        //halt();
         tcr = timer0->tcr1;
     } while ( ! (tcr & TIMER_TRIG) );
}

void tic_isr()
{
    tic_msec++;
    timer0->tcr0     = TIMER_EN | TIMER_AR | TIMER_IRQEN;
}

void tic_init()
{
    tic_msec = 0;

    // Setup timer0.0
    timer0->compare0 = (FCPU/10000);
    timer0->counter0 = 0;
    timer0->tcr0     = TIMER_EN | TIMER_AR | TIMER_IRQEN;

    isr_register(1, &tic_isr);
}


/***************************************************************************
 * UART Functions
 */
void uart_init()
{
    //uart0->ier = 0x00;  // Interrupt Enable Register
    //uart0->lcr = 0x03;  // Line Control Register:    8N1
    //uart0->mcr = 0x00;  // Modem Control Register

    // Setup Divisor register (Fclk / Baud)
    //uart0->div = (FCPU/(57600*16));
}

char uart_getchar()
{   
    while (! (uart0->ucr & UART_DR)) ;
    return uart0->rxtx;
}

void uart_putchar(char c)
{
    while (uart0->ucr & UART_BUSY) ;
    uart0->rxtx = c;
}

void uart_putstr(char *str)
{
    char *c = str;
    while(*c) {
        uart_putchar(*c);
        c++;
    }
}


/*
GPIO
***************************************************************************
*/

uint32_t readGpio()
{
return gpio0->in;
}

void writeGpio(uint32_t data)
{
gpio0->out = data;
}

/*TECLADO*/

uint32_t getdato(){
return teclado0->dato;
};
/*INTERRUPCIONES*/
void irq_handler(uint32_t pending)
{   
  int i;
  i=pending & 16;  //Rescata el bit al cuál le quiero meter la interrupción.   10010&10000=10000
    if (i==16){
  uint32_t  a;
   a=getdato();  //lee dato del teclado
   writeGpio(a); //escribe dato en GPIO
   }
  
}









