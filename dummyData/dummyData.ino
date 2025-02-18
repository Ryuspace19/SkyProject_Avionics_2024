void setup() {
  Serial.begin(115200);
  delay(5000);
}

void loop() {
  Serial.println("app,No,1,AIR,7.1,RS,120,ALT,0,PLT,90,90");
  delay(100);
  Serial.println("app,No,2,AIR,7.4,RS,122,ALT,20,PLT,90,90");
  delay(100);
  Serial.println("app,No,3,AIR,7.6,RS,124,ALT,40,PLT,90,90");
  delay(100);
  Serial.println("app,No,4,AIR,7.8,RS,126,ALT,60,PLT,90,90");
  delay(100);
  Serial.println("app,No,5,AIR,8.0,RS,128,ALT,80,PLT,90,90");
  delay(100);
  Serial.println("app,No,6,AIR,8.2,RS,130,ALT,100,PLT,90,90");
  delay(100);
  Serial.println("app,No,7,AIR,8.4,RS,132,ALT,120,PLT,90,90");
  delay(100);
  Serial.println("app,No,8,AIR,8.6,RS,134,ALT,140,PLT,90,90");
  delay(100);
  Serial.println("app,No,9,AIR,8.8,RS,136,ALT,120,PLT,90,90");
  delay(100);
  Serial.println("app,No,10,AIR,9.0,RS,138,ALT,100,PLT,90,90");
  delay(100);
}
