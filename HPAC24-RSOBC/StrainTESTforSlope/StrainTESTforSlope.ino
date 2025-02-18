/*
スロープ値計算用ひずみ値計測プログラム
2024/5/14作成
作成者：帝京大学 航空宇宙工学科 鶴田研究室所属 B4 渡邉龍一郎
5/14：

*/

//ひずみ計測関連////////////////////
#define ADC3  26
#define ADC2  27

const float E_sys = 3.3;                          //ゲージ印加電圧
float Ks = 2.13;                                  //Ksはゲージ率。ゲージのデータシートを要確認
float STRAIN_Vol = 0.000000;                      //ゲージ出力電圧
float STRAIN , STRAIN_offset = 0.000000;          // 
float A3_1 , A2_1 , A_low , A_sum = 0;            //
float Torque;                                     //トルク値格納変数
float slope = 123.456;                                      //スロープ値(ε-N.mの傾き)
float STARIN_Vol;
//float radpersec = 0.000;
//int Power = 0;

struct repeating_timer st_timer;
bool timer_flag = false;

bool Timer(struct repeating_timer *t) {
  timer_flag = true;
  return true;
}

void setup() {

  pinMode(ADC3,INPUT);
  pinMode(ADC2,INPUT);

  // デバッグ用シリアル通信は115200bps
  Serial1.setTX(0);
  Serial1.setRX(1);
  Serial1.begin(115200);

  add_repeating_timer_us(1000000, Timer, NULL, &st_timer);    //us指定(1000000us=1s)

}

void loop() {


  for(int i=0 ; i <= 10 ; i++){
    A3_1 = analogRead(ADC3);      //Analog値取得
    A2_1 = analogRead(ADC2);      //Analog値取得

    A_low = A3_1 - A2_1;          //差分計算

    if(A_low < 0){
      A_low = A_low * -1;         //絶対値化処理
    }

    A_sum += A_low;               //差分を合計していく

    delay(4);
  }

  STRAIN_Vol = A_sum / 10;        //出力電圧の平均を求める
  A_sum = 0;
  STRAIN = STARIN_Vol/(Ks * E_sys);         //ひずみ値に計算する
  STRAIN = STRAIN * 0.000001;

  if(timer_flag == true){
    Serial1.print("Strain[μ],");
    Serial1.println(STRAIN);
    timer_flag = false;
  }


  

}
