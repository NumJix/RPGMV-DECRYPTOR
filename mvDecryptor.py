# RPG Maker MV Decryption Script
#
# Created By SilicaAndPina 1/12/2018
#
#

import binascii
import os


def xor(data, key):
    """XOR Encryption / Decryption Algorithm"""
    ln = len(key)
    # Do complex MATH stuff and return the converted the result to a bytearray.
    return bytearray(((data[i] ^ key[i % ln]) for i in range(0, len(data))))


def find_key(game_dir: str):
    """Function for finding decryption key in game folder from System.json"""
    key = open(os.path.join(game_dir, "www", "data", "System.json"), "rb").read()
    key = key[key.index(b'"encryptionKey":"')+len(b'"encryptionKey":"'):]
    key = key[:key.index(b'"}')]
    # return Decoded Hexadecimal and converted to ByteArray key.
    return bytearray(binascii.unhexlify(key))


def decrypt_file_name(encrypted_file_name: str):
    """Function for "Decrypting" a filename
    `.rpgmo`: `.ogg`
    `.rpgmvm`: `.m4a`
    `.rpgmvp`: `.png`"""
    if encrypted_file_name.endswith(".rpgmvo"):
        return encrypted_file_name[:-7]+".ogg"
    if encrypted_file_name.endswith(".rpgmvm"):
        return encrypted_file_name[:-7] + ".m4a"
    if encrypted_file_name.endswith(".rpgmvp"):
        return encrypted_file_name[:-7] + ".png"
    if encrypted_file_name[-4:-1] in ["ogg", "m4a", "png"]:
        return encrypted_file_name[:-1]


def is_encrypted_file(path):
    """Function for determining if the specified path is an Encrypted RMMV File
    Types of RMMV file - [rpgmvo, rpgmvm, rpgmvp]"""
    if path.endswith(".rpgmvo"):
        return True
    if path.endswith(".rpgmvm"):
        return True
    if path.endswith(".rpgmvp"):
        return True
    if path[-4:-1] in ["ogg", "m4a", "png"]:
        return True


def decrypt_file_and_save(encrypted_file_name: str, key: bytearray):
    """Function for decrypting a file and writing it"""
    dfile = decrypt_file_name(encrypted_file_name)
    ctime = os.stat(encrypted_file_name).st_mtime
    file = open(encrypted_file_name, "rb").read()  # Read encrypted file.
    file = file[16:]  # Remove file header.
    cyphertext = bytearray(file[:16])  # Read encrypted file header
    plaintext = bytearray(xor(cyphertext, key))  # Decrypt file header
    file = file[16:]  # Remove decrypted file header
    with open(dfile, "wb") as wt:
        # Write decrypted file header +
        # rest of file to disk as Decrypted Filename
        wt.write(plaintext + file)
    os.utime(dfile, (ctime, ctime))


def decrypt_entire_game(game_dir):
    """Function for decrypting an entire game folder"""
    # Find Decryption Key
    key = find_key(game_dir)
    # Loop through all files inside the Game's project folder.
    for path, dirs, files in os.walk(os.path.join(game_dir, "www")):
        for f in files:  # For all files in Game's WWW folder.
            if is_encrypted_file(os.path.join(path, f)):
                decrypt_file_and_save(os.path.join(path, f), key)
                os.remove(os.path.join(path, f))  # Delete encrypted file
    SystemJson = open(os.path.join(game_dir, "www", "data", "System.json"), "rb").read()
    SystemJson = SystemJson.replace(
        b'"hasEncryptedImages":true',
        b'"hasEncryptedImages":false')  # Sets hasEncryptedImages to FALSE
    SystemJson = SystemJson.replace(
        b'"hasEncryptedAudio":true',
        b'"hasEncryptedAudio":false')  # Sets hasEncryptedAudio to FALSE
    with open(os.path.join(game_dir, "www", "data", "System.json"), "wb") as wt:
        wt.write(SystemJson)  # Writes new System.json to disk
    with open(os.path.join(game_dir, "www", "Game.rpgproject"), "wb") as wt:
        wt.write(b"RPGMV 1.0.0")  # Creates Editable RPG Maker MV Project File
