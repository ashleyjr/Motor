//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

#include "SI_C8051F850_Register_Enums.h"
#include "SI_C8051F850_Defs.h"

//-----------------------------------------------------------------------------
// Defines
//-----------------------------------------------------------------------------

#define PSTEP 10

SBIT(LED0, SFR_P1, 0);  
SBIT(LED1, SFR_P1, 1);  
SBIT(PIS0, SFR_P1, 3);  
SBIT(PIS1, SFR_P1, 4);  


//-----------------------------------------------------------------------------
// Prototypes
//-----------------------------------------------------------------------------

U8    uartRx(void);
void  uartTx(U8 tx);
U32   uartTxPos(U32 num, U8 pos);


//-----------------------------------------------------------------------------
// Global Variables
//-----------------------------------------------------------------------------

volatile U32 a_rise;
volatile U32 a_fall;
volatile U32 b_rise;
volatile U32 b_fall;
volatile U32 timer;
volatile U32 period;

volatile U32 convert;
volatile U8 state;

//-----------------------------------------------------------------------------
// Main Routine
//-----------------------------------------------------------------------------

void main (void){    
   //--------------------------------------------------------------------------
   // Variables
   //--------------------------------------------------------------------------
   U32 convert; 
   U32 i;
   U8 send;
   //--------------------------------------------------------------------------
   // Initialise
   //--------------------------------------------------------------------------
   
   LED0   = 0;
   LED1   = 0;
   timer  = 0;
   period = 1000;
   a_rise = 500;
   a_fall = 999;
   b_rise = 500;
   b_fall = 999;
   state  = 0;
   //--------------------------------------------------------------------------
   // Setup micro
   //--------------------------------------------------------------------------
   
   // Disabled watchdog
   WDTCN    = 0xDE;
   WDTCN    = 0xAD;
   // Clock
	CLKSEL   = CLKSEL_CLKSL__HFOSC 	      |     // Use 24.5MHz interal clock
			     CLKSEL_CLKDIV__SYSCLK_DIV_1;      // Do not divide      
   // Setup XBAR         
   P0MDOUT  = P0MDOUT_B4__PUSH_PULL;            // UART output
   P1MDOUT  = P1MDOUT_B0__PUSH_PULL|            // LED 0            
              P1MDOUT_B1__PUSH_PULL;            // LED 1 
              P1MDOUT_B3__PUSH_PULL|            // PISTON 0            
              P1MDOUT_B4__PUSH_PULL;            // PISTON 1
   XBR0     = XBR0_URT0E__ENABLED;              // Route out UART P0.4 
   XBR2     = XBR2_XBARE__ENABLED;
   // UART
	SCON0    |= SCON0_REN__RECEIVE_ENABLED;      // UART rx 
   // Timer 1: UART baud gen 115200 
	CKCON    |= CKCON_T1M__SYSCLK;
	TMOD     |= TMOD_T1M__MODE2;
	TCON     |= TCON_TR1__RUN;  
   TH1      = 0x96;                             // Magic values from datasheet for 115200
	TL1      = 0x96;
   // Timer 2: Counter 10KHz
	TMR2CN   = TMR2CN_TR2__RUN;
   TMR2L    = 0x00;
   TMR2H    = 0xFF;
   TMR2RLL  = 0x00;
   TMR2RLH  = 0xFF;
   // Timer 3: Counter 1KHz
	TMR3CN   = TMR3CN_TR3__RUN;
   TMR3L    = 0x00;
   TMR3H    = 0xF0;
   TMR3RLL  = 0x00;
   TMR3RLH  = 0xF0;
   // Interrupts
	IE       = IE_EA__ENABLED | 
              IE_ET2__ENABLED;
   EIE1     = EIE1_ET3__ENABLED;
   //--------------------------------------------------------------------------
   // Main loop
   //--------------------------------------------------------------------------
   while(1){     
      if(SCON0_RI){
         switch(uartRx()){
            case 'q': if(period != 0xFFFFFFFF){
                        period += PSTEP;
                      }
                      break;
            case 'a': if(period != 0){
                        period -= PSTEP;
                      }
                      break;
            case 'w': if(a_rise != 0xFFFFFFFF){
                        a_rise += PSTEP;
                      }
                      break;
            case 's': if(a_rise != 0){
                        a_rise -= PSTEP;
                      }
                      break;
            case 'e': if(a_fall != 0xFFFFFFFF){
                        a_fall += PSTEP;
                      }
                      break;
            case 'd': if(a_fall != 0){
                        a_fall -= PSTEP;
                      }
                      break;
            case 'r': if(b_rise != 0xFFFFFFFF){
                        b_rise += PSTEP;
                      }
                      break;
            case 'f': if(b_rise != 0){
                        b_rise -= PSTEP;
                      }
                      break;
            case 't': if(a_fall != 0xFFFFFFFF){
                        b_fall += PSTEP;
                      }
                      break;
            case 'g': if(b_fall != 0){
                        b_fall -= PSTEP;
                      }
                      break;
         }

      }
      if(a_rise > period) a_rise = period;
      if(a_fall > period) a_fall = period;
      if(b_rise > period) b_rise = period;
      if(b_fall > period) b_fall = period;
   }
}

//-----------------------------------------------------------------------------
// Interrupts
//-----------------------------------------------------------------------------

INTERRUPT (TIMER2_ISR, TIMER2_IRQn){           
   // Global time keeper
   timer++; 
   timer %= period; 
   if(timer == a_rise)  PIS0=1;
   if(timer == a_fall)  PIS0=0;
   if(timer == b_rise)  PIS1=1;
   if(timer == b_fall)  PIS1=0; 
   TMR2CN &= ~TMR2CN_TF2H__SET;
}

INTERRUPT (TIMER3_ISR, TIMER3_IRQn){           
   U8 send; 
   switch(state){
      case 0:  uartTx('p');                  break;
      case 1:  uartTx('e');                  break;
      case 2:  uartTx('r');                  break;
      case 3:  uartTx('i');                  break;
      case 4:  uartTx('o');                  break;
      case 5:  uartTx('d');                  break; 
      case 6:  convert=period;
               convert=uartTxPos(convert,6); break;
      case 7:  convert=uartTxPos(convert,5); break;
      case 8:  convert=uartTxPos(convert,4); break;
      case 9:  convert=uartTxPos(convert,3); break;
      case 10: convert=uartTxPos(convert,2); break;
      case 11: convert=uartTxPos(convert,1); break;   
      case 12: convert=uartTxPos(convert,0); break;
      case 13: uartTx(',');                 break; 
      case 14: uartTx(' ');                 break;
      case 15: uartTx('a');                  break;
      case 16: uartTx('_');                  break;
      case 17: uartTx('r');                  break;
      case 18: uartTx('i');                  break;
      case 19: uartTx('s');                  break;
      case 20: uartTx('e');                  break; 
      case 21: convert=a_rise;
               convert=uartTxPos(convert,6); break;
      case 22: convert=uartTxPos(convert,5); break;
      case 23: convert=uartTxPos(convert,4); break;
      case 24: convert=uartTxPos(convert,3); break;
      case 25: convert=uartTxPos(convert,2); break;
      case 26: convert=uartTxPos(convert,1); break;   
      case 27: convert=uartTxPos(convert,0); break;
      case 28: uartTx(',');                 break; 
      case 29: uartTx(' ');                 break;
      case 30: uartTx('a');                  break;
      case 31: uartTx('_');                  break;
      case 32: uartTx('f');                  break;
      case 33: uartTx('a');                  break;
      case 34: uartTx('l');                  break;
      case 35: uartTx('l');                  break; 
      case 36: convert=a_fall;
               convert=uartTxPos(convert,6); break;
      case 37: convert=uartTxPos(convert,5); break;
      case 38: convert=uartTxPos(convert,4); break;
      case 39: convert=uartTxPos(convert,3); break;
      case 40: convert=uartTxPos(convert,2); break;
      case 41: convert=uartTxPos(convert,1); break;   
      case 42: convert=uartTxPos(convert,0); break;
      case 43: uartTx(',');                 break; 
      case 44: uartTx(' ');                 break;
      case 45: uartTx('b');                  break;
      case 46: uartTx('_');                  break;
      case 47: uartTx('r');                  break;
      case 48: uartTx('i');                  break;
      case 49: uartTx('s');                  break;
      case 50: uartTx('e');                  break; 
      case 51: convert=b_rise;
               convert=uartTxPos(convert,6); break;
      case 52: convert=uartTxPos(convert,5); break;
      case 53: convert=uartTxPos(convert,4); break;
      case 54: convert=uartTxPos(convert,3); break;
      case 55: convert=uartTxPos(convert,2); break;
      case 56: convert=uartTxPos(convert,1); break;   
      case 57: convert=uartTxPos(convert,0); break;
      case 58: uartTx(',');                 break; 
      case 59: uartTx(' ');                 break;
      case 60: uartTx('b');                  break;
      case 61: uartTx('_');                  break;
      case 62: uartTx('f');                  break;
      case 63: uartTx('a');                  break;
      case 64: uartTx('l');                  break;
      case 65: uartTx('l');                  break; 
      case 66: convert=b_fall;
               convert=uartTxPos(convert,6); break;
      case 67: convert=uartTxPos(convert,5); break;
      case 68: convert=uartTxPos(convert,4); break;
      case 69: convert=uartTxPos(convert,3); break;
      case 70: convert=uartTxPos(convert,2); break;
      case 71: convert=uartTxPos(convert,1); break;   
      case 72: convert=uartTxPos(convert,0); break; 
      case 73: uartTx(13);                 break; 
      case 74: uartTx('\r');                 break;
   }
   state++;
   state %= 75;
   TMR3CN &= ~TMR3CN_TF3H__SET;
}


//-----------------------------------------------------------------------------
// UART
//-----------------------------------------------------------------------------

U32 uartTxPos(U32 num, U8 pos){
   U32 scale;
   U8 i;
   scale = 1;
   for(i=0;i<pos;i++){
      scale *= 10;
   }
   i = num / scale;         
   uartTx('0'+i);    
   scale = num - (i*scale);
   return scale;
}

U8 uartRx(void){
   while(!SCON0_RI);
   SCON0_RI = 0;
   return SBUF0;
}

void uartTx(U8 tx){ 
   SCON0_TI = 0;
   SBUF0 = tx; 
}
