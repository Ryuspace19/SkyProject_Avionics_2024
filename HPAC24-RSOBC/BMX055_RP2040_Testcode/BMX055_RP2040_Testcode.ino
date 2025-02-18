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
float xAccl = 0.00;
float yAccl = 0.00;
float zAccl = 0.00;
float xGyro = 0.00;
float yGyro = 0.00;
float zGyro = 0.00;
int   xMag  = 0;
int   yMag  = 0;
int   zMag  = 0;

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
  //BMX055 初期化
  BMX055_Init();
  delay(300);
}

void loop()
{
/*
  //BMX055 加速度の読み取り
  BMX055_Accl();
  Serial1.print("Accl= ");
  Serial1.print(xAccl);
  Serial1.print(",");
  Serial1.print(yAccl);
  Serial1.print(",");
  Serial1.print(zAccl);
  Serial1.println(""); 
  */
  //BMX055 ジャイロの読み取り
  BMX055_Gyro();
  Serial1.print("Gyro= ");
  Serial1.print(xGyro);
  Serial1.print(",");
  Serial1.print(yGyro);
  Serial1.print(",");
  Serial1.print(zGyro);
  Serial1.println(""); 
  /*
  //BMX055 磁気の読み取り
  BMX055_Mag();
  Serial1.print("Mag= ");
  Serial1.print(xMag);
  Serial1.print(",");
  Serial1.print(yMag);
  Serial1.print(",");
  Serial1.print(zMag);
  Serial1.println(""); 
  */
  delay(100);
}

//=====================================================================================//
void BMX055_Init()
{
  //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Accl);
  Wire1.write(0x0F); // Select PMU_Range register
  Wire1.write(0x03);   // Range = +/- 2g
  Wire1.endTransmission();
  delay(10);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Accl);
  Wire1.write(0x10);  // Select PMU_BW register
  Wire1.write(0x08);  // Bandwidth = 7.81 Hz
  Wire1.endTransmission();
  delay(10);
  //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Accl);
  Wire1.write(0x11);  // Select PMU_LPW register
  Wire1.write(0x00);  // Normal mode, Sleep duration = 0.5ms
  Wire1.endTransmission();
  delay(10);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Gyro);
  Wire1.write(0x0F);  // Select Range register
  Wire1.write(0x04);  // Full scale = +/- 125 degree/s
  Wire1.endTransmission();
  delay(10);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Gyro);
  Wire1.write(0x10);  // Select Bandwidth register
  Wire1.write(0x07);  // ODR = 100 Hz
  Wire1.endTransmission();
  delay(10);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Gyro);
  Wire1.write(0x11);  // Select LPM1 register
  Wire1.write(0x00);  // Normal mode, Sleep duration = 2ms
  Wire1.endTransmission();
  delay(100);
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Mag);
  Wire1.write(0x4B);  // Select Mag register
  Wire1.write(0x83);  // Soft reset
  Wire1.endTransmission();
  delay(10);
  //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Mag);
  Wire1.write(0x4B);  // Select Mag register
  Wire1.write(0x01);  // Soft reset
  Wire1.endTransmission();
  delay(10);
  //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Mag);
  Wire1.write(0x4C);  // Select Mag register
  Wire1.write(0x00);  // Normal Mode, ODR = 10 Hz
  Wire1.endTransmission();
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Mag);
  Wire1.write(0x4E);  // Select Mag register
  Wire1.write(0x84);  // X, Y, Z-Axis enabled
  Wire1.endTransmission();
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Mag);
  Wire1.write(0x51);  // Select Mag register
  Wire1.write(0x04);  // No. of Repetitions for X-Y Axis = 9
  Wire1.endTransmission();
 //------------------------------------------------------------//
  Wire1.beginTransmission(Addr_Mag);
  Wire1.write(0x52);  // Select Mag register
  Wire1.write(16);  // No. of Repetitions for Z-Axis = 15
  Wire1.endTransmission();
}
//=====================================================================================//
void BMX055_Accl()
{
  unsigned int data[6];
  for (int i = 0; i < 6; i++)
  {
    Wire1.beginTransmission(Addr_Accl);
    Wire1.write((2 + i));// Select data register
    Wire1.endTransmission();
    Wire1.requestFrom(Addr_Accl, 1);// Request 1 byte of data
    // Read 6 bytes of data
    // xAccl lsb, xAccl msb, yAccl lsb, yAccl msb, zAccl lsb, zAccl msb
    if (Wire1.available() == 1)
      data[i] = Wire1.read();
  }
  // Convert the data to 12-bits
  xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16;
  if (xAccl > 2047)  xAccl -= 4096;
  yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16;
  if (yAccl > 2047)  yAccl -= 4096;
  zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16;
  if (zAccl > 2047)  zAccl -= 4096;
  xAccl = xAccl * 0.00098; // range = +/-2g
  yAccl = yAccl * 0.00098; // range = +/-2g
  zAccl = zAccl * 0.00098; // range = +/-2g
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
  zGyro = zGyro * 0.0038; //  Full scale = +/- 125 degree/s
}
//=====================================================================================//
void BMX055_Mag()
{
  unsigned int data[8];
  for (int i = 0; i < 8; i++)
  {
    Wire1.beginTransmission(Addr_Mag);
    Wire1.write((0x42 + i));    // Select data register
    Wire1.endTransmission();
    Wire1.requestFrom(Addr_Mag, 1);    // Request 1 byte of data
    // Read 6 bytes of data
    // xMag lsb, xMag msb, yMag lsb, yMag msb, zMag lsb, zMag msb
    if (Wire1.available() == 1)
      data[i] = Wire1.read();
  }
// Convert the data
  xMag = ((data[1] <<5) | (data[0]>>3));
  if (xMag > 4095)  xMag -= 8192;
  yMag = ((data[3] <<5) | (data[2]>>3));
  if (yMag > 4095)  yMag -= 8192;
  zMag = ((data[5] <<7) | (data[4]>>1));
  if (zMag > 16383)  zMag -= 32768;
}
