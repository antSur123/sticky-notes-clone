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
SNOTE_INFO_PATH = FILE_SAVE_DIR + "\\snote.inf"


# Checks if the save directory exists
def check_save_dir_exists():
    if os.path.exists(FILE_SAVE_DIR): 
        print("{FILE_SAVE_DIR} valid")
    else:
        raise Exception(f"{FILE_SAVE_DIR} wasn't found")


# Checks if the snote.inf file exists
def check_snote_inf_exists():
    DEFAULT_FILE_PATH = FILE_SAVE_DIR + "\\default.snote"
    if os.path.isfile(SNOTE_INFO_PATH):
        print("{SNOTE_INFO_PATH} exists.")
        
    else:
        with open(SNOTE_INFO_PATH, "w") as file:
            file.write(DEFAULT_FILE_PATH)


# Reads the last oppened file
def read_last_opened_file():
    check_snote_inf_exists()

    with open(SNOTE_INFO_PATH, "r") as file:
        return file.readline()


# Loads the text from a note
def load_note(note_name):
    fileExt = ".snote"
    file_path = f"{FILE_SAVE_DIR}\\1{fileExt}"
    print(f"{file_path=}")
    text = ""
    try:
        with open(file_path, "r") as file:
            text = file.read()
        print("Successfully read.")
    except:
        print("Error: Couldn't read.")
        raise
    finally:
        return text


# Saves current file
def save_file(textWidget, fileName = 1):
    fileExt = ".snote"
    filePath = f"{FILE_SAVE_DIR}\\1{fileExt}"
    text = textWidget.get("1.0", tk.END)

    debugTextFilePath = "\\" + filePath.split("\\")[-1]
    try:
        with open(filePath, "w") as file:
            file.write(text)
        print(f"{debugTextFilePath} successfully saved.")

    except:
        print(f"Error: Couldn't save {debugTextFilePath}")
        raise


# Opens a file
def open_file(textWidget, filePath = None):
    if type(filePath) == None:
        filePath = filedialog.askopenfilename(
                                    initialdir = FILE_SAVE_DIR,
                                    filetypes=[("Sticky Note File", "*.snote")]
                                    )

    try:
        with open(filePath, "r") as file:
            loadedText = file.read()
        print(f'Successfully read {filePath}')
        
        textWidget.delete("1.0", "end")
        textWidget.insert(index=1.0, chars=loadedText)

    except:
        print(f"Error: Couldn't read {filePath}")
        raise

    
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
