# Imports
import tkinter as tk
from functions import (startup_file_validation, handle_note_action, 
                       save_file, open_file, read_last_opened_file,
                       create_delete_confirmation_window, update_title
                       )

#// TODO  Add asterisk in not saved file. 
#// TODO  Ask to save file before you close, open or create another note.

# Setup checks
startup_file_validation()


# Screen consts
SCREEN_WIDTH = 403
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
mainWin.resizable(0, 0)


# Create Text Widget
lastOpenedFile = read_last_opened_file()

noteTextWidget = tk.Text(mainWin, width=TEXT_WIDGET_WIDTH, height=TEXT_WIDGET_HEIGHT)
open_file(noteTextWidget, lastOpenedFile, mainWin)


def on_text_change(event):
    # Unsaved file warning
    mainWin.after(10, lambda: update_title(noteTextWidget, mainWin))


noteTextWidget.focus_set()
noteTextWidget.bind("<Key>", on_text_change)

mainWin.protocol("WM_DELETE_WINDOW", lambda: handle_note_action("close", noteTextWidget, mainWin))


# Menu buttons
# 2d list of buttons [ ["text", command], ["text1", command1], ... ]
buttonList = [["Save",      lambda: save_file(noteTextWidget, mainWin) ],
              ["Open",      lambda: handle_note_action("open", noteTextWidget, mainWin) ],
              ["New Note",  lambda: handle_note_action("create", noteTextWidget, mainWin) ],
              ["Delete Note", lambda: create_delete_confirmation_window(noteTextWidget, mainWin) ]
              ]

noteTextWidget.grid(row=0, column=0, columnspan=len(buttonList))

for i, buttonDat in enumerate(buttonList):
    btn_text = buttonDat[0]
    btn_command = buttonDat[1]

    button = tk.Button(mainWin, text=btn_text, command=btn_command)
    button.grid(row=1, column=i, sticky="nsew")


# Start window
mainWin.mainloop()