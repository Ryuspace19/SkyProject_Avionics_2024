//ライブラリのインクルード
#include <SPI.h>
#include <SD.h>

//SDカードモジュールのチップセレクト
int SD_CS = 10;

//SDカード内部に保存するファイルのパス及びファイル名
String logfilepath = "/sample.txt";

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  Serial.setTimeout(15);

  //ファイルが開けない状態であるときの例外処理
  
  if(!SD.begin(SD_CS)){
    while(1);
  }  
  delay(100);
  
}


void loop() {
  // put your main code here, to run repeatedly:

  //ログデータ保存処理
  if(Serial.available()>0){
    String s = "";
    s += Serial.readString();
      //データフォーマット形成(チェックサム付与)
      String SD_write = String(s);
      //SD_write.concat(",");
      //SD_write.concat(String(nonNumericCount));
      //SD_write.concat(",");
      //SD_write.concat((s));

    //ログファイル保存
    File logfile = SD.open(logfilepath, FILE_WRITE);
    if( logfile ){
      logfile.print(SD_write);
      logfile.close();
    }

  }
}
