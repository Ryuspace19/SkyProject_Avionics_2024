
/*
スロープ値計算用ひずみ値計測プログラム
2024/5/14作成
作成者：帝京大学 航空宇宙工学科 鶴田研究室所属 B4 渡邉龍一郎
5/14：

*/

//ひずみ計測関連////////////////////
#define ADC0  A0
  
float A0_1 = 0.00;       

void setup() {

  pinMode(ADC0,INPUT);

  analogReadResolution(12);

  // デバッグ用シリアル通信は115200bps
  Serial1.setTX(0);
  Serial1.setRX(1);
  Serial1.begin(115200);

}

void loop() {

    A0_1 = analogRead(ADC0);      //Analog値取得
    Serial1.println(A0_1);

  delay(50);

}