/*
** Scheduler provides teh framework to run tasks at regular times.
** Time is based on a delta from the previous micros() value. 
**
** Original Author:  Greg Watkins
** Date:    27 Aug 2021
** Updated by: Daniel Babekuhl
** Date:    14 Aug 2022
*/
#include "BluetoothSerial.h"
#include "switch.h"

BluetoothSerial SerialBT;
// pins for LED and switch
#define LED_PIN 32
#define SWITCH_PIN 33
#define SENSOR_PIN 25

// holds tick time counts
unsigned long lastTickTime;
bool pushOnOff1 = false;
uint16_t pulse_reading;
unsigned long adcStart, adcEnd;
int count = 1;
int threshold = 1000;
boolean old_state = false;
boolean new_state = false;
unsigned long period;
float rate;
float new_rate;
unsigned long lastTransition, currentTransition, largest_time;
int record[100];
int position_i = 0;
char sending[1000];

String btName = "ESP32testG06";
bool connected;
bool first_20 = true;

void setup() {
  // initialize pin modes
  pinMode(LED_PIN, OUTPUT);
  pinMode(SWITCH_PIN, INPUT);
  
  // start the Serial interface (over USB)
  Serial.begin(115200);
  Serial.println("****************************");
  Serial.println("* ESP Bluetooth SLAVE DEMO *");
  Serial.println("****************************");
  Serial.println("\nNow run the host program...");

  SerialBT.register_callback(btCallback);

  SerialBT.begin(btName); //Bluetooth device name

  if (!SerialBT.begin(btName))
  {
    Serial.println("An error occurred initializing Bluetooth");
  }
  else
  {
    Serial.println("Bluetooth initialized");
    Serial.println(btName);
  }
}

// Define switch data
// require 10 consecutive same-state readings before validating switch push
#define DEBOUNCE_CNT 5
Switch switch1(1, DEBOUNCE_CNT);

// TICK/SCHEDULING DATA
// 200000 microseconds in 20 milliseconds
#define TICK_20MSEC 20000
 
// to count ticks to 1 sec
uint16_t tick1sec = 0;  
#define TICK_1SEC 50

// to count ticks to 10 sec
uint16_t tick10sec = 0; 
#define TICK_10SEC 500

// accumulate seconds for a time of day (ToD) clock
uint16_t secondsToD = 0;     

void loop() {
  
  if ((micros() - lastTickTime) > TICK_20MSEC) {
    // save current time immediately. This preserves timing accuracy indpendent
    // of the execution time of the code below. This is moe accurate than using the 
    // delay() function.
    lastTickTime = micros();  
    
    //*********************** 20 msec tasks *********************

    if (first_20){
      sprintf(&(sending[0]), "%06d ", count);
      if (rate < 100) {
        sprintf(&(sending[7]), "0%.1f ", rate);
      } else {
        sprintf(&(sending[7]), "%.1f ", rate);
      }
      first_20 = false;
    }
    // can update/check status in one statement
    pulse_reading = analogRead(SENSOR_PIN);
    sprintf(&(sending[13 + 5 * position_i]), "%04d ", pulse_reading);
    position_i++;
    // record for 2 second
    for (int i = 0; i < 99; i++){
      record[i] = record[i + 1];
    }
    record[99] = pulse_reading;
    int current_largest = 0;
    for (int i = 0; i < 100; i++){
      if (record[i] > current_largest){
        current_largest = record[i];
      }
    }
    int current_smallest = 3000;
    for (int i = 0; i < 100; i++){
      if (record[i] < current_smallest){
        current_smallest = record[i];
      }
    }
    
    threshold = current_largest - 0.3*(current_largest - current_smallest);
    //Serial.println(threshold);
    old_state = new_state;
    Serial.printf("%lu,%d\n",threshold,pulse_reading);
    if (pulse_reading > threshold){
      new_state = true;
    }
    else {
      new_state = false;
    }
    if (old_state == false && new_state == true) {
      lastTransition = currentTransition;
      currentTransition = millis();
    }

    period = currentTransition - lastTransition;
    new_rate = 60000./((float)period);
    if (new_rate < 200){
      rate = new_rate;
    }
    //>>>>> Insert code here so that each switch operates as a push on/push off switch rather than momentary contact
  
    // solution 4.2: pushOnOff1 is stored in global space so it can retain its value
    switch1.update(digitalRead(SWITCH_PIN));
    if (switch1.changed())
    {
      if (switch1.state())
      {
        pushOnOff1 = !pushOnOff1;
        Serial.printf("Switch Push-on/off %x ->%x\n", switch1.id(), pushOnOff1);
      }
    }

    if (pushOnOff1){
        digitalWrite(LED_PIN, LOW);
      }
      else {
        digitalWrite(LED_PIN, HIGH);
    }
    //************************************************************
    


    //*********************** 1 sec tasks *********************
    if (++tick1sec >= TICK_1SEC) {
      if (pushOnOff1){
        SerialBT.printf("Sending Stopped\n");
      }
      else {
        SerialBT.printf("%s\n", sending);
        count++;
      }
      if (count == 1000000){
        count = 0;
      }
      first_20 =  true;
      memset(sending, 0, 1000);
      position_i = 0;
      tick1sec = 0;
    }
    //************************************************************



    //*********************** 10 sec tasks *********************
    if (++tick10sec >= TICK_10SEC) {
      tick10sec = 0;
    }
    //************************************************************

  } // 20 msec tick
}

int openEvt = 0;

void btCallback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param)
//
// This function displays SPP events when they occur. This provides 
// information on what is hapening on the bluetooth link.
//
//
{
  if (event == ESP_SPP_SRV_OPEN_EVT) {
    char buf[50];
    openEvt++;
    sprintf(buf, "Client Connected:%d", openEvt);
    Serial.println(buf);
    Serial.print("  Address = ");

    for (int i = 0; i < 6; i++)
    {
      sprintf(&(buf[i * 3]), "%02X:", param->srv_open.rem_bda[i]);
    }
    buf[17] = 0;
    Serial.println(buf);
  }


  if (event == ESP_SPP_INIT_EVT)
    Serial.println("ESP_SPP_INIT_EVT");
  else if (event == ESP_SPP_UNINIT_EVT)
    Serial.println("ESP_SPP_INIT_EVT");
  else if (event == ESP_SPP_DISCOVERY_COMP_EVT )
    Serial.println("ESP_SPP_DISCOVERY_COMP_EVT");
  else if (event == ESP_SPP_OPEN_EVT )
    Serial.println("ESP_SPP_OPEN_EVT");
  else if (event == ESP_SPP_CLOSE_EVT )
    Serial.println("ESP_SPP_CLOSE_EVT");
  else if (event == ESP_SPP_START_EVT )
    Serial.println("ESP_SPP_START_EVT");
  else if (event == ESP_SPP_CL_INIT_EVT )
    Serial.println("ESP_SPP_CL_INIT_EVT");
  else if (event == ESP_SPP_DATA_IND_EVT )
    Serial.println("ESP_SPP_DATA_IND_EVT");
  else if (event == ESP_SPP_CONG_EVT )
    Serial.println("ESP_SPP_CONG_EVT");
  else if (event == ESP_SPP_WRITE_EVT )
    Serial.println("ESP_SPP_WRITE_EVT");
  else if (event == ESP_SPP_SRV_OPEN_EVT )
    Serial.println("ESP_SPP_SRV_OPEN_EVT");
  else if (event == ESP_SPP_SRV_STOP_EVT )
    Serial.println("ESP_SPP_SRV_STOP_EVT");
  else
  {
    Serial.print("EV: ");
    Serial.println(event);
  };
}
