import smbus
import time
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter  # For smoothing data

# MPU-6050 Registers and Addresses
MPU_ADDR = 0x68
MPU_PWR_MGMT1_REG = 0x6B
MPU_ACCEL_XOUTH_REG = 0x3B
MPU_GYRO_XOUTH_REG = 0x43
MPU_TEMP_OUTH_REG = 0x41

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use I2C bus 1 (Raspberry Pi)

def write_byte(register, value):
    """Write a byte to a register."""
    bus.write_byte_data(MPU_ADDR, register, value)

def read_bytes(register, length):
    """Read multiple bytes from a register."""
    return bus.read_i2c_block_data(MPU_ADDR, register, length)

def initialize_mpu():
    """Initialize the MPU-6050."""
    write_byte(MPU_PWR_MGMT1_REG, 0)  # Wake up the MPU-6050

def get_accelerometer_data():
    """Get accelerometer data (X, Y, Z)."""
    raw = read_bytes(MPU_ACCEL_XOUTH_REG, 6)
    ax = (raw[0] << 8 | raw[1])
    ay = (raw[2] << 8 | raw[3])
    az = (raw[4] << 8 | raw[5])
    return convert_to_signed(ax), convert_to_signed(ay), convert_to_signed(az)

def get_gyroscope_data():
    """Get gyroscope data (X, Y, Z)."""
    raw = read_bytes(MPU_GYRO_XOUTH_REG, 6)
    gx = (raw[0] << 8 | raw[1])
    gy = (raw[2] << 8 | raw[3])
    gz = (raw[4] << 8 | raw[5])
    return convert_to_signed(gx), convert_to_signed(gy), convert_to_signed(gz)

def get_temperature():
    """Get temperature in Celsius."""
    raw = read_bytes(MPU_TEMP_OUTH_REG, 2)
    temp_raw = (raw[0] << 8 | raw[1])
    return (temp_raw / 340.0) + 36.53

def convert_to_signed(val):
    """Convert unsigned 16-bit value to signed."""
    return val - 65536 if val > 32767 else val

def apply_filter(data, window=5, poly=3):
    """Smooth data using Savitzky-Golay filter."""
    return savgol_filter(data, window, poly)

# Collect data for analysis
def collect_data(duration=10, interval=0.1):
    """Collect accelerometer and gyroscope data for a given duration."""
    accel_data = {'x': [], 'y': [], 'z': []}
    gyro_data = {'x': [], 'y': [], 'z': []}
    timestamps = []

    start_time = time.time()
    while time.time() - start_time < duration:
        ax, ay, az = get_accelerometer_data()
        gx, gy, gz = get_gyroscope_data()

        accel_data['x'].append(ax)
        accel_data['y'].append(ay)
        accel_data['z'].append(az)

        gyro_data['x'].append(gx)
        gyro_data['y'].append(gy)
        gyro_data['z'].append(gz)

        timestamps.append(time.time() - start_time)
        time.sleep(interval)

    return accel_data, gyro_data, timestamps

# Plot data
def plot_data(timestamps, accel_data, gyro_data):
    """Visualize accelerometer and gyroscope data."""
    plt.figure(figsize=(12, 8))

    # Accelerometer data
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, accel_data['x'], label='Accel X')
    plt.plot(timestamps, accel_data['y'], label='Accel Y')
    plt.plot(timestamps, accel_data['z'], label='Accel Z')
    plt.title('Accelerometer Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration')
    plt.legend()

    # Gyroscope data
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, gyro_data['x'], label='Gyro X')
    plt.plot(timestamps, gyro_data['y'], label='Gyro Y')
    plt.plot(timestamps, gyro_data['z'], label='Gyro Z')
    plt.title('Gyroscope Data')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main function
if __name__ == "__main__":
    initialize_mpu()
    time.sleep(1)

    print("Collecting data...")
    accel_data, gyro_data, timestamps = collect_data(duration=10, interval=0.1)

    # Apply smoothing filters
    for axis in ['x', 'y', 'z']:
        accel_data[axis] = apply_filter(accel_data[axis])
        gyro_data[axis] = apply_filter(gyro_data[axis])

    print("Data collected. Plotting...")
    plot_data(timestamps, accel_data, gyro_data)
