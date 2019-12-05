try:
    from PIL import Image
except:
    print("pip install Pillow")
    exit()
import os
import time
import ctypes
import sys

ctypes.windll.kernel32.SetConsoleTitleW(sys.argv[0])

folders = []
for i in os.listdir("DecomposePhotos/"):
    folders += [i]
file_ext = input("file ext: ")

try:
    for the_folder in folders:
        if not os.path.isdir("DecomposePhotos/"+the_folder):
            print(the_folder+" starting..."+"Process:" +
                  str(folders.index(the_folder)+1)+"/"+str(len(folders)), end="\r")
            temp = Image.open("DecomposePhotos/"+the_folder)
            if not os.path.exists("Result_decompose"):
                os.mkdir("Result_decompose")
            temp.save("Result_decompose/%s.%s" %
                      (the_folder[:the_folder.rindex(".")], file_ext), file_ext)
            print(the_folder, "finished.  "+"["+str(folders.index(the_folder)+1)+"/"+str(
                len(folders))+"]                               ")
except:
    input("\n\n\nSomething Error.\a")
    exit()

print("\n\nFinish all task.")
time.sleep(2)
exit()
