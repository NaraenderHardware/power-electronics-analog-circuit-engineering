```cpp
// 50 kHz PWM on Arduino Nano (Pin 9)

void setup() {
  pinMode(9, OUTPUT);

  // Clear Timer1 control registers
  TCCR1A = 0;
  TCCR1B = 0;

  // Set Fast PWM mode with ICR1 as TOP
  TCCR1A |= (1 << WGM11);
  TCCR1B |= (1 << WGM12) | (1 << WGM13);

  // Non-inverting mode on OC1A (Pin 9)
  TCCR1A |= (1 << COM1A1);

  // No prescaler
  TCCR1B |= (1 << CS10);

  // Set TOP value for 50 kHz
  ICR1 = 319;   // 16MHz / (1 * (319+1)) = 50kHz

  // 50% duty cycle
  OCR1A = 160;  // ~50% of 320
}

void loop() {
  // Nothing needed here (hardware PWM runs automatically)
}
```
