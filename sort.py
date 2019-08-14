from queue import Queue
from threading import Thread
import os
import shutil
import re

# --------------------------------------------------------------------
# Get filelist
# select the common of filenames
# mkdir folders to common
# move them
# if need clear empty folder,change the bool
# --------------------------------------------------------------------

threading_num: int = 4


def SortFile(q: Queue):
    while not q.empty():
        a_dict: dict = q.get()
        for Folder in a_dict.keys():
            if os.path.exists(Folder):
                for File in a_dict[Folder]:
                    shutil.move(
                        File, "{folder}/{filename}".format(folder=Folder, filename=File))
            else:
                os.mkdir(Folder)
                print("{folder} is created.".format(folder=Folder))
                for File in a_dict[Folder]:
                    shutil.move(
                        File, "{folder}/{filename}".format(folder=Folder, filename=File))
            print("{folder} is finished.".format(folder=Folder))


def main():
    dirs: list[str] = os.listdir()
    files: list[str] = []
    for i in dirs:
        if os.path.isfile(i):
            files.append(i)
    common_dict: dict[str, list[str]] = {}
    Accepted: bool = False
    while not Accepted:
        pattern: str = input("Keyin pattern : ")
        if not pattern:
            continue
        common_dict.clear()
        for i in files:
            pattern_match_tuple = re.compile(pattern).match(i)
            common_str: str = ""
            if pattern_match_tuple:
                common_str = pattern_match_tuple[0]
            else:
                continue
            if common_str in common_dict:
                common_dict[common_str].append(i)
            else:
                common_dict[common_str] = [i]
        for i in common_dict.keys():
            print(i, " : ", common_dict[i])
        Accepte_receviced: str = input(
            "It is a result of match. Does it right?(nothing key in is Right;anything is error)")
        if not Accepte_receviced:
            Accepted = True
    File_Queue: Queue = Queue()
    for i in common_dict.keys():
        File_Queue.put({i: common_dict[i]})
    threading_list: list[Thread] = []
    for _ in range(threading_num):
        threading_list.append(Thread(target=SortFile, args=(File_Queue,)))
    for i in threading_list:
        i.start()


if __name__ == "__main__":
    try:
        while True:
            main()
    except IOError:
        with open("sortpy.IOError.log", "w") as log:
            log.write(IOError)
    except OSError:
        with open("sortpy.OSError.log", "w") as log:
            log.write(OSError)
    finally:
        print("\n\nIt has a error.\a")
        input()
