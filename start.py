import os
import mvDecryptor

dir = os.getcwd()
system_json = os.path.join(dir, "www", "data", "System.json")

if os.path.exists(system_json):  # Check System.json exists in cwd
    # Decyption happens here
    mvDecryptor.decrypt_entire_game(dir)
    print("success")
else:
    print(system_json + " not found.")
exit(0)  # Exit the application (avoids memory leaks)
