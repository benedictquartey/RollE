
    #include <Wire.h>
    #include <LiquidCrystal_I2C.h>
    
    
    #define I2C_ADDR    0x3F // <<- Add your address here.
    #define Rs_pin  0
    #define Rw_pin  1
    #define En_pin  2
    #define BACKLIGHT_PIN 3
    #define D4_pin  4
    #define D5_pin  5
    #define D6_pin  6
    #define D7_pin  7
    




 String Agentname="RollE_MKII";
LiquidCrystal_I2C lcd(I2C_ADDR,En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin);


//joystick definitions
int joySteerY = A0;
int joyThrottleX = A1;
int stopBtn = 8;

int joyVal;


void setup() {
  // put your setup code here, to run once:
 lcd.begin (20,4); // <<-- our LCD is a 20x4, change for your LCD if needed
    
    // LCD Backlight ON
    lcd.setBacklightPin(BACKLIGHT_PIN,POSITIVE);
    lcd.setBacklight(HIGH);

//lcd intro sequence
    lcd.setCursor (5,1); // go to fith column of 2nd line
    lcd.print("Connecting ");
    lcd.setCursor (7,2); // go to fith column of 2nd line
    
    for(int i=0; i<3;i++){
           lcd.print(". ");
           delay(1000);
      }
     lcd.clear();
//end of intro

    lcd.home (); // go home on LCD
    lcd.setCursor(3,0);
    lcd.print("* "+Agentname+" * ");  
    lcd.setCursor (0,1); // go to fith column of 2nd line
  lcd.print("--------------------");
    lcd.setCursor (0,2); // go to start of 3nd line
    lcd.print("Steer:");
     lcd.setCursor (0,3); 
    lcd.print("Throttle:");
Serial.begin(9600);

  pinMode(stopBtn, INPUT); //set btn pin as input
  pinMode(stopBtn, INPUT_PULLUP); //instantiate pullup resistor on button
}


void loop() {
  // put your main code here, to run repeatedly:

  if (digitalRead(stopBtn)==HIGH){
joyVal = analogRead(joyThrottleX);
//float throttle = map(joyVal,0,1023,0,180); // map sensor reading to range -1 to 1
float throttle = range_map(joyVal,0,1023,1,-1);
Serial.print("Throttle:  ");
Serial.print(throttle);
Serial.println(':'); //end symbol

lcd.setCursor (10,3);
lcd.print(throttle);

joyVal = analogRead(joySteerY);
//float steer = map(joyVal,0,1023,0,180); // map sensor reading to range -1 to 1
float steer = range_map(joyVal,0,1023,1,-1);
Serial.print("Steering: ");
Serial.print(steer);
Serial.println(':');//end symbol

lcd.setCursor (7,2);
lcd.print(steer);}
   if(digitalRead(stopBtn)==LOW){
    stopControl();}
}


float range_map(int val , int X_min,int X_max, int Y_min, int Y_max){
  int X_range = X_max-X_min;
  int Y_range = Y_max-Y_min;
  float XY_ratio = X_range/Y_range;
  float y=((val - X_min)/XY_ratio + Y_min)/1;
  return y;
  }


  void stopControl(){
    Serial.print("Control: ");
    Serial.print("stopRec");
    Serial.println(':');
    lcd.clear();
    //lcd stop control sequence
    lcd.setCursor (5,1); // go to fith column of 2nd line
    lcd.print(" Stopped");
    lcd.setCursor (7,2); // go to fith column of 2nd line
    
    for(int i=0; i<3;i++){
           lcd.print(". ");
           delay(1000);
      }
     lcd.clear();
//end of sequence

     //lcd reconnecting sequence
    lcd.setCursor (4,1); // go to fith column of 2nd line
    lcd.print("Reconnecting ");
    lcd.setCursor (7,2); // go to fith column of 2nd line
    
    for(int i=0; i<3;i++){
           lcd.print(". ");
           delay(1000);
      }
     lcd.clear();
//end of sequence

//default lcd annotations

    lcd.home (); // go home on LCD
    lcd.setCursor(3,0);
    lcd.print("* "+Agentname+" * ");  
    lcd.setCursor (0,1); // go to fith column of 2nd line
  lcd.print("--------------------");
    lcd.setCursor (0,2); // go to start of 3nd line
    lcd.print("Steer:");
     lcd.setCursor (0,3); 
    lcd.print("Throttle:");

    }
