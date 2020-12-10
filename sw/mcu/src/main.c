//-----------------------------------------------------------------------------
// Includes
//-----------------------------------------------------------------------------

#include "SI_C8051F850_Register_Enums.h"
#include "SI_C8051F850_Defs.h"

//-----------------------------------------------------------------------------
// Defines
//-----------------------------------------------------------------------------

SBIT(LED0, SFR_P1, 0);  
SBIT(LED1, SFR_P1, 1);  

//-----------------------------------------------------------------------------
// Prototypes
//-----------------------------------------------------------------------------

U8    uartRx(void);
void  uartTx(U8 tx);

//-----------------------------------------------------------------------------
// Main Routine
//-----------------------------------------------------------------------------

void main (void){    
   
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
   P1MDOUT  = P1MDOUT_B0__PUSH_PULL|            // LED            
              P1MDOUT_B1__PUSH_PULL;            // LED  
   XBR0     = XBR0_URT0E__ENABLED;              // Route out UART P0.4 
   XBR2     = XBR2_WEAKPUD__PULL_UPS_DISABLED | 
              XBR2_XBARE__ENABLED;
   // UART
	SCON0    |= SCON0_REN__RECEIVE_ENABLED;      // UART rx 
   // Timer 1: UART baud gen 115200 
	CKCON    |= CKCON_T1M__SYSCLK;
	TMOD     |= TMOD_T1M__MODE2;
	TCON     |= TCON_TR1__RUN;  
   TH1      = 0x96;                             // Magic values from datasheet for 115200
	TL1      = 0x96;

   //--------------------------------------------------------------------------
   // Initialise
   //--------------------------------------------------------------------------
   
   LED0=0;
   LED1=0;
 
   //--------------------------------------------------------------------------
   // Main loop
   //--------------------------------------------------------------------------
   while(1){
      uartTx('T');
      uartTx('E');
      uartTx('S');
      uartTx('T');
      uartTx('\n');
      uartTx(uartRx());
   }
}

//-----------------------------------------------------------------------------
// UART
//-----------------------------------------------------------------------------

U8 uartRx(void){
   while(!SCON0_RI);
   SCON0_RI = 0;
   return SBUF0;
}

void uartTx(U8 tx){
   SCON0_TI = 0;
   SBUF0 = tx;
   while(!SCON0_TI); 
}
