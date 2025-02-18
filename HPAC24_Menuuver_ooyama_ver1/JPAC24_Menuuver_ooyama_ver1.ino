
//HPAC24(REBORNⅢ)操縦用プログラム
//作成者：航空宇宙工学科　大山
//2024/06/27作成
//2024/06/20 Vr1.1 渡邉
//MAtmega2560との通信

#include <VarSpeedServo.h>

VarSpeedServo Ladder;    //垂直尾翼(右側)
VarSpeedServo Elevator;  //水平尾翼(左側)

const int Joy_Ladder = A2;    //A0をJoy_Ladderに割り当て
const int Joy_Elevator = A0;  //A1をJoy_Elevatorに割り当て

const int Servo_Ladder = PD4;    //D3をServo_Ladderに割り当て
const int Servo_Elevator = PD3;  //D4をServo_Elevatorに割り当て

const bool servo_Bat = PC3;      //サーボバッテリの残量確認ピン
const bool servo_Bat_LED = PD2;  //サーボバッテリの低残量Indicator

const float OBC_Bat = PC4;     //OBCバッテリー残量確認用アナログピン
const bool OBC_Bat_LED = PD1;  //OBCバッテリの低残量Indicator
float OBC_Bat_val;

float Ladder_val;        //Joyステックで入力される(垂直)
float Elevator_val;      //Joyステックで入力される(水平)
float Ladder_val_new;    //垂直
float Elevator_val_new;  //水平

float trim_Ladder;    //垂直
float trim_Elevator;  //水平


//以下、6/20渡邉追加
int CS = 2;
volatile boolean sta = false;

void flag(){
  sta = true;
}


void setup() {
  Serial.begin(9600);
  pinMode(Servo_Ladder, OUTPUT);
  pinMode(Servo_Elevator, OUTPUT);
  pinMode(Joy_Ladder, INPUT);
  pinMode(Joy_Elevator, INPUT);

  pinMode(servo_Bat, INPUT);
  pinMode(servo_Bat_LED, OUTPUT);
  pinMode(OBC_Bat, INPUT);
  pinMode(OBC_Bat_LED, OUTPUT);

  Ladder.attach(Servo_Ladder);      //Servo_LadderをLadderに割り当て
  Elevator.attach(Servo_Elevator);  //Servo_ElevatorをElevatorに割り当て

  delay(1000);

  Ladder.write(90, 40);      //
  Elevator.write(90, 20);  //

  trim_Ladder = 3;//中央オフセット:3
  trim_Elevator = -16;//中央オフセット:〇〇

  //attachInterrupt(digitalPinToInterrupt(CS), flag, FALLING);

  delay(1000);
}


void loop() {
  ///////ジョイステックからの入力を変数に格納//////
  Ladder_val = analogRead(Joy_Ladder); //アナログ値を読み取り(垂直)
  Elevator_val = analogRead(Joy_Elevator); //アナログ値を読み取り(水平)

///////ジョイステック無操作時のノイズを拾わないための設定///////
  if((Ladder_val >= 500) && (Ladder_val <= 524)){
    Ladder_val = 512;
  }

  if((Elevator_val >= 500) && (Elevator_val <= 524)){
    Elevator_val = 512;
  }

///////取得したアナログ値をMAP関数にてサーボに出力する元祖データに変換///////
Ladder_val = map(Ladder_val, 0, 1023, 39.87, 140.13); //垂直(66,114)or(114,66),渡邉校正値(56.58,123.42)
Elevator_val = map(Elevator_val, 0, 1023, 56.58, 123.42); //水平(115,65)or(65,115)

///////トリム調整処理///////
if(digitalRead(9) == LOW){//垂直尾翼　右トリム該当9
  while(digitalRead(9)==LOW){}
    trim_Ladder = trim_Ladder - 1.04;    
}

if(digitalRead(10) == LOW){//垂直尾翼 左トリム10
  while(digitalRead(10)==LOW){}
    trim_Ladder = trim_Ladder + 1.04; 
}

if(digitalRead(8) == LOW){//トリムリセット
  while(digitalRead(8)==LOW){}
    trim_Ladder = 3;//垂直初期Trimに設定
    trim_Elevator = 0.0;//水平初期Trimに設定
}

if(digitalRead(7) == LOW){//水平機首上げトリム6
  while(digitalRead(7)==LOW){}
    trim_Elevator = trim_Elevator - 1.04;//トリム込みで97度以上なら0.72度ずつ動かす  
}

if(digitalRead(6) == LOW){//水平機首下げトリム7
  while(digitalRead(6)==LOW){}
    trim_Elevator = trim_Elevator + 1.04;//トリム込みで89度以上なら0.72度ずつ動かす 
}

///////ジョイステックとトリム値を足し合わせ///////
Ladder_val_new = Ladder_val + trim_Ladder;      // 垂直尾翼用データ形成
Elevator_val_new = Elevator_val + trim_Elevator;//水平尾翼用データ形成

if(Ladder_val_new >= 140.13){
  Ladder_val_new = 140.13;
}

if(Ladder_val_new <= 39.87){
  Ladder_val_new = 39.87;
}

if(Elevator_val_new >= 123.42){
  Elevator_val_new = 123.42;
}

if(Elevator_val_new <= 56.58){
  Elevator_val_new = 56.58;
}

///////上記で計算した値をサーボに送信///////
Elevator.write(Elevator_val_new,20);    // 速度40設定 送信(エレベータ)
Ladder.write(Ladder_val_new,40);    // 速度40設定 送信(ラダー)

//サーボバッテリ残量確認フェーズ
  if(digitalRead(servo_Bat)==HIGH){
    digitalWrite(servo_Bat_LED,HIGH);
  }else{
    digitalWrite(servo_Bat_LED,LOW);
  }

//OBCバッテリ残量確認フェーズ
  OBC_Bat_val = analogRead(OBC_Bat);
  if(OBC_Bat_val <= 716){
    digitalWrite(OBC_Bat_LED,HIGH);
  }else{
    digitalWrite(OBC_Bat_LED,LOW);
  }

//Atmega2560へのデータ送信フェーズ

    String TX_Elevator_val_new = String(Elevator_val_new);
    String TX_Ladder_val_new = String(Ladder_val_new);

    Serial.print(TX_Elevator_val_new);
    Serial.print(",");
    Serial.println(TX_Ladder_val_new);
    


  delay(100); //delayは必ず50以上入れること。動作が非常に不安定になる
}