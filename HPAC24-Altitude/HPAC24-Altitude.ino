const int pulsePin = PD0; // センサーのパルス幅出力ピン
long duration;
int distance;
//float fff = 123.4;


void setup() {
  Serial.begin(9600);
  pinMode(pulsePin, INPUT);
}

void loop() {
  duration = pulseIn(pulsePin, HIGH); // パルスの長さを測定
  distance = duration / 58; // 距離をセンチメートルに変換

  if(distance >= 1000){
    distance = 0;
  }
 // String data = String(fff);
  String TX_distance = String(distance);
  Serial.println(TX_distance);
  //Serial.print("1\n");

  delay(10); 
}
