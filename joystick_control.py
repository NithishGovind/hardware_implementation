import pygame
import serial
import time
import sys

# -------------------------
# Arduino connection setup
# -------------------------
ARDUINO_PORTS = ["/dev/ttyACM0", "/dev/ttyUSB0"]  # possible Arduino ports
BAUDRATE = 115200  # adjust to your Arduino sketch

def connect_arduino():
    """Retry until Arduino is found on one of the known ports."""
    while True:
        for port in ARDUINO_PORTS:
            try:
                ser = serial.Serial(port, BAUDRATE, timeout=1)
                print(f"[INFO] ✅ Arduino connected on {port}")
                return ser
            except serial.SerialException:
                continue
        print("[WARN] ⚠️ No Arduino detected, retrying in 2s...")
        time.sleep(2)

# -------------------------
# Joystick setup
# -------------------------
def init_joystick():
    """Initialize pygame joystick, retry if not found."""
    pygame.init()
    pygame.joystick.init()
    while True:
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            print(f"[INFO] ✅ Joystick connected: {joystick.get_name()}")
            return joystick
        else:
            print("[WARN] ⚠️ No joystick detected, retrying in 2s...")
            time.sleep(2)
            pygame.joystick.quit()
            pygame.joystick.init()

# -------------------------
# Robot control logic
# -------------------------
def send_command(ser, x_axis, y_axis):
    """
    Example skid steering mapping:
    - y_axis controls forward/backward
    - x_axis controls left/right turn
    Scale values from -1.0..1.0 → -100..100
    """
    left_speed = int((y_axis + x_axis) * 100)
    right_speed = int((y_axis - x_axis) * 100)

    # clamp values
    left_speed = max(-100, min(100, left_speed))
    right_speed = max(-100, min(100, right_speed))

    command = f"{left_speed},{right_speed}\n"
    try:
        ser.write(command.encode())
    except serial.SerialException:
        print("[ERROR] ❌ Lost Arduino connection, reconnecting...")
        return False
    return True

# -------------------------
# Main loop
# -------------------------
def main():
    arduino = connect_arduino()
    joystick = init_joystick()

    try:
        while True:
            pygame.event.pump()  # process internal queue

            # Example: left stick axes (adjust index for your joystick)
            x_axis = joystick.get_axis(0)  # left/right
            y_axis = -joystick.get_axis(1) # forward/backward (invert)

            if not send_command(arduino, x_axis, y_axis):
                # reconnect if Arduino disconnected
                arduino.close()
                arduino = connect_arduino()

            time.sleep(0.05)  # 20 Hz update
    except KeyboardInterrupt:
        print("\n[INFO] 🚪 Exiting...")
    finally:
        arduino.close()
        pygame.quit()

if __name__ == "__main__":
    main()
