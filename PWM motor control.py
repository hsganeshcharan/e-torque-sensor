import RPi.GPIO as GPIO
import time

# Motor control pin (GPIO pin connected to motor controller PWM input)
MOTOR_PWM_PIN = 18  # Example GPIO pin for PWM signal
MAX_PWM_DUTY_CYCLE = 100  # Max duty cycle (100% for full motor speed)

# Set up GPIO for PWM
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PWM_PIN, GPIO.OUT)

# Set PWM frequency (in Hz)
PWM_FREQUENCY = 1000  # 1 kHz PWM frequency (adjust according to your motor controller)

# Initialize PWM
pwm_motor = GPIO.PWM(MOTOR_PWM_PIN, PWM_FREQUENCY)
pwm_motor.start(0)  # Start PWM with 0% duty cycle (motor off)

def set_motor_speed(duty_cycle_percentage):
    """Sets the motor speed by adjusting PWM duty cycle"""
    if duty_cycle_percentage < 0:
        duty_cycle_percentage = 0
    elif duty_cycle_percentage > MAX_PWM_DUTY_CYCLE:
        duty_cycle_percentage = MAX_PWM_DUTY_CYCLE

    pwm_motor.ChangeDutyCycle(duty_cycle_percentage)  # Set the motor speed

def calculate_pwm_duty_cycle(torque_assistance, max_torque=2):
    """Maps torque assistance to a PWM duty cycle"""
    # Assuming torque assistance is proportional to required motor speed/torque
    # Map the torque assistance (e.g., 0-2 Nm) to a PWM duty cycle (0-100%)
    duty_cycle = (torque_assistance / max_torque) * MAX_PWM_DUTY_CYCLE
    return duty_cycle

# Example function to adjust motor based on calculated torque assistance
def control_motor(pedal_speed, motor_speed, max_motor_speed=250):
    """Adjust motor speed and torque assistance based on pedal and motor speed"""
    # Calculate the torque assistance (this could be more complex, based on speed difference)
    torque_assistance = calculate_torque_assistance(pedal_speed, motor_speed)

    # Map the calculated torque assistance to a PWM duty cycle
    duty_cycle = calculate_pwm_duty_cycle(torque_assistance)

    # Set the motor speed using PWM
    set_motor_speed(duty_cycle)
    print(f"Motor Speed: {motor_speed} RPM | Torque Assistance: {torque_assistance} Nm | PWM Duty Cycle: {duty_cycle}%")

# Example usage in a loop
try:
    for i in range(60):  # Simulate 1 minute of control loop
        pedal_speed = 60 + 10 * math.sin(i * math.pi / 30)  # Example pedal speed variation
        motor_speed = 58  # Example motor speed (calculated)
