import tkinter as tk
from tkinter import filedialog, messagebox
import os
import mvDecryptor

# Create the main window (hidden)
window = tk.Tk()
window.withdraw()

# Display a message explaining what directory to choose
messagebox.showinfo(title="INFORMATION", message="Please select the game directory.\n(The one that contains the main executable)")

# Show a directory selection dialog
game_dir = filedialog.askdirectory(title="Select Game Directory")

# If the user clicks cancel or does not select a directory
if not game_dir:
    # Exit the program
    exit(0)

# Check if System.json exists in the expected path
system_json_path = os.path.join(game_dir, "www", "data", "System.json")
if os.path.exists(system_json_path):
    # Decrypt the game
    mvDecryptor.decrypt_entire_game(game_dir)
    # Show a success message
    messagebox.showinfo(title="INFORMATION", message="DONE!\nGame has been decrypted.\nAn editable file has been created.")
else:
    # Display an error message
    messagebox.showerror(title="ERROR", message="Could not find System.json.\nDid you select the correct directory?")

# Clean up and exit
window.destroy()
exit(0)
