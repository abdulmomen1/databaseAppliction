#include <Servo.h>
#define THRESHOLD 100
#define DTIME 50
#define SENSOR_TL 3
#define SENSOR_TR 1
#define SENSOR_BL 0
#define SENSOR_BR 2

#define HORIZ_LIMIT 160
#define VERT_LIMIT 160

Servo horiz ;
Servo vert ;
int horizpos = HORIZ_LIMIT / 2;
int vertpos =  VERT_LIMIT / 2;

void setup(){
  Serial.begin(9600);
  horiz.attach(9);
  vert.attach(10);
  //vert.write(90);
 // horiz.write(90);  
  delay(100);
}

void loop(){
    
  track();
  //delay(DTIME);


}
void track(){

    int tl = analogRead(SENSOR_TL) ;
    int tr = analogRead(SENSOR_TR) ;
    int bl = analogRead(SENSOR_BL) ;
    int br = analogRead(SENSOR_BR) ;
    int avrege_top = (tl + tr) / 2 ;
    int avrege_down = (bl + br) / 2 ;
    int avrege_left = (tl + bl) / 2 ;
    int avrege_rigth = (tr + br) / 2 ;
    
    
    int dif_vert = avrege_top  - avrege_down ;
    int dif_horz = avrege_left - avrege_rigth ;
    
    
    if ( ((-1 * THRESHOLD) <= dif_vert) && (dif_vert <= THRESHOLD)){
       vert.detach();
       } 
     else {
        vert.attach(10);
        
         if (avrege_top > avrege_down)
         {
           vertpos = --vertpos ;
           if (vertpos > VERT_LIMIT)
           {
                vert.detach();
                vertpos = VERT_LIMIT;
            }
         }
        else if ( avrege_top < avrege_down)
        {
          vertpos = ++vertpos;
          if (vertpos < 0)
          { 
            vert.detach();
             vertpos = 0;
          }
        }
        else if ( avrege_top == avrege_down)
        {
          }
       vert.write(vertpos);
        }
    
if ( ((-1*THRESHOLD) <= dif_horz) && (dif_horz <= THRESHOLD)){
       horiz.detach();
       } 
     else {
        horiz.attach(9);
        
         if (avrege_left > avrege_rigth)
         {
           horizpos = --horizpos;
           if (horizpos < 0)
           {
                horiz.detach();
                horizpos = 0;
            }
         }
        else if ( avrege_left < avrege_rigth  )
        {
          horizpos = ++horizpos;
          if (horizpos > HORIZ_LIMIT)
          { 
            horiz.detach();
             horizpos = HORIZ_LIMIT;
          }
        }
        else if ( avrege_left == avrege_rigth)
        {
          }
       horiz.write(horizpos);
        }
    
  delay(DTIME);

}
