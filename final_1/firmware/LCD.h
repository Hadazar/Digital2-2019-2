#ifndef LCD_H
#define LCD_H

#include <stdio.h>
#include <generated/csr.h>

#define M 14
#define N 13
typedef int Matriz [M][M];

void lcd_config(void);

void lcd_inic(void);

void lcd_write( unsigned char rs, unsigned int info);  //escribe pixel

void dib_cua(unsigned int Xmin,unsigned int Ymin,unsigned int Xmax,unsigned int ymax,unsigned int color); 
void dib_tiles(unsigned int Xmin,unsigned int Ymin,Matriz matris); //dibuja tiles

void busy_wait(unsigned int ds);



#endif
