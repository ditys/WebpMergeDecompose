# ver 0.1
from PIL import Image
import os
import copy

def main():
    dirs = os.listdir()
    folders = []
    for i in dirs:
        if os.path.isdir(i):
            folders.append(i)
    if not "background" in folders:
        print("background is not EXISTS!\a")
        input()
        return 0
    folders.remove("background")
    if not os.path.exists("Result"):
        os.mkdir("Result")
    print("   -- Work Start --   ")
    for b in os.listdir("background"):
        background_photo = Image.open("./background/"+b)
        for i in folders:
            for f in os.listdir(i):
                part = Image.open("{}/{}".format(i,f))
                background_photo_copy = copy.deepcopy(background_photo)
                background_photo_copy.paste(part,(0,0),part)
                background_photo_copy.save("./Result/"+b[:b.rindex(".")]+"___"+f,f[f.rindex(".")+1:])
                del background_photo_copy

if __name__ == "__main__":
    main()