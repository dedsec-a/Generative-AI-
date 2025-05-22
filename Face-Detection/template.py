import os

folder_names = [
    "known_faces",
    "captured_images",
]

file_names = [
    "main.py",
    "known_faces/user1.png"
    "captured_images/"
]





if __name__ == "__main__":
    for file in folder_names:
     os.makedirs(file , exist_ok=True)
     os.makedirs("main.py")
