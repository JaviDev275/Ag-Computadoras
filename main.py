
from tkinter import Tk
from gui import ComputerGeneratorGUI


def main():
    window = Tk()
    computer_generator_ui = ComputerGeneratorGUI(window)
    computer_generator_ui.run()

if __name__ == '__main__':
    main()