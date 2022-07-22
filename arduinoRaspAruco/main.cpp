
 #include<Arduino.h>
//Fuente: dronebotworkshop.com/?s=l298N
float dist;
//Distancia objetivo. En este caso es 1 metro
float objetivo = 1;
 // Motor 1 
int enA = 9;
int in1 = 8;
int in2 = 7;
 
// Motor 2
int enB = 3;
int in3 = 5;
int in4 = 4;

//Variable para la distancia que recibimos desde el serial
String d;
void backward();
void setup()
 
{
 Serial.begin(9600); 

 //Declaramos los pins como salidas
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
 
}
void forward()
{

  // Encendemos el motor 1
 
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
 
  // Velocidad en el rango de 0-255
 
  analogWrite(enA,200);
 
  // Encendemos el motor 2
 
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
 
  // Velodidad en el rango de 0-255
 
  analogWrite(enB, 200);
 
  delay(2000);
  //Apagamos motores
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

}

void backward()
{
 
  // Opuesto de la función previa
 
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);  
   analogWrite(enA, 200);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH); 
  analogWrite(enB, 200);
  delay(2000);
 
  // Apagamos los motores
 
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);


}
 

void loop()
 
{

if (Serial.available() > 0)
{
  //Leemos lo que nos envía la raspberry
  d=Serial.readString();

  //Convertimos a float 
  dist=d.toFloat();
  
  //Si estás más lejos del objetivo te acercas y viceversa 
  if(dist<objetivo)
  {
     backward();
     delay(1000);
  }
  if (dist>objetivo)
  {
     forward();
     delay(1000);
  }
  else
  {
    delay(1000);
  }

  delay(1000);
 
    }
 
}

