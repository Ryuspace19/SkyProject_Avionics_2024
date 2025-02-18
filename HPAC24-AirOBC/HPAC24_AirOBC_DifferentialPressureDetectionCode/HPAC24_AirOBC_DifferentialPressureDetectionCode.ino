/*
HPAC24-AirOBC Program
2024/3/13作成(渡邉)
readPressure関数内未実装
シリアル通信のボーレートはTweliteと要相談
I2Cアドレスはセンサ側と要相談
*/
#include <Wire.h>

// SDP32のI2Cアドレスを定義
#define SDP32_I2C_ADDRESS 0x21 // 実際のI2Cアドレスに置き換えてください

// 測定間隔とデータの数
const int measurementInterval = 10; // 100Hzでのデータ取得のため10msの間隔
const int numMeasurements = 10; // 平均化する測定値の数
float measurements[numMeasurements]; // 測定値を格納する配列
int measurementIndex = 0; // 現在の測定インデックス

unsigned long lastMeasurementTime = 0; // 最後に測定した時間
unsigned long lastOutputTime = 0; // 最後に出力した時間
const int outputInterval = 100; // 出力間隔100ms（10Hz）

void setup() {
  Serial.begin(115200); // シリアル通信の初期化
  Wire.begin(); // I2Cの初期化
}

void loop() {
  unsigned long currentMillis = millis();

  // 指定された間隔でデータを取得
  if (currentMillis - lastMeasurementTime >= measurementInterval) {
    lastMeasurementTime = currentMillis;
    
    // SDP32から圧力差を読み取る処理（ダミーのランダム値を使用）
    float pressure = random(1000) / 100.0;
    
    // 測定値を配列に格納し、インデックスを更新
    measurements[measurementIndex++] = pressure;

    // インデックスが配列のサイズに達したらリセット
    if (measurementIndex >= numMeasurements) {
      measurementIndex = 0;
    }
  }

  // 10Hzで平均値を出力
  if (currentMillis - lastOutputTime >= outputInterval) {
    lastOutputTime = currentMillis;
    float averagePressure = calculateAverage(measurements, numMeasurements);
    Serial.println(averagePressure);
  }
}

// 測定値の平均を計算する関数
float calculateAverage(float array[], int length) {
  float sum = 0.0;
  for (int i = 0; i < length; i++) {
    sum += array[i];
  }
  return sum / length;
}
