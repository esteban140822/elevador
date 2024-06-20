/*
  Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador Arduino

  ALUMNOS:
  Bautista Arreola Esteban Misael
  Ibarra Hernández Héctor Napoleón 

  Version: Finalizada
  Comentarios: Elevador funcional, cuenta con 5 botones, 4 para subir entre los pisos segun sean seleccionados
  y 1 denominado el boton de panico, el cual al ser activado pasa al operador el permiso de poder mover el
  elevador si es deseado, unicamente si hace sesion en la interfaz de otro archivo de python ya creado.
  Puede moverlo de forma entre pisos directamente o por pasos.
  
  25/Mayo/2023
*/

#include <Wire.h>  // Librería de comunicación por I2C
#define Pecho 6    // Pecho conectado al pin 6 (Sensor de proximidad)
#define Ptrig 7    // Trigger conectado al pin 7 (Sensor de Proximidad)
#include <LiquidCrystal_I2C.h>  // Librería para LCD por I2C
#include <Stepper.h>            // Librería para comunicación con el motor

LiquidCrystal_I2C lcd(0x3f, 16, 2);  // Lectura para el LCD

//DIBUJOS PARA EL LCD
byte Flecha_A[8] = {  // Se dibuja una flecha hacia arriba
  0b00100,
  0b01110,
  0b11111,
  0b01110,
  0b01110,
  0b01110,
  0b00000,
  0b00000
};
byte Flecha_B[8] = {  // Se dibuja una flecha hacia abajo
  0b00000,
  0b00000,
  0b01110,
  0b01110,
  0b01110,
  0b11111,
  0b01110,
  0b00100
};


int stepsPerRevolution = 2048;                        // Pasos para de una vuelta completa
int motSpeed = 10;                                    // Velocidad del motor
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);  // Declaración del motor

int t;    // Guardamos el valor del sensor ultrasónico
int dis;  // Para guardar el valor en cm

//Estados de los botones inicializados en 0
int estado1 = 0;
int estado2 = 0;
int estado3 = 0;
int estado4 = 0;

int banderaAlto = true; // Valor para entrar a la función independiente del elevador o cambiarlo al modo operador

int alturaPisos[] = { 3, 10, 17, 24 }; // Distancia a la que esta cada piso
int selecPiso;  // Variable para seleccionar el piso con los botones
int Piso;       // Variable para seleccionar piso en modo operador
bool mover;    // Variable para permitir que el operador mueva el elevador
bool mover_man;
bool aviso_detenido;
String puerta=" ";
String puerta_2=" ";

//COMIENZA EL SETUP*********************************************************
void setup() {
  // DISPLAY
  lcd.init();       // Iniciar el Display
  lcd.backlight();  // Fondo del Display
  lcd.clear();      // Se limpia la pantalla LCD
  lcd.createChar(0, Flecha_A);
  lcd.createChar(1, Flecha_B);
  myStepper.setSpeed(motSpeed);  // VELOCIDAD MOTOR
  Serial.begin(9600);

  //Iniciar el Sensor
  pinMode(Pecho, INPUT);   // Pin 6 como entrada
  pinMode(Ptrig, OUTPUT);  // Pin 7 como salida

  //BOTONES
  pinMode(5, INPUT);
  pinMode(4, INPUT);
  pinMode(3, INPUT);
  pinMode(12, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), boton_paro, CHANGE);  // Botón de panico
}
//TERMINA EL SETUP*****************************************************

//COMIENZA EL LOOP------------------------------------------------------
void loop() {
  if (banderaAlto) { // Si es verdadero entra y da acceso a los botones para moverlo independientemente

    digitalWrite(Ptrig, LOW);
    digitalWrite(Ptrig, HIGH);  // Pulso trigger de 10ms
    digitalWrite(Ptrig, LOW);

    //Botones
    estado1 = digitalRead(5);
    estado2 = digitalRead(4);
    estado3 = digitalRead(3);
    estado4 = digitalRead(12);

    //FUNCIONES PARA ELEGIR EL PISO Y DETECTAR LA DISTANCIA
    escogerPiso();
    distancia();
    //CONDICIONES DE PISOS
    if (dis == alturaPisos[selecPiso - 1] && selecPiso != 0) {// DETENER EL ELEVADOR
      puerta="ABIERTA ";
      alto();
      apagado();
    }

    if (dis < alturaPisos[selecPiso - 1] && selecPiso != 0) {// SUBIR EL ELEVADOR
      puerta="CERRADA ";
      subir();
    }

    if (dis > alturaPisos[selecPiso - 1] && selecPiso != 0) {// BAJAR EL ELEVADOR
      puerta="CERRADA ";
      bajar();
    }

  } else {
      aviso_detenido;
      while(aviso_detenido){
      lcd.setCursor(0, 0);
      lcd.print("DETENIDO");  // Mensaje a despegar en el Display
      Serial.print("DETENIDO ");
      Serial.print(puerta);
      Serial.print(dis);
      Serial.print("cm");
      Serial.println();
      selecPiso = 0;
      aviso_detenido = false;
      delay(1000);
      }
    
    // SI PRESIONA M PERMITE AL OPERADOR MOVER EL ELEVADOR (OPERADOR)
    mover;
    while (mover) {
      escogerPiso_Operador();
      distancia();
      if (dis == alturaPisos[selecPiso - 1] && selecPiso != 0) {// DETENER EL ELEVADOR
        alto();
        apagado();
      }
      if (dis < alturaPisos[selecPiso - 1] && selecPiso != 0) {// SUBIR EL ELEVADOR
        subir();
      }
      if (dis > alturaPisos[selecPiso - 1] && selecPiso != 0) {// BAJAR EL ELEVADOR
        bajar();
      }
      if (Piso == 6) {  // SI PRESIONA LA TECLA C TODO EL FUNCIONAMIENTO DEL ELEVADOR VUELVE A SU FUNCION NORMAL (OPERADOR-ELEVADOR)
        lcd.setCursor(0, 0);
        lcd.print("CONTINUA");  // Mensaje a despegar en el Display
        Serial.print("CONTINUA ");
        Serial.print(puerta);
        Serial.print(dis);
        Serial.print("cm");
        Serial.println();
        mover=false;
        banderaAlto = true; // Vuelve a ser true para operar normalmente
        delay(2000);
      }
      if (Piso == 7) {// SI SE PRESIONA EL 9 SALE DE LA FUNCION DE MOVER EL ELEVADOR DE FORMA AUTOMÁTICA
        mover = false;
      }
      if (Piso == 8){
        puerta="CERRADA ";
        puerta_2=puerta;
      }
      if (Piso == 9){
        puerta="ABIERTA ";
        puerta_2=puerta;
      }
    }
    char manual = Serial.read();
    distancia();
    if (manual == 'S') {  // SI PRESIONA LA TECLA S TODO EL FUNCIONAMIENTO DEL ELEVADOR SE HACE MANUAL PARA SUBIR (OPERADOR)
      subir_man();
    }
    if (manual == 'B') {  // SI PRESIONA LA TECLA B TODO EL FUNCIONAMIENTO DEL ELEVADOR SE HACE MANUAL PARA BAJAR (OPERADOR)
      bajar_man();
    }
    if (manual == 'A'){   // SI PRESIONA LA TECLA A TODO EL FUNCIONAMIENTO DEL ELEVADOR VUELVE A SER AUTOMÁTICO (OPERADOR)
      mover=true;
    }
    if (manual == 'J'){
        puerta="CERRADA ";
    }
    if (manual == 'O'){
        puerta="ABIERTA ";
    }
    if (manual == 'C') {  // SI PRESIONA LA TECLA C TODO EL FUNCIONAMIENTO DEL ELEVADOR VUELVE A SU FUNCION NORMAL (OPERADOR-ELEVADOR)
      lcd.setCursor(0, 0);
      lcd.print("CONTINUA");  // Mensaje a despegar en el Display
      Serial.print("CONTINUA ");
      Serial.print(puerta);
      Serial.print(dis);
      Serial.print("cm");
      Serial.println();
      banderaAlto = true; // Vuelve a ser true para operar normalmente
      delay(2000);
    }
  }
}
//TERMINA EL LOOP--------------------------------------------------

//COMIENZAN LAS FUNCIONES++++++++++++++++++++++++++++++++++++++++++++

//FUNCIÓN PARA ELEGIR EL PISO CON LOS BOTONES
void escogerPiso() {
  if (estado1 == HIGH) {
    selecPiso = 1;
    return selecPiso;
  }
  if (estado2 == HIGH) {
    selecPiso = 2;
    return selecPiso;
  }
  if (estado3 == HIGH) {
    selecPiso = 3;
    return selecPiso;
  }
  if (estado4 == HIGH) {
    selecPiso = 4;
    return selecPiso;
  }
}

//FUNCIÓN UNICAMENTE CUANDO SE PRESIONA EL BOTÓN DE PARO Y EL ELEVADOR PASA A SER DIRIGIDO POR EL OPERADOR
void escogerPiso_Operador() {
  Piso = Serial.parseInt();
  if (Piso == 1) {
    selecPiso = 1;
    return selecPiso;
  }
  if (Piso == 2) {
    selecPiso = 2;
    return selecPiso;
  }
  if (Piso == 3) {
    selecPiso = 3;
    return selecPiso;
  }
  if (Piso == 4) {
    selecPiso = 4;
    return selecPiso;
  }
}

//FUNCIÓN PARA CALCULAR LA DISTANCIA E IMPRIMIR
void distancia() {
  digitalWrite(Ptrig, HIGH);
  delayMicroseconds(10);  // Enviamos un pulso de 10us
  digitalWrite(Ptrig, LOW);

  t = pulseIn(Pecho, HIGH);  // Obtenemos el ancho del pulso
  dis = t / 58;
}

//FUNCIÓN PARA APAGAR EL MOTOR
void apagado() {
  digitalWrite(11, LOW);
  digitalWrite(10, LOW);
  digitalWrite(9, LOW);
  digitalWrite(8, LOW);
}

//FUNCIÓN PARA DETENER EL ELEVADOR AUNQUE ESTE EN MOVIMIENTO
void boton_paro() {
  banderaAlto = false;
  mover = true;
  mover_man = true;
  aviso_detenido = true;
}

//FUNCIÓN PARA DETENER EL ELEVADOR
void alto() {
  lcd.clear();
  lcd.setCursor(0, 1);          
  lcd.print("PUERTA "+puerta); 
   
  lcd.display();                
  if (dis == 3) {
    lcd.setCursor(0, 0);          
    lcd.print("PLANTA BAJA");
    lcd.display();
    Serial.print("PLANTA BAJA ");
    Serial.print(puerta);
    Serial.print(dis);
    Serial.print("cm");
    Serial.println();
    delay(300); 
    lcd.clear();              
  }
  if (dis == 10) {
    lcd.setCursor(0, 0);         
    lcd.print("PISO 1");
    lcd.display(); 
    Serial.print("PISO 1 ");
    Serial.print(puerta);
    Serial.print(dis);
    Serial.print("cm");
    Serial.println();     
    delay(300);  
    lcd.clear();        
  }
  if (dis == 17) {
    lcd.setCursor(0, 0);     
    lcd.print("PISO 2");
    lcd.display();
    Serial.print("PISO 2 ");
    Serial.print(puerta);
    Serial.print(dis);
    Serial.print("cm");
    Serial.println();   
    delay(300); 
    lcd.clear();          
  }
  if (dis == 24) {
    lcd.setCursor(0, 0);        
    lcd.print("PISO 3");
    lcd.display();  
    Serial.print("PISO 3 ");
    Serial.print(puerta);
    Serial.print(dis);
    Serial.print("cm");
    Serial.println();
    delay(300);   
    lcd.clear();         
  }
}

//FUNCION PARA SUBIR EL ELEVADOR
void subir() {
  Serial.print("SUBIENDO ");
  Serial.print(puerta);
  Serial.print(dis);
  Serial.print("cm");
  Serial.println();
  lcd.setCursor(0, 0);          // Ubica cursor en columna 0 y linea 0
  lcd.print("SUBIENDO");        // Escribe texto
  lcd.setCursor(12, 0);
  lcd.write(0);                // Muestra el texto
  lcd.setCursor(0, 1);          // Ubica cursor en columna 0 y linea 1
  lcd.print("PUERTA "+puerta);  // Escribe texto
  myStepper.step(-400);
  lcd.clear();
}

//FUNCION PARA BAJAR EL ELEVADOR
void bajar() {
  Serial.print("BAJANDO ");
  Serial.print(puerta);
  Serial.print(dis);
  Serial.print("cm");
  Serial.println();
  lcd.setCursor(0, 0);          // Ubica cursor en columna 0 y linea 0
  lcd.print("BAJANDO");        // Escribe texto
  lcd.setCursor(12, 0);
  lcd.write(1);                // Muestra el texto
  lcd.setCursor(0, 1);          // Ubica cursor en columna 0 y linea 1
  lcd.print("PUERTA "+puerta); // Escribe texto
  myStepper.step(400);
  lcd.clear();
}
//FUNCION PARA SUBIR EL ELEVADOR DE MANERA MANUAL
void subir_man() {
  Serial.print("SUBIENDO ");
  Serial.print(puerta);
  Serial.print(dis);
  Serial.print("cm");
  Serial.println();
  lcd.setCursor(0, 0);          // Ubica cursor en columna 0 y linea 0
  lcd.print("SUBIENDO");        // Escribe texto
  lcd.setCursor(12, 0);
  lcd.write(0);                // Muestra el texto
  lcd.setCursor(0, 1);          // Ubica cursor en columna 0 y linea 1
  lcd.print("PUERTA "+puerta);  // Escribe texto
  myStepper.step(-100);
  lcd.clear();
}

//FUNCION PARA BAJAR EL ELEVADOR DE MANERA MANUAL
void bajar_man() {
  Serial.print("BAJANDO ");
  Serial.print(puerta);
  Serial.print(dis);
  Serial.print("cm");
  Serial.println();
  lcd.setCursor(0, 0);          // Ubica cursor en columna 0 y linea 0
  lcd.print("BAJANDO");        // Escribe texto
  lcd.setCursor(12, 0);
  lcd.write(1);                // Muestra el texto
  lcd.setCursor(0, 1);          // Ubica cursor en columna 0 y linea 1
  lcd.print("PUERTA "+puerta); // Escribe texto
  myStepper.step(100);
  lcd.clear();
}
