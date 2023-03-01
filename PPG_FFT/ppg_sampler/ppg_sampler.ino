/*
 * Basic pulse reading program. Samples and transmits
 * (via UART) a pulse sensor signal at a rate of 
 * SAMPLE_HZ. Output data format:
 *    "<pulse sensor value>,<sample freq (Hz)>\n"
 */

#define BAUDRATE 115200
#define SAMPLE_HZ 50
#define SENSOR_PIN 25

long time_1;
long time_2;

void setup() {
  Serial.begin(BAUDRATE);
  time_1 = micros();
}

void loop() {

  // aquire and transmit sample if a period of 1000000/SAMPLE_HZ microseconds has elapsed
  time_2 = micros();
  if ((time_2 - time_1) > 1000000/SAMPLE_HZ) {
    Serial.printf("%d,%.2f\n", analogRead(SENSOR_PIN), (float)1000000./(time_2 - time_1));
    time_1 = time_2;   
  }
}
