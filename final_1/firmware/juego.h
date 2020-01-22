#ifndef JUEGO_H
#define JUEGO_H

#include "LCD.h"
#include <generated/csr.h>

unsigned int tempo;
unsigned int vuelta;

void juego(unsigned int color);

void pantalladerecha(void);
void pantallasup(void);
void margenes(void);
void nivel1(void);
void preparacion(void);

#endif
