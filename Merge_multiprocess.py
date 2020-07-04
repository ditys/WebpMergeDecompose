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
import multiprocessing

all_task: int = 0


def Worker(fs: Queue, all_task: int):
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
        ctypes.windll.kernel32.SetConsoleTitleW(
            "Process [{0}/{1}]".format(all_task-fs.qsize(), all_task))

def main():
    threading_number: int = 10
    threading_list: list[multiprocessing.Process] = []
    ctypes.windll.kernel32.SetConsoleTitleW(sys.argv[0])
    folders = []
    for i in os.listdir("MergePhotos/"):
        folders += [i]
    all_task = len(folders)
    try:
        files = multiprocessing.Queue()
        for i in folders:
            files.put(i)
        if not os.path.exists("Result_merge"):
            os.mkdir("Result_merge")
        for _ in range(threading_number):
            threading_list += [multiprocessing.Process(
                target=Worker, args=(files, all_task))]
            threading_list[-1].start()
        for i in threading_list:
            i.join()
    except IOError:
        input("\n\n\nSomething Error.\a", IOError)
        exit()

    print("\n\nFinish all task.")
    time.sleep(2)
    exit()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
