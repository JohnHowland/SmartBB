#include <Arduino.h>
#include <WiFi.h>
#include "driver/mcpwm.h"


#define TOP_BUTTON_PIN  15
#define BOTTOM_BUTTON_PIN  19
#define SERVO_PULSE_GPIO 18

boolean locked = false;
const char* ssid     = "ARRIS-BC2D";
const char* password = "5G4233204430";

WiFiServer server(80);

//Interrupt for "locked" button
void IRAM_ATTR topButtonIsr() 
{
  if(!locked)
  {
    mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 0);
    locked = true;
  }
}

//Interrupt for "unlocked" button
void IRAM_ATTR bottomButtonIsr() 
{
  if(locked)
  {
    mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 0); 
    locked = false;
  }
}

void setup() {
  
  Serial.begin(115200);
  
  pinMode(TOP_BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(TOP_BUTTON_PIN, topButtonIsr, FALLING);
  
  pinMode(BOTTOM_BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(BOTTOM_BUTTON_PIN, bottomButtonIsr, FALLING);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  //wait for wifi to connect
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }

  //print out assigned IP address
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();

  //configure motor PWM driver and pin
  mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0A, SERVO_PULSE_GPIO); // To drive a RC servo, one MCPWM generator is enough

  mcpwm_config_t pwm_config = {
      .frequency = 50, // frequency = 50Hz, i.e. for every servo motor time period should be 20ms
      .cmpr_a = 0,     // duty cycle of PWMxA = 0
      .duty_mode = MCPWM_DUTY_MODE_0,
      .counter_mode = MCPWM_UP_COUNTER,
    };

  //initialize duty cycle to 0
  mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_0, &pwm_config);
  mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 0);
}

void loop() {
  
  WiFiClient client = server.available();   // listen for incoming clients

  if (client) // if you get a client,
  {                             
    Serial.println("New Client.");           // print a message out the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    
    while (client.connected()) 
    {    
      //If bytes to read        
      if (client.available()) 
      {             
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        
        // if the byte is a newline character
        if (c == '\n')
        { 
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0)
          {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            client.print("Click <a href=\"/H\">here</a> to do nothing.<br>");

            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          }
          else
          { // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        }
        else if (c != '\r')
        { // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }

        // Check to see if the client asked to lock
        if (currentLine.equalsIgnoreCase("Lock"))
        {
          if(locked)
            Serial.println("SmartBB already locked."); 
          else
             mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 75);              // turn on motor
        }
       if (currentLine.equalsIgnoreCase("Unlock"))
        {
          if(!locked)
            Serial.println("SmartBB already unlocked."); 
          else
             mcpwm_set_duty(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, 75);               // turn on motor
        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("Client Disconnected.");
  }
}
