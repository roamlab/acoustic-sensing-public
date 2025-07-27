#include <micro_ros_arduino.h>
#include <Audio.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/bool.h>
#include <utility/imxrt_hw.h>

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}
#define LED_PIN 13

// Definition of Speaker
AudioOutputI2S           i2s1;           // Output to speaker
AudioSynthToneSweep      sinesweep;      // Tone sweep generator
AudioConnection          patchCord2(sinesweep, 0, i2s1, 0);  // Connect tone generator to speaker
AudioControlSGTL5000     sgtl5000_1;     // Audio shield control

// ROS components
rcl_subscription_t subscription_command;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

// Parameters
float sweep_amp = 1;     // Amplitude of tone sweep (0-1)
int sweep_low = 20;      // Lowest frequency of tone sweep (Hz)
int sweep_high = 20000;  // Highest frequency of tone sweep (Hz)
float sweep_time = 5;   // Duration of tone sweep (seconds)

// Callback function for ROS message
void command_callback(const void * msgin)
{
  const std_msgs__msg__Bool * msg = (const std_msgs__msg__Bool *)msgin;
  Serial.print("Received data: ");
  Serial.println(msg->data);

  if (msg->data) {
    // Start tone sweep
    sinesweep.play(sweep_amp, sweep_low, sweep_high, sweep_time);
    Serial.println("Received TRUE message. Start tone sweep.");

  } else {
//    Serial.println("Received FALSE message.");
  }
  delay(sweep_time * 1000);
  // Initiate executor again
//  RCSOFTCHECK(rclc_executor_fini(&executor));
//  RCSOFTCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
//  RCSOFTCHECK(rclc_executor_add_subscription(
//    &executor, 
//    &subscription_command, 
//    &subscription_command,  
//    command_callback, 
//    ON_NEW_DATA));
  Serial.println("Done tone sweep.");
}

void error_loop(){
  while(1) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  // Initialize Audio library
  AudioMemory(10);  // Increase the allocated memory for audio
  sgtl5000_1.enable();
  sgtl5000_1.lineOutLevel(13); // Set line-out level (13-31)

  // Set up micro-ROS
  set_microros_transports();
  
  allocator = rcl_get_default_allocator();
  
  Serial.println("Initializing micro-ROS...");
  
  while (rclc_support_init(&support, 0, NULL, &allocator) != RCL_RET_OK) {
    delay(100);
    Serial.println("micro-ROS init failed, retrying...");
  }

  Serial.println("micro-ROS initialized.");

  RCCHECK(rclc_node_init_default(&node, "teensy_node", "", &support));
  Serial.println("Node initialized.");

  // Create subscription
  RCCHECK(rclc_subscription_init_default(
      &subscription_command,
      &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
      "command_topic"));
  Serial.println("Subscription initialized.");

  // Create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(
    &executor, 
    &subscription_command, 
    &subscription_command,  
    command_callback, 
    ON_NEW_DATA));
  Serial.println("Executor and subscription added.");

  digitalWrite(LED_PIN, LOW);
}


void loop()
{
  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
  Serial.println("waiting for msg ...");
}
