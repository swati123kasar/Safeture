#include <DHT.h>

DHT dht;

int ledPin=13;
int EP=9;

void setup()
{
  pinMode(ledPin,OUTPUT);
  pinMode(EP,INPUT);
  Serial.begin(9600);
  //Serial.println("vibration dmo");
  
 // Serial.println();
  //Serial.println("Temperature (C)");

  dht.setup(2); // data pin 2
  /*for(int i=0;i<numRead;i++)
  {
      readings[i]=0;
  }*/
}

void loop()
{
  long measurement=TP_init();
  delay(50);
  //Serial.println("measurment :");
  Serial.println(measurement);
  if(measurement>1000)
  {
    digitalWrite(ledPin,HIGH);
  }
  else
  {
    digitalWrite(ledPin,LOW);
  }

  delay(3000);

  //float humidity = dht.getHumidity();
  int temperature = dht.getTemperature();

  //Serial.print(dht.getStatusString());
  //Serial.print("\t");
  //Serial.print(humidity, 1);
  //Serial.print("\t\t");
  Serial.println(temperature, 1);
  
}
long TP_init()
{
  delay(10);
  long measurement=pulseIn(EP,HIGH);
  return measurement;
}
  
