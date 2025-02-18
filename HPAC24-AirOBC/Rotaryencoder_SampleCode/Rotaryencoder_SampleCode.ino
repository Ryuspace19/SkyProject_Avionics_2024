/*
2024/06/14作成
6/14:Ver1.0
ロータリーエンコーダの1秒間での回転数をシリアル出力するソースコード
使用するにはMsTimer2.hというライブラリをダウンロードする必要がある
1秒間に1回の出力だが、0.5秒とかに変更したい場合はsetup内のMsTimer2の呼び出し設定部分の数値を500に変更し、44行目の計算を/50にしてください

*/

#include<MsTimer2.h>

const byte REpin = 2;
volatile byte state = LOW;
int REcount = 0;
int RPS = 0;

volatile byte timestate = LOW;

void blink(){
  state = HIGH; //エンコーダがLOWになったらフラグを立てる
}

void flash(){
  timestate = HIGH; //1秒ごとにフラグを立てる
}

void setup() {
  Serial.begin(115200); //9600でも大丈夫です
  pinMode(REpin,INPUT); //REpinを入力用に設定
  attachInterrupt(digitalPinToInterrupt(REpin),blink,FALLING);  //REpinに入ってくる信号がHIGHからLOWにFALLINGしたときにblink関数を呼び出す
  MsTimer2::set(1000, flash); // 1000msごとにflash関数呼び出し
  MsTimer2::start();
}

void loop() {

  if(state == HIGH){
    REcount = REcount + 1;  //REcountという変数に1づつ追加していく
    state = LOW;  //フラグを下げる
  }

  if(timestate == HIGH){
    RPS = REcount / 100;  //タイマー割り込みを1秒ごとに行うなら100で割る。0.5秒ごとなら50で割る
    REcount = 0;
    Serial.print("Rotation Count : ");
    Serial.println(RPS);  //RPS:1秒間での回転数
    timestate = LOW;  //フラグを下げる
  }
  
}
