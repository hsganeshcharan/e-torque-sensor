import smbus
import time

# MPU-6050 Registers and Addresses
MPU_ADDR = 0x68
MPU_PWR_MGMT1_REG = 0x6B
MPU_GYRO_CFG_REG = 0x1B
MPU_ACCEL_CFG_REG = 0x1C
MPU_SAMPLE_RATE_REG = 0x19
MPU_CFG_REG = 0x1A
MPU_TEMP_OUTH_REG = 0x41
MPU_GYRO_XOUTH_REG = 0x43
MPU_ACCEL_XOUTH_REG = 0x3B

# Initialize I2C
bus = smbus.SMBus(1)  # Use I2C bus 1 on Raspberry Pi

def write_byte(register, data):
    """Write a byte to a specific register."""
    try:
        bus.write_byte_data(MPU_ADDR, register, data)
    except IOError as e:
        print(f"I2C Write Error: {e}")
        return 1
    return 0

def read_byte(register):
    """Read a single byte from a specific register."""
    try:
        return bus.read_byte_data(MPU_ADDR, register)
    except IOError as e:
        print(f"I2C Read Error: {e}")
        return None

def read_bytes(register, length):
    """Read multiple bytes from a specific register."""
    try:
        return bus.read_i2c_block_data(MPU_ADDR, register, length)
    except IOError as e:
        print(f"I2C Read Error: {e}")
        return None

def mpu_init():
    """Initialize the MPU-6050 sensor."""
    write_byte(MPU_PWR_MGMT1_REG, 0x80)  # Reset device
    time.sleep(0.1)
    write_byte(MPU_PWR_MGMT1_REG, 0x00)  # Wake up the MPU-6050
    set_gyro_fsr(2)
    set_accel_fsr(2)
    set_sample_rate(50)

def set_gyro_fsr(fsr):
    """Set Gyroscope full-scale range."""
    return write_byte(MPU_GYRO_CFG_REG, fsr << 3)

def set_accel_fsr(fsr):
    """Set Accelerometer full-scale range."""
    return write_byte(MPU_ACCEL_CFG_REG, fsr << 3)

def set_sample_rate(rate):
    """Set the sample rate of Gyroscope and Accelerometer."""
    if rate > 1000:
        rate = 1000
    if rate < 4:
        rate = 4
    sample_rate = int(1000 / rate) - 1
    write_byte(MPU_SAMPLE_RATE_REG, sample_rate)
    set_low_pass_filter(rate // 2)

def set_low_pass_filter(lpf):
    """Set the low-pass filter."""
    if lpf >= 188:
        data = 1
    elif lpf >= 98:
        data = 2
    elif lpf >= 42:
        data = 3
    elif lpf >= 20:
        data = 4
    elif lpf >= 10:
        data = 5
    else:
        data = 6
    return write_byte(MPU_CFG_REG, data)

def get_temperature():
    """Get the temperature from MPU-6050."""
    raw = read_bytes(MPU_TEMP_OUTH_REG, 2)
    if raw:
        temp = (raw[0] << 8 | raw[1])
        return 36.53 + (temp / 340.0)
    return None

def get_gyroscope():
    """Get gyroscope data."""
    raw = read_bytes(MPU_GYRO_XOUTH_REG, 6)
    if raw:
        gx = (raw[0] << 8 | raw[1])
        gy = (raw[2] << 8 | raw[3])
        gz = (raw[4] << 8 | raw[5])
        return gx, gy, gz
    return None

def get_accelerometer():
    """Get accelerometer data."""
    raw = read_bytes(MPU_ACCEL_XOUTH_REG, 6)
    if raw:
        ax = (raw[0] << 8 | raw[1])
        ay = (raw[2] << 8 | raw[3])
        az = (raw[4] << 8 | raw[5])
        return ax, ay, az
    return None

# Example usage
if __name__ == "__main__":
    mpu_init()
    time.sleep(1)

    while True:
        temp = get_temperature()
        gyro = get_gyroscope()
        accel = get_accelerometer()

        print(f"Temperature: {temp:.2f}°C")
        print(f"Gyroscope: {gyro}")
        print(f"Accelerometer: {accel}")
        time.sleep(1)
