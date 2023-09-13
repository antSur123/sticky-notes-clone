import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
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
        messagebox.showinfo("Error", "Unsupported operating system.")
        raise OSError("Unsupported operating system")
    
DOCUMENTS_DIR = get_documents_directory()
FILE_SAVE_DIR = DOCUMENTS_DIR + "\\StickyNotes notes"
LAST_SNOTE_INFO_PATH = FILE_SAVE_DIR + "\\last.snote.inf"
DEFAULT_FILE_PATH = FILE_SAVE_DIR + "\\default.snote"


# Checks if the save directory exists
def check_save_dir_exists():
    if os.path.exists(FILE_SAVE_DIR): 
        print("{FILE_SAVE_DIR} valid")
    else:
        os.makedirs(FILE_SAVE_DIR)
        print("{FILE_SAVE_DIR} was created")


# Checks if the snote.inf file exists
def check_snote_inf_exists():
    if os.path.isfile(LAST_SNOTE_INFO_PATH):
        print("{LAST_SNOTE_INFO_PATH} exists.")
        
    else:
        with open(LAST_SNOTE_INFO_PATH, "w") as file:
            file.write(DEFAULT_FILE_PATH)


# Check if default.snote file exists
def check_default_snote_exists():
    if os.path.isfile(DEFAULT_FILE_PATH):
        print("{DEFAULT_FILE_PATH} exists.")
        
    else:
        with open(DEFAULT_FILE_PATH, "w") as file:
            text = ("Welcome to Sticky Notes by Time\n\n\
Here you can save, open, create and remove Sticky Notes files.\n\n\
However, you can not save changes to this default file.\n\n\
Enjoy!")
            file.write(text)


# Ask "Do you want to save before you..."
def on_close(window):
    modalAnswer = messagebox.askyesnocancel("Closing without saving.", "Unsaved\nDo you want to save before closing?")
    
    print(f"{modalAnswer=}")
    if modalAnswer == False:
        window.destroy()

    elif modalAnswer == True:
        print("save")
        window.destroy()

    else: 
        print("Canceled close")



# Reads the last oppened file
def read_last_opened_file():
    check_snote_inf_exists()

    with open(LAST_SNOTE_INFO_PATH, "r") as file:
        return file.readline()
    

# Saves current file
def save_file(textWidget):
    filePath = read_last_opened_file()

    filePath = filePath.replace("\\", "/")
    fileName = filePath.split("/")[-1].split(".")[0]
    if fileName == "default":
        print("Save failed. You can not edit the default note.")
        messagebox.showinfo("Save failed", "You can not edit the default note.")
        return


    text = textWidget.get("1.0", tk.END)

    # Save file
    try:
        with open(filePath, "w") as file:
            file.write(text)
        print(f"{filePath} successfully saved.")
        messagebox.showinfo("Succesfully saved", "File saved successfully.")

    except:
        print(f"Error: Couldn't save {filePath}")
        messagebox.showinfo("Save failed", "File failed to save.")
        raise


# Opens a file
def open_file(textWidget, filePath, window):
    if filePath == None:
        filePath = filedialog.askopenfilename(
                                    initialdir = FILE_SAVE_DIR,
                                    filetypes=[("Sticky Note File", "*.snote")]
                                    )

    try:
        with open(filePath, "r") as file:
            loadedText = file.read()

        editedFilePath = filePath.replace("\\", "/")
        windowTitle = "Notes  |  " + editedFilePath.split("/")[-1].split(".")[0]

    except:
        print(f"Error: Couldn't read {filePath}")
        print("Trying to open {DEFAULT_FILE_PATH} instead.")
        check_save_dir_exists()
        check_default_snote_exists()

        try:
            with open(DEFAULT_FILE_PATH, "r") as file:
                loadedText = file.read()
                windowTitle = "Notes  |  default"

        except:
            print("Error: Couldn't read {DEFAULT_FILE_PATH}")
            messagebox.showinfo("Read failed", "Couldn't read file.")
            raise
            

    finally:
        print(f'Successfully read {filePath}')

        textWidget.delete("1.0", tk.END)
        textWidget.insert(index=1.0, chars=loadedText)

        window.title(windowTitle)

        # Update last oppened file
        try:
            with open(LAST_SNOTE_INFO_PATH, "w") as file:
                file.write(filePath)
        
        except:
            print("Error: Couldn't write to {LAST_SNOTE_INFO_PATH}")
            messagebox.showinfo("Write failed", "Couldn't write to file.")
            raise

    
# Create new note file
def create_file(textWidget, mainTextWidget, window):
    check_save_dir_exists()
    fileName = textWidget.get()
    fileExt = ".snote"
    filePath = f"{FILE_SAVE_DIR}\\{fileName}{fileExt}"

    if os.path.isfile(filePath):
        raise Exception("File already exists")
    
    else:
        with open(filePath, "w"):
            pass     
        createFileWin.destroy()
        open_file(mainTextWidget, filePath, window)
        print(f"Created {filePath}")        
        messagebox.showinfo("Succesfully created", "The file was created successfully.")


# Open create file createFileWin
def create_file_gui(mainTextWidget, window):
    
    # Trigger button with enter
    def on_enter_key(event):
        submitButton.invoke()

    global createFileWin
    createFileWin = tk.Toplevel(window)
    createFileWin.title("New file")
    createFileWin.resizable(0, 0)

    # Create header
    headerLabel = tk.Label(createFileWin, text="Create new note", font=("Arial", 10))
    headerLabel.grid(row=0, columnspan=100, pady=(10, 0))

    # Create labels
    nameLabel = tk.Label(createFileWin, text="Name:")
    nameLabel.grid(row=1, column=0, padx=10, pady=(10, 0))

    # Create entry fields
    nameEntry = tk.Entry(createFileWin)
    nameEntry.grid(row=1, column=1, padx=10, pady=(10, 0))
    nameEntry.focus_set()

    # Create buttons
    submitButton = tk.Button(createFileWin, text="Create",
                              command=lambda: create_file(nameEntry,
                                                          mainTextWidget,
                                                          window
                                                          ))
    
    submitButton.grid(row=2, columnspan=100, pady=(10, 10))
    
    nameEntry.bind("<Return>", on_enter_key)


# Delete file
def confirm_deletion(confirmationText, textWidget, window): 
    if confirmationText == "Delete":
        fileToDelete = read_last_opened_file()
        print(f"{fileToDelete=}")

        if os.path.exists(fileToDelete):
            os.remove(fileToDelete)
            deleteFileWin.destroy()
            print(f"The file {fileToDelete} has been successfully removed.")            
            messagebox.showinfo("Succesfull deletion", "The file was deleted successfully.")

        else:
            print(f"The file {fileToDelete} does not exist.")
            messagebox.showinfo("Deletion failed", "Couldn't delete file. It doesn't exist.")

        goToDefaultFile = FILE_SAVE_DIR + "\\default.snote"
        open_file(textWidget, goToDefaultFile, window)

    else:
        print("Delete confirmation failed")
        messagebox.showinfo("Confirmation failed", "The confirmation text did not match.")


# Creates a confirmation for file deletion
def delete_file_confirmation(textWidget, window):
    # Trigger button with enter
    def on_enter_key(event):
        confirmButton.invoke()

    fileToDelete = read_last_opened_file()

    fileToDelete = fileToDelete.replace("\\", "/")
    fileName = fileToDelete.split("/")[-1].split(".")[0]
    if fileName == "default":
        print("Deletion failed. You can not delete the default note.")
        messagebox.showinfo("Deletion failed", "You can not delete the default note.")
        return


    global deleteFileWin
    deleteFileWin = tk.Toplevel(window)
    deleteFileWin.title("Delete file")
    deleteFileWin.resizable(0, 0)

    # Create header
    headerText = 'Type "Delete" below to confirm note deletion.'
    headerLabel = tk.Label(deleteFileWin, text=headerText, font=("Arial", 10))
    headerLabel.grid(row=0, columnspan=100, pady=(10, 0))

    # Create entry fields
    confirmationEntry = tk.Entry(deleteFileWin)
    confirmationEntry.grid(row=1, column=1, padx=10, pady=(10, 0))
    confirmationEntry.focus_set()

    # Create button
    confirmButton = tk.Button(deleteFileWin, text="Confirm",
                              command= lambda: confirm_deletion(
                                                                confirmationEntry.get(), textWidget, 
                                                                window))
    confirmButton.grid(row=2, columnspan=100, pady=(10, 10))

    confirmationEntry.bind("<Return>", on_enter_key)

