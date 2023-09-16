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


# Check if the save directory exists, create it if not
def ensure_save_directory_exists():
    if os.path.exists(FILE_SAVE_DIR): 
        print(f"Save directory '{FILE_SAVE_DIR}' exists.")
    else:
        os.makedirs(FILE_SAVE_DIR)
        print(f"Save directory '{FILE_SAVE_DIR}' was created.")


# Create a new or update an existing snote.inf file
def create_or_update_snote_inf():
    with open(LAST_SNOTE_INFO_PATH, "w") as file:
        file.write(DEFAULT_FILE_PATH)


# Validate the existence of the snote.inf file and update if needed
def validate_snote_inf_and_update(debug=True):
    # Check if snote.inf file exists
    if not os.path.isfile(LAST_SNOTE_INFO_PATH):
        create_or_update_snote_inf()
        if debug:
            print(f"Created or updated snote.inf with default path: {DEFAULT_FILE_PATH}")
        return

    # Read the last opened path from snote.inf
    with open(LAST_SNOTE_INFO_PATH, "r") as file:
        lastOpenedPath = file.read().rstrip("\n")

    # Check if the last opened path is a valid file
    if not os.path.isfile(lastOpenedPath):
        create_or_update_snote_inf()
        if debug:
            print(f"Invalid file path. Updated snote.inf with default path: {DEFAULT_FILE_PATH}")
    else:
        if debug:
            print(f"snote.inf points to a valid file: {DEFAULT_FILE_PATH}")


# Check if default.snote file exists, create it if not
def ensure_default_snote_exists():
    # Check if the default snote file already exists
    if os.path.isfile(DEFAULT_FILE_PATH):
        print(f"Default file '{DEFAULT_FILE_PATH}' exists.")

    else:
        # If it doesn't exist, create it
        with open(DEFAULT_FILE_PATH, "w") as file:
            text = ("Welcome to Sticky Notes by Time\n\n"
                    "Here you can save, open, create, and remove Sticky Notes files.\n\n"
                    "However, you cannot save changes to this default file.\n\n"
                    "Enjoy!")
            
            file.write(text)


# Perform startup file validation
def startup_file_validation():
    ensure_save_directory_exists()
    validate_snote_inf_and_update(True)
    ensure_default_snote_exists()


# Reads the last oppened file
def read_last_opened_file(debug = True):
    validate_snote_inf_and_update(debug)

    with open(LAST_SNOTE_INFO_PATH, "r") as file:
        return file.readline()
   

# Changes window title
def change_title(window, filePath, addAsterix = False):
    editedFilePath = filePath.replace("\\", "/")
    windowTitle = "Notes  |  " + editedFilePath.split("/")[-1].split(".")[0]

    if addAsterix:
        windowTitle = "*" + windowTitle

    window.title(windowTitle)


# Saves current file
def save_file(textWidget, window, shouldShowConfirm = True):
    openFile = read_last_opened_file()

    openFile = openFile.replace("\\", "/")
    fileName = openFile.split("/")[-1].split(".")[0]
    text = textWidget.get("1.0", tk.END)

    if fileName == "default":
        print("Save failed. You can not edit the default note.")
        messagebox.showinfo("Save failed", "You can not edit the default note.")
        return

    # Save file
    try:
        with open(openFile, "w") as file:
                if text.endswith('\n'):  # Remove the trailing newline character
                    text = text[:-1]  
                file.write(text)

        change_title(window, openFile, addAsterix = False)
        print(f"{openFile} successfully saved.")

        if shouldShowConfirm:
            messagebox.showinfo("Succesfully saved", "File saved successfully.")

    # Failed to save file
    except:
        print(f"Error: Couldn't save {openFile}")
        messagebox.showinfo("Save failed", "File failed to save.")
        raise


# Opens a file
def open_file(textWidget, filePath, window):
    # Check if a file path is provided; if not, prompt the user to select a file
    if filePath is None:
        filePath = filedialog.askopenfilename(
            initialdir=FILE_SAVE_DIR,
            filetypes=[("Sticky Note File", "*.snote")]
        )
        
        # Check if the user canceled the file dialog
        if not filePath:
            print("File open canceled by the user.")
            return 
    
    try:
        # Try to open the selected file
        with open(filePath, "r") as file:
            loadedText = file.read()
        
        # Change the window title to reflect the opened file
        change_title(window, filePath)

    except:
        # Handle exceptions if the file cannot be opened
        print(f"Error: Couldn't read {filePath}")
        print("Trying to open {DEFAULT_FILE_PATH} instead.")

        # Ensure necessary directories and default file exist
        ensure_save_directory_exists()
        ensure_default_snote_exists()

        try:
            # Try to open the default file
            with open(DEFAULT_FILE_PATH, "r") as file:
                loadedText = file.read()
                  
            # Change the window title to the default file
            change_title(window, DEFAULT_FILE_PATH)

        except:
            # Handle exceptions if the default file cannot be opened
            print("Error: Couldn't read {DEFAULT_FILE_PATH}")
            messagebox.showinfo("Read failed", "Couldn't read file.")
            raise
            
    finally:
        # Display a success message and load the file's content into the text widget
        print(f'Successfully read {filePath}')
        textWidget.delete("1.0", tk.END)
        textWidget.insert(index=1.0, chars=loadedText)

        try:
            # Update the path of the last opened file
            with open(LAST_SNOTE_INFO_PATH, "w") as file:
                file.write(filePath)
        
        except:
            # Handle exceptions if the path cannot be updated
            print("Error: Couldn't write to {LAST_SNOTE_INFO_PATH}")
            messagebox.showinfo("Write failed", "Couldn't write to file.")
            raise

    
# Create new note file
def create_file(textWidget, mainTextWidget, window):
    ensure_save_directory_exists()
    fileName = textWidget.get()
    fileExt = ".snote"
    filePath = f"{FILE_SAVE_DIR}\\{fileName}{fileExt}"

    # Check if file already exists
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
    # Confirm deletion
    if confirmationText == "Delete":
        fileToDelete = read_last_opened_file()
        print(f"{fileToDelete=}")

        # Check if file exists and delete
        if os.path.exists(fileToDelete):
            os.remove(fileToDelete)
            deleteFileWin.destroy()
            print(f"The file {fileToDelete} has been successfully removed.")            
            messagebox.showinfo("Succesfull deletion", "The file was deleted successfully.")

        else:
            print(f"The file {fileToDelete} does not exist.")
            messagebox.showinfo("Deletion failed", "Couldn't delete file. It doesn't exist.")

        # Open default file after deletion
        goToDefaultFile = FILE_SAVE_DIR + "\\default.snote"
        open_file(textWidget, goToDefaultFile, window)

    # Deletion confirmaiton failed
    else:
        print("Delete confirmation failed")
        messagebox.showinfo("Confirmation failed", "The confirmation text did not match.")
        

# Creates a confirmation for file deletion
def create_delete_confirmation_window(textWidget, window):
    
    # Trigger button with enter
    def on_enter_key(event):
        confirmButton.invoke()

    fileToDelete = read_last_opened_file()

    fileToDelete = fileToDelete.replace("\\", "/")
    fileName = fileToDelete.split("/")[-1].split(".")[0]
    if fileName == "default":
        print("Deletion failed. You cannot delete the default note.")
        messagebox.showinfo("Deletion failed", "You cannot delete the default note.")
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
                              command=lambda: confirm_deletion(
                                  confirmationEntry.get(), textWidget,
                                  window))
    confirmButton.grid(row=2, columnspan=100, pady=(10, 10))

    confirmationEntry.bind("<Return>", on_enter_key)


# Check if file has been edited
def is_file_edited(textWidget) -> bool:
    openFile = read_last_opened_file(False)
    textWidgetText = textWidget.get("1.0", "end-1c")
    
    try:
        with open(openFile, "r") as file:
            openFileText = file.read()       

    except:
        print(f"{openFile} failed to open as read.")
        raise

    return not textWidgetText == openFileText


# Add asterix if file is changed
def update_title(textWidget, window):
    isFileEdited = is_file_edited(textWidget)
    openFile = read_last_opened_file(False)

    if isFileEdited:
        change_title(window, openFile, addAsterix=True)
    
    else:
        change_title(window, openFile, addAsterix=False)


# Ask "Do you want to save before you..."
def handle_note_action(action, textWidget, window):
    isFileEdited = is_file_edited(textWidget)

    # No changes; procede
    if not isFileEdited:
        if action == "close":
            window.destroy()
        elif action == "open":
            open_file(textWidget, None, window)
        elif action == "create":
            create_file_gui(textWidget, window)
    
    # changes made; suggest save
    else:
        modalMessage = "Do you want to save changes before you {} note?"
        modalTitle = "Note not saved"
        modalAnswer = messagebox.askyesnocancel(modalTitle, modalMessage.format(action))

        # Don't save; procede
        if modalAnswer == False:
            if action == "close":
                window.destroy()
            elif action == "open":
                open_file(textWidget, None, window)
            elif action == "create":
                create_file_gui(textWidget, window)

        # Save and procede
        elif modalAnswer == True:
            save_file(textWidget, window, shouldShowConfirm=False)
            if action == "close":
                window.destroy()
            elif action == "open":
                open_file(textWidget, None, window)
            elif action == "create":
                create_file_gui(textWidget, window)

        # Cancel
        else: 
            print("User canceled {}.".format(action))

