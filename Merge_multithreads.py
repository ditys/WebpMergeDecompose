try:
    from PIL import Image
except:
    print()
    print("pip install Pillow")
    exit()
from queue import Queue
import os
import time
import ctypes
import sys
import threading

from threading import Thread


def Worker(fs: Queue):
    # for the_folder in folders:
    while not fs.empty():
        the_folder = fs.get()
        if os.path.isdir("MergePhotos/"+the_folder):
            filenames = []
            for _, _, i in os.walk("MergePhotos/"+the_folder+"/"):
                filenames += i
            filestreams = []
            for i in filenames:
                filestreams += [Image.open("MergePhotos/"+the_folder+"/"+i)]
            filestreams[0].save("Result_merge/"+the_folder+".webp",
                                "WEBP", save_all=True, append_images=filestreams[1:])
            print("Folder: ", the_folder, " finished. ")
        else:
            temp = Image.open("MergePhotos/"+the_folder)
            temp.save("Result_merge/"+the_folder+".webp", "WEBP")
            print(the_folder, "finished.  ")


def main():
    threading_number: int = 10
    threading_list: list[Thread] = []
    ctypes.windll.kernel32.SetConsoleTitleW(sys.argv[0])
    folders = []
    for i in os.listdir("MergePhotos/"):
        folders += [i]
    try:
        files = Queue()
        for i in folders:
            files.put(i)
        if not os.path.exists("Result_merge"):
            os.mkdir("Result_merge")
        for _ in range(threading_number):
            threading_list += [Thread(target=Worker, args=(files,))]
        for i in threading_list:
            i.start()
        for i in threading_list:
            i.join()
    except IOError:
        input("\n\n\nSomething Error.\a", IOError)
        exit()

    print("\n\nFinish all task.")
    time.sleep(2)
    exit()


main()
