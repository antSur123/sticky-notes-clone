# Imports
import tkinter as tk
from functions import (save_file, open_file, create_file_gui, 
                       read_last_opened_file, check_save_dir_exists,
                       check_snote_inf_exists
                       )

check_save_dir_exists()
check_snote_inf_exists()


# Screen consts
SCREEN_WIDTH = 400
SCREEN_HEIGHT = SCREEN_WIDTH
SCREEN_GEOMETRY = str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT)


# Variable consts
TXT_CHAR_WIDTH = 8
TXT_ROW_HEIGHT = 16
BUTTON_HEIGHT = 2
TEXT_WIDGET_WIDTH = SCREEN_WIDTH // TXT_CHAR_WIDTH
TEXT_WIDGET_HEIGHT = SCREEN_HEIGHT // TXT_ROW_HEIGHT - BUTTON_HEIGHT


# Window setup
mainWin = tk.Tk()
mainWin.title("Notes")
mainWin.geometry(SCREEN_GEOMETRY)


# Create Text Widget
noteTextWidget = tk.Text(mainWin, width=TEXT_WIDGET_WIDTH, height=TEXT_WIDGET_HEIGHT)
lastOpenedFile = read_last_opened_file()
open_file(noteTextWidget, lastOpenedFile)


# Menu buttons
# 2d list of buttons [ ["name", command], ["name1", command1], ... ]
buttonList = [["Save",  lambda: save_file(noteTextWidget)],
              ["Open",  lambda: open_file(noteTextWidget)],
              ["New Note",      create_file_gui]
              ]

noteTextWidget.grid(row=0, column=0, columnspan=len(buttonList))

for i, buttonDat in enumerate(buttonList):
    btn_text = buttonDat[0]
    btn_command = buttonDat[1]

    button = tk.Button(mainWin, text=btn_text, command=btn_command)
    button.grid(row=1, column=i, sticky="nsew")


# Start window
mainWin.mainloop()