#include <Servo.h>

// 5 servo objects can be created on most boards
Servo finger1; // create servo object to control a servo
Servo finger2; 
Servo finger3;
Servo finger4;
Servo finger5;

int pos = 0;    // variable to store the servo position

// split string vars
String strs[20];
String temp;
int StringCount = 0;
int val;

void setup() 
{
  finger1.attach(5);  // thumb
  finger2.attach(4); // pointer finger
  finger3.attach(3); // middle finger
  finger4.attach(2); //ring finger
  finger5.attach(6); // pinky
  Serial.begin(9600);
  while (!Serial);
}

void loop()
{
  if (Serial.available())
  {
    // grab positions from serial
    String str = Serial.readString();
    Serial.println(str);

    // Split the string into substrings
    while (str.length() > 0)
    {
      int index = str.indexOf(' ');
      if (index == -1) // No space found
      {
        strs[StringCount++] = str;
        break;
      }
      else
      {
        strs[StringCount++] = str.substring(0, index);
        str = str.substring(index+1);
      }
    }

    // Show the resulting substrings
    for (int i = 0; i < StringCount; i++)
    {
      Serial.print(i);
      Serial.print(": \"");
      Serial.print(strs[i]);
      Serial.println("\"");
    }
    StringCount = 0;  //go back to first string for next round

    // move finger
    moveFinger(strs[0], finger1, 1);
    moveFinger(strs[1], finger2, 0);
    moveFinger(strs[2], finger3, 0);
    moveFinger(strs[3], finger4, 0);
    moveFinger(strs[4], finger5, 1);

    delay(100);
  }
}

void moveFinger1(Servo finger){
  for (pos = 0; pos <= 200; pos += 1) { // goes from 0 degrees to 180 degrees
    finger.write(pos);
    delay(4);                       // waits 15ms for the servo to reach the position
  }   
}

void moveFinger2(Servo finger){
  for (pos = 200; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    finger.write(pos);              // tell servo to go to position in variable 'pos'
    delay(4);                  // waits 15ms for the servo to reach the position
  }
}

void moveFinger(String s, Servo finger, int flip){
  String temp = s;
  int val = s.toInt();

  // workaround if its wrong wiring 
  if (flip){
    if (val == 1){
      val = 2;
    } else {
      val = 1;
    }
  }

  if (val == 1) {
    moveFinger1(finger);
  } else {
    moveFinger2(finger);
  }
}
