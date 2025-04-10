
import os
import sys

import tkinter as tk
from tkinter import filedialog, messagebox

import mvDecryptor


def decrypt_game(resource_dir):
    # Decrypt the game
    mvDecryptor.decrypt_entire_game(resource_dir)
    # Show a success message
    messagebox.showinfo(title="INFORMATION", message="DONE!\nGame has been decrypted.\nAn editable file has been created.")  # noqa: E501


# Create the main window (hidden)
window = tk.Tk()
window.withdraw()

# Display a message explaining what directory to choose
messagebox.showinfo(title="INFORMATION", message="Please select the game directory.\n(The one that contains the main executable)")  # noqa: E501

# Show a directory selection dialog
game_dir = filedialog.askdirectory(title="Select Game Directory")

# If the user clicks cancel or does not select a directory
if not game_dir:
    # Exit the program
    sys.exit(0)

# Check if System.json exists in the expected path
if os.path.exists(os.path.join(game_dir, "www", "data", "System.json")):
    mvDecryptor.SYSTEM_JSON_PATH = os.path.join(game_dir, "www", "data", "System.json")  # noqa: E501
    mvDecryptor.BASE_DIR = os.path.join(game_dir, "www")
    decrypt_game(mvDecryptor.BASE_DIR)
elif os.path.exists(os.path.join(game_dir, "data", "System.json")):
    mvDecryptor.SYSTEM_JSON_PATH = os.path.join(game_dir, "data", "System.json")  # noqa: E501
    mvDecryptor.BASE_DIR = game_dir
    decrypt_game(mvDecryptor.BASE_DIR)
else:
    # Display an error message
    messagebox.showerror(title="ERROR", message="Could not find System.json.\nDid you select the correct directory?")  # noqa: E501

# Clean up and exit
window.destroy()
sys.exit(0)
