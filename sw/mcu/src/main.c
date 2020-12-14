//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

#include "SI_C8051F850_Register_Enums.h"
#include "SI_C8051F850_Defs.h"

//-----------------------------------------------------------------------------
// Defines
//-----------------------------------------------------------------------------

#define FREQ_TUNE    7990000
#define FREQ_MAX     100000
#define FREQ_MIN     100
#define FREQ_STEP    100
#define DUTY_MAX     100000
#define DUTY_MIN     100
#define DUTY_STEP    100
#define PHASE_MAX    360000
#define PHASE_MIN    0
#define PHASE_STEP   1000



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

volatile U32 a_fall;
volatile U32 b_rise;
volatile U32 b_fall;
volatile U32 timer;
volatile U32 period;


volatile U32 a_duty;
volatile U32 b_duty;
volatile U32 a_b_phase;
volatile U32 freq;

volatile U32 convert;
volatile U8 state;

//-----------------------------------------------------------------------------
// Main Routine
//-----------------------------------------------------------------------------

void main (void){    
   //--------------------------------------------------------------------------
   // Variables
   //-------------------------------------------------------------------------- 
   U32 i;
   U8 send;
   U8 cmd;
   //--------------------------------------------------------------------------
   // Initialise
   //--------------------------------------------------------------------------
  
   cmd    = ' ';  // Init command
   LED0   = 0;
   LED1   = 0;
   timer  = 0; 
   state  = 0;
   freq   = FREQ_MIN; 
   
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
         cmd=uartRx();
      }
     
      switch(cmd){
         case 'q':   freq += FREQ_STEP;  
                     if(freq > FREQ_MAX)  
                        freq = FREQ_MAX; 
                     break;
         case 'a':   freq -= FREQ_STEP;  
                     if(freq < FREQ_MIN)  
                        freq = FREQ_MIN; 
                     break;
         case 'w':   a_duty += DUTY_STEP;  
                     if(a_duty > DUTY_MAX)  
                        a_duty = DUTY_MAX;
                     break;
         case 's':   a_duty -= DUTY_STEP;  
                     if(a_duty < DUTY_MIN)  
                        a_duty = DUTY_MIN;
                     break; 
         case 'e':   b_duty += DUTY_STEP;  
                     if(b_duty > DUTY_MAX)  
                        b_duty = DUTY_MAX;
                     break;
         case 'd':   b_duty -= DUTY_STEP;  
                     if(b_duty < DUTY_MIN)  
                        b_duty = DUTY_MIN;
                     break;
         case 'r':   a_b_phase += PHASE_STEP; 
                     if(a_b_phase > PHASE_MAX) 
                        a_b_phase = PHASE_MAX;
                     break;
         case 'f':   a_b_phase -= PHASE_STEP; 
                     if(a_b_phase < PHASE_MIN) 
                        a_b_phase = PHASE_MIN;
                     break;
         case ' ':   freq      = FREQ_MIN;
                     a_duty    = DUTY_MIN;
                     b_duty    = DUTY_MIN;
                     a_b_phase = PHASE_MIN; 
                     break; 
      } 
      
      // Calculate timer numbers   
      if(0 != cmd){
         period = (U32)((float)FREQ_TUNE/(float)freq); 
         a_fall = (U32)(((float)period*((float)a_duty)/DUTY_MAX));
         b_rise = (U32)(((float)period*((float)a_b_phase)/PHASE_MAX));
         b_fall = b_rise + (U32)(((float)period*((float)b_duty)/DUTY_MAX));
         b_fall %= period;
      }

      // Need another Rx to update
      cmd = 0;

   }
}

//-----------------------------------------------------------------------------
// Interrupts
//-----------------------------------------------------------------------------

INTERRUPT (TIMER2_ISR, TIMER2_IRQn){           
   // Global time keeper
   timer++; 
   timer %= period; 
   // Drive outputs
   //    - A always goes high at time 0
   if(timer == 0)       PIS0=1;
   if(timer == a_fall)  PIS0=0;
   if(timer == b_rise)  PIS1=1;
   if(timer == b_fall)  PIS1=0; 
   TMR2CN &= ~TMR2CN_TF2H__SET;
}

INTERRUPT (TIMER3_ISR, TIMER3_IRQn){           
   U8 send; 
   switch(state){
      case 0:  uartTx('\n');                 break;
      case 1:  uartTx('\r');                 break; 
      case 2:  uartTx('F');                  break;
      case 3:  uartTx('r');                  break;
      case 4:  uartTx('e');                  break;
      case 5:  uartTx('q');                  break;
      case 6:  uartTx('(');                  break;
      case 7:  uartTx('H');                  break;
      case 8:  uartTx('z');                  break;
      case 9:  uartTx(')');                  break;
      case 10: uartTx('=');                  break; 
      case 11: convert=freq;
               convert=uartTxPos(convert,6); break;
      case 12: convert=uartTxPos(convert,5); break;
      case 13: convert=uartTxPos(convert,4); break;
      case 14: convert=uartTxPos(convert,3); break;
      case 15: uartTx('.');                  break;  
      case 16: convert=uartTxPos(convert,2); break;
      case 17: convert=uartTxPos(convert,1); break;   
      case 18: convert=uartTxPos(convert,0); break;
      case 19: uartTx(',');                  break;
      case 20: uartTx('A');                  break;
      case 21: uartTx(' ');                  break;
      case 22: uartTx('D');                  break;
      case 23: uartTx('u');                  break;
      case 24: uartTx('t');                  break;
      case 25: uartTx('y');                  break;
      case 26: uartTx('(');                  break; 
      case 27: uartTx('%');                  break;
      case 28: uartTx(')');                  break; 
      case 29: uartTx('=');                  break; 
      case 30: convert=a_duty;
               convert=uartTxPos(convert,5); break;
      case 31: convert=uartTxPos(convert,4); break;
      case 32: convert=uartTxPos(convert,3); break;
      case 33: uartTx('.');                  break;
      case 34: convert=uartTxPos(convert,2); break;
      case 35: convert=uartTxPos(convert,1); break;
      case 36: convert=uartTxPos(convert,0); break;    
      case 37: uartTx(',');                  break;
      case 38: uartTx('B');                  break;
      case 39: uartTx(' ');                  break;
      case 40: uartTx('D');                  break;
      case 41: uartTx('u');                  break;
      case 42: uartTx('t');                  break;
      case 43: uartTx('y');                  break;
      case 44: uartTx('(');                  break; 
      case 45: uartTx('%');                  break;
      case 46: uartTx(')');                  break; 
      case 47: uartTx('=');                  break; 
      case 48: convert=b_duty;
               convert=uartTxPos(convert,5); break;
      case 49: convert=uartTxPos(convert,4); break;
      case 50: convert=uartTxPos(convert,3); break;
      case 51: uartTx('.');                  break;
      case 52: convert=uartTxPos(convert,2); break;
      case 53: convert=uartTxPos(convert,1); break;
      case 54: convert=uartTxPos(convert,0); break;
      case 55: uartTx(',');                  break;
      case 56: uartTx('A');                  break;
      case 57: uartTx('-');                  break;
      case 58: uartTx('B');                  break;
      case 59: uartTx(' ');                  break;
      case 60: uartTx('P');                  break;
      case 61: uartTx('h');                  break;
      case 62: uartTx('a');                  break; 
      case 63: uartTx('s');                  break;
      case 64: uartTx('e');                  break; 
      case 65: uartTx('(');                  break; 
      case 66: uartTx('d');                  break;
      case 67: uartTx('e');                  break; 
      case 68: uartTx('g');                  break; 
      case 69: uartTx(')');                  break;  
      case 70: uartTx('=');                  break; 
      case 71: convert=a_b_phase;
               convert=uartTxPos(convert,5); break;
      case 72: convert=uartTxPos(convert,4); break;
      case 73: convert=uartTxPos(convert,3); break;
      case 74: uartTx('.');                  break;
      case 75: convert=uartTxPos(convert,2); break;
      case 76: convert=uartTxPos(convert,1); break;
      case 77: convert=uartTxPos(convert,0); break;
      case 78: uartTx('\r');  
               state = 1;
               break;
   }
   state++; 
   TMR3CN &= ~TMR3CN_TF3H__SET;
}


//-----------------------------------------------------------------------------
// UART
//-----------------------------------------------------------------------------

U32 uartTxPos(U32 num, U8 pos){
   U32 scale;
   U8 i;
   switch(pos){
      case 0:  scale = 1; break;
      case 1:  scale = 10; break;
      case 2:  scale = 100; break;
      case 3:  scale = 1000; break;
      case 4:  scale = 10000; break;
      case 5:  scale = 100000; break;
      case 6:  scale = 1000000; break;
      case 7:  scale = 10000000; break;
      case 8:  scale = 100000000; break;
      case 9:  scale = 1000000000; break;
      case 10: scale = 10000000000; break;
      default: scale = 0; break;
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
