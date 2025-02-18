//================================================================//
//  AE-BMX055             Seeed XIAO RP2040                       //
//    VCC                    +3.3V                                //
//    GND                    GND                                  //
//    SDA                    P6(SDA)                              //
//    SCL                    P7(SCL)                              //
//                                                                //
//   JP1:O,JP2:O,JP3:O,JP4:S,JP5:S,JP6:O,JP7:S,JP8:O              //
//   http://akizukidenshi.com/catalog/g/gK-13010/                 //
//================================================================//

#include<Wire.h>
// BMX055 加速度センサのI2Cアドレス  
#define Addr_Accl 0x19  // (JP1,JP2,JP3 = Openの時)
// BMX055 ジャイロセンサのI2Cアドレス
#define Addr_Gyro 0x69  // (JP1,JP2,JP3 = Openの時)
// BMX055 磁気センサのI2Cアドレス
#define Addr_Mag 0x13   // (JP1,JP2,JP3 = Openの時)

// センサーの値を保存するグローバル変数
float xGyro = 0.00;
float yGyro = 0.00;
float zGyro = 0.00;

// rpm計算に使用するグローバル変数
int rpm = 0;

struct repeating_timer st_timer;
bool timer_flag = false;


/* タイマー割り込み処理 */
bool Timer(struct repeating_timer *t) {
  timer_flag = true;
  return true;
}


void setup()
{
  // Wire(Arduino-I2C)の初期化
  Wire1.setSDA(6);
  Wire1.setSCL(7);
  Wire1.begin();
  // デバッグ用シリアル通信は9600bps
  Serial1.setTX(0);
  Serial1.setRX(1);
  Serial1.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);

  add_repeating_timer_us(1000000, Timer, NULL, &st_timer);


  //BMX055 初期化
  BMX055_Init();

  //Serial1.print("Set up done");
  delay(300);
  
}

void loop()
{
  digitalWrite(LED_BUILTIN, LOW);

  BMX055_Gyro();
  rpm = zGyro / 6;

  /*
  Serial1.print("rpm: ");
  Serial1.println(rpm);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(250);
  digitalWrite(LED_BUILTIN, LOW);
  delay(250);
  */

  String TX_rpm = String(rpm);
    //Serial1.print("1\n");
  Serial1.println(TX_rpm);
  delay(100);
/*
  if (timer_flag == true) {
    Serial1.print("rpm:");
    Serial1.println(rpm);
    digitalWrite(LED_BUILTIN, HIGH);
    timer_flag = false;
    delay(50);
  }
*/

/*
  //BMX055 ジャイロの読み取り
  BMX055_Gyro();
  Serial1.print("Gyro= ");
  Serial1.print(xGyro);
  Serial1.print(",");
  Serial1.print(yGyro);
  Serial1.print(",");
  Serial1.print(zGyro);
  Serial1.println(""); 
*/
  //delay(100);
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

