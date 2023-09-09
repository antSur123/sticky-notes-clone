import tkinter as tk
from tkinter import filedialog
import os
import platform

# Set directory paths
def get_documents_directory():
    system = platform.system()
    userHome = os.path.expanduser("~")

    if system == "Windows":
        if platform.release() >= "10":
            return os.path.join(userHome, "Documents")
        else:
            return os.path.join(userHome, "My Documents")
    elif system == "Darwin":  # macOS
        return os.path.join(userHome, "Documents")
    elif system == "Linux":
        return os.path.join(userHome, "Documents")
    else:
        raise OSError("Unsupported operating system")
    
DOCUMENTS_DIR = get_documents_directory()
FILE_SAVE_DIR = DOCUMENTS_DIR + "\\StickyNotes notes"

def check_save_dir_exists():
    if os.path.exists(FILE_SAVE_DIR): 
        print("{FILE_SAVE_DIR} valid")
    else:
        raise Exception(f"{FILE_SAVE_DIR} wasn't found")


# Loads the text from a note
def load_note(noteName, textWidget):
    fileExt = ".snote"
    filePath = f"{FILE_SAVE_DIR}\\1{fileExt}"
    print(f"{filePath=}")
    loadedText = ""

    try:
        with open(filePath, "r") as file:
            loadedText = file.read()
        print("Successfully read.")

    except:
        print("Error: Couldn't read.")
        raise

    finally:
        textWidget.delete("1.0", "end")
        textWidget.insert(index=1.0, chars=loadedText)


# Saves current file
def save_file(textWidget, fileName = 1):
    fileExt = ".snote"
    filePath = f"{FILE_SAVE_DIR}\\1{fileExt}"
    text = textWidget.get("1.0", tk.END)

    try:
        with open(filePath, "w") as file:
            file.write(text)
        print("Successfully saved.")

    except:
        print("Error: Couldn't save.")
        raise


# Opens a file
def open_file():
    openFile = filedialog.askopenfilename(
        initialdir = FILE_SAVE_DIR,
        filetypes=[("Sticky Note File", "*.snote")]
    )

    print(openFile)

    
# Create new note file
def create_file(textWidget):
    check_save_dir_exists()
    fileName = textWidget.get()
    fileExt = ".snote"
    filePath = f"{FILE_SAVE_DIR}\\{fileName}{fileExt}"

    if os.path.isfile(filePath):
        raise Exception("File already exists")
    
    else:
        with open(filePath, "w"):
            pass   
        print(f"Created {filePath}")    
        createFileWin.destroy()
        load_note(fileName)
        load_note(fileName, noteTextWidget)


# Open create file createFileWin
def create_file_gui():
    global createFileWin
    createFileWin = tk.Tk()
    createFileWin.title("New file")

    # Create header
    headerLabel = tk.Label(createFileWin, text="Create new note", font=("Arial", 10))
    headerLabel.grid(row=0, columnspan=100, pady=(10, 0))

    # Create labels
    nameLabel = tk.Label(createFileWin, text="Name:")
    nameLabel.grid(row=1, column=0, padx=10, pady=(10, 0))

    # Create entry fields
    nameEntry = tk.Entry(createFileWin)
    nameEntry.grid(row=1, column=1, padx=10, pady=(10, 0))

    # Create buttons
    submitButton = tk.Button(createFileWin, text="Create",
                              command=lambda: create_file(nameEntry))
    submitButton.grid(row=2, columnspan=100, pady=(10, 10))

    createFileWin.mainloop()



check_save_dir_exists()