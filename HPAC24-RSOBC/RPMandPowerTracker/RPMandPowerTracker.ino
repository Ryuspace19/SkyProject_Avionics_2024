/*
2024/5/11作成
作成者：帝京大学 航空宇宙工学科 鶴田研究室所属 B4 渡邉龍一郎
5/11：コア0でのデータ取得まで完了。コア1で計算する処理が未着手。コア間のデータ送受信はグローバル変数でやり取りすれば解決か？
5/14：

*/


//ひずみ計測関連////////////////////
#define ADC0  A0


float STRAIN_Vol = 0.000000;                      //ゲージ出力電圧
float STRAIN , STRAIN_offset = 0.000000;          // 
float A0_1 , A_sum = 0;            //
float Torque;                                     //トルク値格納変数
float slope = 123.456;                                      //スロープ値(ε-N.mの傾き)
float STARIN_Vol;
float radpersec = 0.000;
int Power = 0;

///////////////////////////////////

//角速度センサ関連//////////////////
#include<Wire.h>
// BMX055 加速度センサのI2Cアドレス  
#define Addr_Accl 0x19  // (JP1,JP2,JP3 = Openの時)
// BMX055 ジャイロセンサのI2Cアドレス
#define Addr_Gyro 0x69  // (JP1,JP2,JP3 = Openの時)
// BMX055 磁気センサのI2Cアドレス
#define Addr_Mag 0x13   // (JP1,JP2,JP3 = Openの時

// センサーの値を保存するグローバル変数
float xGyro = 0.00;
float yGyro = 0.00;
float zGyro = 0.00;

// rpm計算に使用するグローバル変数
int rpm , rpm_sum , true_rpm , rpm_old = 0;
////////////////////////////////////


void setup() {
  pinMode(ADC0,INPUT);

  analogReadResolution(12);

  // Wire(Arduino-I2C)の初期化
  Wire1.setSDA(6);
  Wire1.setSCL(7);
  Wire1.begin();
  //BMX055 初期化
  BMX055_Init();
/*
  for(int i=0 ; i <= 10 ; i++){
    A0_1 = analogRead(ADC0);      //Analog値取得

    if(A0_1 < 0){
      A0_1 = A0_1 * -1;         //絶対値化処理
    }

    A_sum += A0_1;               //差分を合計していく

    delay(4);
  }

  STRAIN_Vol = A_sum / 10;        //出力電圧の平均を求める

  STRAIN_offset = STARIN_Vol;    //ひずみ値のオフセット設定

  //STRAIN_offset = STRAIN_offset * 0.000001;      //単位換算→μ
*/
}

void setup1() {
  // デバッグ用シリアル通信は9600bps
  Serial1.setTX(0);
  Serial1.setRX(1);
  Serial1.begin(115200);

}

void loop() {


  for(int i=0 ; i <= 10 ; i++){
    A0_1 = analogRead(ADC0);      //Analog値取得

    BMX055_Gyro();

    rpm = zGyro / 6;              //deg/s→rpm変換

    if(A0_1 < 0){
      A0_1 = A0_1 * -1;         //絶対値化処理
    }

    A_sum += A0_1;               //差分を合計していく
    rpm_sum += rpm;                //計測したrpmを合計していく

    delay(4);
  }

  STRAIN_Vol = A_sum / 10;        //出力電圧の平均を求める
  true_rpm = rpm_sum /10;         //回転数の平均を求める
  rpm_sum = 0;
  A_sum = 0;

  

}

void loop1() {


  STRAIN = STARIN_Vol;         //ひずみ値に計算する

  //Torque = (STRAIN-STRAIN_offset)/slope;    //トルクを算出
  Torque = 9.52*STRAIN-6935.3;

  radpersec = true_rpm * (3.14/30);         //rpm→rad/s変換

  Power = Torque * radpersec;               //Power計算(トルク*角速度(rad/s))

  Serial1.print("P:");
  Serial1.print(Power,DEC);
  Serial1.print(",");
  Serial1.print("R:");
  Serial1.print(true_rpm,DEC);
  Serial1.print(",");
  Serial1.print("S:");
  Serial1.println(STRAIN);
  //Serial1.print(",");
  //Serial1.print("O:");
  //Serial1.println(STRAIN_offset);
  
  delay(50);

}


//=====================================================================================//
void BMX055_Init()
{
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Gyro);
  Wire1.write(0x0F);  // Select Range register
  Wire1.write(0x00);  // Full scale = +/- 2000 degree/s
  Wire1.endTransmission();
  delay(10);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Gyro);
  Wire1.write(0x10);  // Select Bandwidth register
  Wire1.write(0x03);  // ODR = 400 Hz
  Wire1.endTransmission();
  delay(10);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Gyro);
  Wire1.write(0x11);  // Select LPM1 register
  Wire1.write(0x00);  // Normal mode, Sleep duration = 2ms
  Wire1.endTransmission();
  delay(10);
}
//=====================================================================================//
void BMX055_Gyro()
{
  unsigned int data[6];
  for (int i = 0; i < 6; i++)
  {
    Wire1.beginTransmission(Addr_Gyro);
    Wire1.write((2 + i));    // Select data register
    Wire1.endTransmission();
    Wire1.requestFrom(Addr_Gyro, 1);    // Request 1 byte of data
    // Read 6 bytes of data
    // xGyro lsb, xGyro msb, yGyro lsb, yGyro msb, zGyro lsb, zGyro msb
    if (Wire1.available() == 1)
      data[i] = Wire1.read();
  }
  // Convert the data
  xGyro = (data[1] * 256) + data[0];
  if (xGyro > 32767)  xGyro -= 65536;
  yGyro = (data[3] * 256) + data[2];
  if (yGyro > 32767)  yGyro -= 65536;
  zGyro = (data[5] * 256) + data[4];
  if (zGyro > 32767)  zGyro -= 65536;

  xGyro = xGyro * 0.0038; //  Full scale = +/- 125 degree/s
  yGyro = yGyro * 0.0038; //  Full scale = +/- 125 degree/s
  zGyro = zGyro * 0.061; //  Full scale = +/- 2000 degree/s
}
//=====================================================================================//
