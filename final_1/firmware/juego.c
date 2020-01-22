#include "juego.h"

#include <irq.h>
#include <uart.h>
#include "LCD.h"
#include "bloques.h"
#include "matrices.h"

unsigned int tempo;
unsigned int vuelta;

void juego(unsigned int color){
  start:
  while(1){
    if (botones_in_read () & 1 << 0x1 ) {
      goto empezar;
    }
    dib_cua(0x00,0x00,0xaf,0xDB,0x001F);
  }

  empezar:
  //dibujar pantalla con lteras
  //busy_wait(20)
  margenes();
  pantallasup();
  pantalladerecha();
  dib_tiles(0x84,0xA5,corazon);
  dib_tiles(0x84,0xB4,corazon);
  dib_tiles(0x84,0xc3,corazon);
  preparacion();
  nivel1();

  while (1) {
    if (botones_in_read() & 1 << 0x3) {
      goto start;
    }
     if (botones_in_read() & 1 << 0x2) {
      goto empezar;
    }
  }

}

void pantalladerecha(void){
  dib_cua(0x00,0xA2,0xaf,0xDB,0xC618);
}
void pantallasup(void){
  dib_cua(0x92,0x00,0xaf,0x1A,0xC618);
  dib_cua(0x92,0x82,0xaf,0x9C,0xC618);
  dib_cua(0x92,0x1A,0xaf,0x82,0x901A);


}
void margenes(void){
    //dib morado
    dib_cua(0x00,0x00,0x8c,0x2A,0x03E0);
    dib_cua(0x00,0x74,0x8c,0x9c,0x03E0 ); //past0
    dib_cua(0x00,0x2f,0x8c,0x6f,0x7BEF); //pista
    //dib_cua(0x000D,0x0047,0x0001c,0x0055,0XC618);
    dib_tiles(0x000D,0x0047,carrito);


    for(int i=0;i<=0x8A;i++){
      dib_cua(i,0x2A,i+4,0x2F,0x0000);
      dib_cua(i+4,0x2A,i+7,0x2F,0xFFFF);
      i=i+7;
    }
    for(int i=0;i<=0x8A;i++){
      dib_cua(i,0x6f,i+4,0x74,0x0000);
      dib_cua(i+4,0x6f,i+7,0x74,0xFFFF);
      i=i+7;
    }
    for(int i=0;i<=0X8A;i++){
      dib_cua(i,0x43,i+4,0x45,0x7BEF);
      dib_cua(i+4,0x43,i+7,0x45,0xFFE0);
      i=i+7;
    }
    for(int i=0;i<=0x8A;i++){
      dib_cua(i,0x59,i+4,0x5b,0x7BEF);
      dib_cua(i+4,0x59,i+7,0x5b,0xFFE0);
      i=i+7;
    }


    for(int i=0X00;i<=0xA0;i++){
      dib_cua(0x8c,i-2,0x92,i+2,0x0000);
    }
    for(int i=0X00;i<=0xAf;i++){
      dib_cua(i-2,0x9c,i+2,0xA2,0x0000);
    }
}


void preparacion(void){
  dib_cua(0x92,0x1A,0xaf,0x82,0xF800);
  busy_wait(30);
  dib_cua(0x92,0x1A,0xaf,0x82,0xFFE0);
  busy_wait(20);
  dib_cua(0x92,0x1A,0xaf,0x82,0x07E0);
  busy_wait(5);
}

void nivel1(void){
  for (vuelta = 1; vuelta <=8; vuelta++) {
    dib_cua(0x92,(0x0D*vuelta)+0x0D,0xaf,(0x0D*vuelta)+0x1A,0xFEA0);
      for (tempo = 0; tempo <= 23; tempo++) {
          if (tempo <= 1) {
            bloque(1);
          }

          if ((tempo >= 2) &&(tempo <= 5)) {
            bloque(3);
            bloque(1);
          }
/*
          if ((tempo >= 6) &&(tempo <= 7)) {
            bloque(2);
            bloque(3);
            bloque(1);
          }
          if ((tempo >= 8) &&(tempo <= 10)) {
            bloque(2);
            bloque(3);
          }
          if ((tempo >= 11) &&(tempo <= 11)) {
            bloque(1);
            bloque(2);
          }

          if ((tempo >= 12) &&(tempo <= 13)) {
            bloque(2);
            bloque(3);
            bloque(1);
          }
          if ((tempo >= 14) &&(tempo <= 15)) {
            bloque(1);
            bloque(3);
          }
          if ((tempo >= 16) &&(tempo <= 18)) {
            bloque(1);
            bloque(2);
            bloque(3);
          }
          if ((tempo >= 19) &&(tempo <= 19)) {
            bloque(2);
            bloque(3);
          }
          if ((tempo >= 20) &&(tempo <= 23)) {
            bloque(2);
          }
  //*/
        }

  }
  dib_cua(0x92,0x1A,0xaf,0x82,0xFFFF);
  for (int bandera = 1; bandera <= 8; bandera++) {
    if ( bandera % 2 == 0 ){
      dib_cua(0xA5,(0x0D*bandera)+0x0D,0xaf,(0x0D*bandera)+0x1A,0x0000);
      dib_cua(0x92,(0x0D*bandera)+0x0D,0x9B,(0x0D*bandera)+0x1A,0x0000);
    }else{
      dib_cua(0x9B,(0x0D*bandera-1)+0x0D,0xA5,(0x0D*bandera-1)+0x1A,0x0000);
    }
  }
  posbloque = 0x84;
  posbloque2 = 0x84;
  posbloque3 = 0x84;
  tempo=0x00;
}
