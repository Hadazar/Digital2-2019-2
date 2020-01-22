#include "bloques.h"

#include <irq.h>
#include <uart.h>
#include "LCD.h"
#include "juego.h"
#include "matrices.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int posx=0x4F;
int posbloque = 0x84;
int posbloque2 = 0x84;
int posbloque3 = 0x84;
int velocidad=5;
int muertes=3;



void bloque(unsigned int carril){

    if (carril == 1) {
      dib_cua(posbloque-0x8,0x0030,posbloque+0x8,0x0042,0x7BEF);
      crash(posbloque,0x39);
      if(posbloque >= 0x15 ){
        posbloque=posbloque-0x10;
      }else{
        posbloque = 0x84;
      }
      //dib_cua(posbloque-0x8,0x0030,posbloque+0x8,0x0042,0x7BE0);
      dib_tiles(posbloque-0x8,0x0030,carrito1);
      busy_wait(velocidad);
    }
    if (carril == 2) {
          dib_cua(posbloque2-0x8,0x0047,posbloque2+0x8,0x0057,0x7BEF);
          crash(posbloque2,0x4f);
          if(posbloque2 >= 0x15 ){
            posbloque2=posbloque2-0x10;
          }else{
            posbloque2 = 0x84;
          }
          dib_tiles(posbloque2-0x8,0x0047,carrito1);
          busy_wait(velocidad);
    }
    if (carril == 3) {
        dib_cua(posbloque3-0x8,0x005E,posbloque3+0x8,0x006C,0x7BEF);
        crash(posbloque3,0x65);
        if(posbloque3 >= 0x15 ){
          posbloque3=posbloque3-0x10;
        }else{
          posbloque3 = 0x84;
        }

        dib_tiles(posbloque3-0x8,0x005E,carrito1);
        busy_wait(velocidad);
    }
}

void  arriba (void){
  subir(0,0X8A,0x2A,0x2F,0x0000,0xFFFF);
  subir(0,0X8A,0x6f,0x74,0xFFFF,0x0000);
  subir(0,0X8A,0x43,0x45,0x7BEF,0xFFE0);
  subir(0,0X8A,0x59,0x5b,0x7BEF,0xFFE0);
  dib_tiles(0x000D,posx-0x8,carrito);
  //dib_cua(0x000D,posx-0x8,0x0001c,posx+0x8,color);
  busy_wait(1);

}
void  abajo (void){
  subir(0,0X8A,0x2A,0x2F,0x0000,0xFFFF);
  subir(0,0X8A,0x6f,0x74,0xFFFF,0x0000);
  subir(0,0X8A,0x43,0x45,0x7BEF,0xFFE0);
  subir(0,0X8A,0x59,0x5b,0x7BEF,0xFFE0);
  dib_tiles(0x000D,posx-0x8,carrito);
}
void izquierda(void){
  dib_cua(0x000D,posx-8,0x0001c,posx+8,0x7BEF);
  if(posx -0xc >= 0x2f ){
    posx = posx-0x16;
  }
  dib_tiles(0x000D,posx-0x8,carrito);
}
void derecha( void){
  dib_cua(0x000D,posx-8,0x0001c,posx+8,0x7BEF);
  if(posx +0xc  <= 0x6f ){
    posx = posx+0x16;
  }
  dib_tiles(0x000D,posx-0x8,carrito);
}

void crash(unsigned char pos, unsigned char posbloquey){
  if (pos <= 0x24) {
    if (posx == posbloquey) {

      posx = 0x4f;
      posbloque = 0x84;
      posbloque2 = 0x84;
      posbloque3 = 0x84;
      pantallasup();
      switch (muertes) {
        case 3:
              pantalladerecha();
              dib_tiles(0x84,0xA5,corazon);
              dib_tiles(0x84,0xB4,corazon);

              break;
        case 2:
              pantalladerecha();
              dib_tiles(0x84,0xA5,corazon);
              dib_tiles(0x84,0xB4,corazon);
              break;
        case 1:
              pantalladerecha();

              break;
        case 0:
              muertes=3;
              while (1) {
                dib_cua(0x00,0x00,0x8c,0x9c,0xFFFF);
                //printf("%x\n" ,botones_in_read() );
                if (botones_in_read() & 1 << 2) {
                  goto termina_pausa;
                }
              }
              termina_pausa:
              break;

      }
      margenes();
      tempo=0;
      velocidad=5;
      vuelta=0;
      muertes=muertes-1;
    }
  }
}


void subir(unsigned int imin,unsigned int imax,unsigned int omin,unsigned int omax,unsigned int color1,unsigned int color2){
    for(int i= imin ;i<= imax;i++){
      dib_cua(i,omin,i+4,omax,color1);
      dib_cua(i+4,omin,i+7,omax,color2);
      i=i+7;
    }

    busy_wait(0.5);
    for(int i=0;i<=0x8c;i++){
      dib_cua(i,omin,i+4,omax,color2);
      dib_cua(i+4,omin,i+7,omax,color1);
      i=i+7;
    }
    busy_wait(0.5);
}
