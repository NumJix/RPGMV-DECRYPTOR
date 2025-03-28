import os
import mvDecryptor

dir = os.getcwd()
if os.path.exists(os.path.join(dir, "www", "data", "System.json")):
    mvDecryptor.SYSTEM_JSON_PATH = os.path.join(dir, "www", "data", "System.json")  # noqa: E501
    mvDecryptor.BASE_DIR = os.path.join(dir, "www")
elif os.path.exists(os.path.join(dir, "data", "System.json")):
    mvDecryptor.SYSTEM_JSON_PATH = os.path.join(dir, "data", "System.json")
    mvDecryptor.BASE_DIR = dir
else:
    print('System.Json' + " not found.")


if os.path.exists(mvDecryptor.SYSTEM_JSON_PATH):  # Check System.json exists in cwd # noqa: E501
    # Decyption happens here
    mvDecryptor.decrypt_entire_game(mvDecryptor.BASE_DIR)
    print("success")
else:
    print("Failed")
exit(0)  # Exit the application (avoids memory leaks)
