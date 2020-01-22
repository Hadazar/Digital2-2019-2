#ifndef BLOQUES_H
#define BLOQUES_H

#include <generated/csr.h>
#include <stdio.h>
#include <stdlib.h>


int posx;
int posbloque;
int posbloque2 ;
int posbloque3 ;
int muertes;

unsigned int tempo;

int velocidad;

void bloque(unsigned int aleatorio);

void  abajo (void);
void  arriba (void);
void izquierda( void);
void derecha( void);

void crash(unsigned char pos,unsigned char posbloquey);

void subir(unsigned int imin,unsigned int imax,unsigned int omin,unsigned int omax,unsigned int color1,unsigned int color2);

#endif
