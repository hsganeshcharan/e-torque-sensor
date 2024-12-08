import math
import time

# Given values
battery_voltage = 12  # 12V battery
motor_power = 250  # 250W motor
payload_weight = 10  # Example payload weight in kg
pedal_sensor_ticks_per_rev = 10  # Example for rotary encoder, 10 ticks per revolution
pedal_cadence = 60  # Pedal cadence in RPM (example)
motor_speed = 0  # Motor speed in RPM, initially 0
motor_torque = 0  # Motor torque in Nm

# Helper functions
def calculate_motor_speed(pedal_cadence, gear_ratio=1):
    """Calculate the motor speed based on pedal cadence and gear ratio."""
    # Assumes motor speed is proportional to pedal cadence and gear ratio
    motor_speed = pedal_cadence * gear_ratio
    return motor_speed

def calculate_torque_assistance(pedal_speed, motor_speed, max_torque=2):
    """Calculate the required motor torque assistance to match pedal speed."""
    # If the motor speed is slower than the pedal speed, provide torque assistance
    speed_difference = pedal_speed - motor_speed
    if speed_difference > 0:
        torque_assistance = speed_difference * max_torque  # Torque increases with speed difference
    else:
        torque_assistance = 0
    return torque_assistance

def calculate_motor_current(power, voltage):
    """Calculate current drawn by the motor using: I = P / V"""
    return power / voltage

# Main control loop (runs every second)
def control_motor(pedal_speed, max_motor_speed=250, max_torque=2):
    global motor_speed, motor_torque
    # Calculate motor speed based on pedal speed
    motor_speed = calculate_motor_speed(pedal_speed)

    # Limit motor speed to max speed
    if motor_speed > max_motor_speed:
        motor_speed = max_motor_speed

    # Calculate the torque required to match pedal speed
    motor_torque = calculate_torque_assistance(pedal_speed, motor_speed, max_torque)

    # Calculate the motor power required
    motor_power_required = motor_torque * motor_speed

    # Calculate the current the motor will draw from the battery
    motor_current = calculate_motor_current(motor_power_required, battery_voltage)

    # Output the motor status
    print(f"Pedal Speed: {pedal_speed} RPM")
    print(f"Motor Speed: {motor_speed} RPM")
    print(f"Torque Assistance: {motor_torque:.2f} Nm")
    print(f"Motor Power: {motor_power_required:.2f} W")
    print(f"Motor Current: {motor_current:.2f} A")
    print("----------")

# Simulate Pedal Speed (RPM)
for i in range(60):  # Simulate 1 minute of cycling
    pedal_speed = 60 + 10 * math.sin(i * math.pi / 30)  # Simulate pedal speed variation
    control_motor(pedal_speed)
    time.sleep(1)
