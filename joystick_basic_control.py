import pygame
import os
import pprint

class GamepadReader:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise Exception("No joystick/gamepad connected")
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = {}
        self.button_data = {}
        self.hat_data = {}

    def listen(self):
        # Initialize button and hat data dictionaries
        for i in range(self.controller.get_numbuttons()):
            self.button_data[i] = False
        for i in range(self.controller.get_numhats()):
            self.hat_data[i] = (0, 0)

        print("Listening for joystick events... Press Ctrl+C to exit.")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 3)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Clear terminal and print current joystick state
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Axis Data:")
                pprint.pprint(self.axis_data)
                print("\nButton Data:")
                pprint.pprint(self.button_data)
                print("\nHat Data:")
                pprint.pprint(self.hat_data)

def main():
    reader = GamepadReader()
    try:
        reader.listen()
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    main()
