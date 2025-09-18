import serial
import serial.tools.list_ports
import time
import pygame

def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "ttyACM" in port.device or "ttyUSB" in port.device:
            return port.device
    return None

# --- Find Arduino ---
arduino_port = find_arduino()
if not arduino_port:
    raise Exception("No Arduino detected!")
print("Connected to Arduino on", arduino_port)

arduino = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)

# --- Pygame Joystick Setup ---
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    raise Exception("No joystick found!")
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("Joystick connected:", joystick.get_name())

# --- Variables ---
current_cmd = "s"
last_cmd = "s"
speed_level = 5  # range 0–9

def send_command(cmd):
    global last_cmd
    if cmd != last_cmd:
        arduino.write(cmd.encode())
        last_cmd = cmd

def send_speed(level):
    arduino.write(str(level).encode())

# --- Main Loop ---
try:
    while True:
        pygame.event.pump()

        x_axis = joystick.get_axis(0)  # left/right
        y_axis = joystick.get_axis(1)  # forward/back

        deadband = 0.2
        cmd = "s"

        if abs(y_axis) > abs(x_axis):  # forward/back priority
            if y_axis < -deadband:
                cmd = "f"
            elif y_axis > deadband:
                cmd = "b"
        else:  # left/right
            if x_axis < -deadband:
                cmd = "l"
            elif x_axis > deadband:
                cmd = "r"

        send_command(cmd)

        magnitude = max(abs(x_axis), abs(y_axis))
        new_speed = int(magnitude * 9)  # 0–9
        if new_speed != speed_level:
            speed_level = new_speed
            send_speed(speed_level)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")
    send_command("s")
    arduino.close()
    pygame.quit()
