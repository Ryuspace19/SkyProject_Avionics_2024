/*
HPAC24 MainOBC-GPS検証用コード
作成日2024/02/19
制作者：渡邉
参考記事
https://how2electronics.com/how-to-interface-quectel-l80-gps-module-with-arduino/

メモ
2024/02/19：GPSが信号受信しているか確認するために、受信したらLEDを点滅させるコードに改編
*/

#include <TinyGPS++.h>

long lat, lon;

TinyGPSPlus gps;
 
void setup()
{
  Serial.begin(9600); // connect gps sensor
  Serial1.begin(9600);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
}
 
void loop()
{
  while (Serial.available())     // check for gps data
  {
    digitalWrite(22, HIGH);
    digitalWrite(23, HIGH);
    digitalWrite(24, HIGH);

    if (gps.encode(Serial.read()))   // encode gps data
    {
      Serial1.print("SATS: ");
      Serial1.println(gps.satellites.value());
      Serial1.print("LAT: ");
      Serial1.println(gps.location.lat(), 6);
      Serial1.print("LONG: ");
      Serial1.println(gps.location.lng(), 6);
      Serial1.print("ALT: ");
      Serial1.println(gps.altitude.meters());
      Serial1.print("SPEED: ");
      Serial1.println(gps.speed.mps());
 
      Serial1.print("Date: ");
      Serial1.print(gps.date.day()); Serial.print("/");
      Serial1.print(gps.date.month()); Serial.print("/");
      Serial1.println(gps.date.year());
 
      Serial1.print("Hour: ");
      Serial1.print(gps.time.hour()); Serial.print(":");
      Serial1.print(gps.time.minute()); Serial.print(":");
      Serial1.println(gps.time.second());
      Serial1.println("---------------------------");
      delay(500);
      digitalWrite(22, LOW);
      digitalWrite(23, LOW);
      digitalWrite(24, LOW);
      delay(500);
    }
  }
}
