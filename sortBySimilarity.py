import os
import shutil
from PIL import Image
import numpy as np
from typing import *
from scipy import spatial
# --------------------------------------------------------------------
# Get all objects
# select images
# put a lot of images which similarity between 1 to wantSimilarity in a folder
# About Mode skip to next para.
# --------------------------------------------------------------------


def Singleton(Fun):
    ins = {}

    def getSingleton(*args, **kw):
        if Fun not in ins:
            ins[Fun] = Fun(*args, **kw)
        return ins[Fun]
    return getSingleton


@Singleton
class ImageCollections:
    def __init__(self):
        self.imageFile: Dict[str, np.ndarray] = {}
        self.fileGroups: Dict[str, Set[str]] = {}
        self.__groupId: int = -1
        self.wantSimilarity: float = 0.7
        self.simMode: str = "H"

    def __getgroupId(self) -> int:
        self.__groupId += 1
        return self.__groupId

    def getGroupName(self) -> str:
        return "Group%03d" % (self.__getgroupId(),)


def loadImageFile(fs: Set[str]):
    print("---"*10, "Loading Files", "---"*10)
    ic = ImageCollections()
    for i in fs:
        if i[i.rindex("."):] in [".png", ".webp"]:
            try:
                ic.imageFile[i] = np.array(Image.open(i).convert("RGBA"))
            except IOError:
                print("Error Key: { %s }" % (i,))
        else:
            try:
                ic.imageFile[i] = np.array(Image.open(i).convert("RGB"))
            except IOError:
                print("Error Key: { %s }" % (i,))


# --------------------------------------------------------------------
# Mode: H, N
# H (hammingDistance): calculate image's similarity by Hamming
# N (normalAllPixel): calculate image's similarity by Pixel
# --------------------------------------------------------------------
def hammingDistance(img1: np.ndarray, img2: np.ndarray) -> float:
    mean1 = np.mean(img1)
    mean2 = np.mean(img2)
    distance1 = np.greater_equal(img1, mean1)
    distance2 = np.greater_equal(img2, mean2)
    return 1 - spatial.distance.hamming(distance1.flatten(), distance2.flatten())


def normalAllPixel(currentImageFIle, tempImageFile):
    iSimilarity: np.ndarray = np.zeros(
        tempImageFile.shape[:2], np.bool)
    for i in range(len(iSimilarity)):
        for j in range(len(iSimilarity[0])):
            if tempImageFile[i][j].tostring() == currentImageFIle[i][j].tostring():
                iSimilarity[i][j] = True
    return iSimilarity.sum()


def generateFileGroup():
    print("---"*9, "Generate File Group", "---"*9)
    ic = ImageCollections()
    while ic.imageFile:
        tempkey: str = list(ic.imageFile.keys())[0]
        tempGroup: Dict[str, List[str]] = {}
        tempImageFile: Image.Image = ic.imageFile[tempkey]
        tempImageSize = tempImageFile.shape[0] * tempImageFile.shape[1]

        tempGroup[tempkey] = [tempkey]

        for iFile in ic.imageFile:
            if iFile == tempkey:
                continue
            currentImageFIle: np.ndarray = ic.imageFile[iFile]

            if ic.simMode == "N":
                if normalAllPixel(currentImageFIle, tempImageFile)/tempImageSize > ic.wantSimilarity:
                    tempGroup[tempkey].append(iFile)
            elif ic.simMode == "H":
                if hammingDistance(tempImageFile, currentImageFIle) > ic.wantSimilarity:
                    tempGroup[tempkey].append(iFile)

        tempGroupFiles: Set[str] = set()
        for i in tempGroup.values():
            for j in i:
                if not j in tempGroupFiles:
                    tempGroupFiles.add(j)
        for i in tempGroupFiles:
            del ic.imageFile[i]
        print("A group finished.")
        ic.fileGroups[ic.getGroupName()] = tempGroupFiles


def reorganizeFiles():
    print("---"*9, "Reorganize Files", "---"*9)
    ic = ImageCollections()
    for f in ic.fileGroups:
        tempGroup: List[str] = ic.fileGroups[f]
        if not os.path.exists(f):
            os.mkdir(f)
        for item in tempGroup:
            shutil.move(
                item, "{folder}/{filename}".format(folder=f, filename=item))


def main():
    dirs: set[str] = set(os.listdir())
    dirs.remove("sortBySimilarity.py")
    files: set[str] = set()
    for i in dirs:
        if os.path.isfile(i):
            files.add(i)

    ic = ImageCollections()
    ic.wantSimilarity = float(input("want sim(float):"))
    ic.simMode = input("Mode(H,N):")

    # ------------------------------------------------------------
    # Process
    # ------------------------------------------------------------
    loadImageFile(files)
    generateFileGroup()
    reorganizeFiles()

    print("---"*11, "Finished", "---"*11)


if __name__ == "__main__":
    try:
        main()
    except IOError:
        with open("sortBySimilarity.IOError.log", "w") as log:
            log.write(IOError)
    except OSError:
        with open("sortBySimilarity.OSError.log", "w") as log:
            log.write(OSError)
    finally:
        print("\n\nIt has a error.\a")
        input()
