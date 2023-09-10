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


class ImageItem:
    mean: np.ndarray
    distance: np.ndarray
    img: np.ndarray
    def __init__(self, mean: np.ndarray, distance: np.ndarray) -> None:
        self.mean = mean
        self.distance = distance


@Singleton
class ImageCollections:
    def __init__(self):
        self.imageFile: Dict[str, ImageItem] = {}
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
        try:
            img:np.ndarray
            # if i[i.rindex("."):] in [".png", ".webp"]:
            #     ic.imageFile[i] = np.array(Image.open(i).convert("RGBA"))
            # else:
            #     ic.imageFile[i] = np.array(Image.open(i).convert("RGB"))
            if i[i.rindex("."):] in [".png", ".webp"]:
                img = np.array(Image.open(i).convert("RGBA"))
            else:
                img = np.array(Image.open(i).convert("RGB"))
            m = np.mean(img)
            d = np.greater_equal(img,m)
            imgItem:ImageItem = ImageItem(mean=m,distance=d)
            imgItem.img = img
            ic.imageFile[i] = imgItem
        except IOError:
            print("Error Key: { %s }" % (i,))


# --------------------------------------------------------------------
# Mode: H, N
# H (hammingDistance): calculate image's similarity by Hamming
# N (normalAllPixel): calculate image's similarity by Pixel
# --------------------------------------------------------------------
def hammingDistance(img1: ImageItem, img2: ImageItem) -> float:
    return 1 - spatial.distance.hamming(img1.distance.flatten(), img2.distance.flatten())


def normalAllPixel(currentImageFIle:ImageItem, tempImageFile:ImageItem):
    iSimilarity: np.ndarray = np.zeros(
        tempImageFile.img.shape[:2], np.bool)
    for i in range(len(iSimilarity)):
        for j in range(len(iSimilarity[0])):
            if tempImageFile.img[i][j].tostring() == currentImageFIle.img[i][j].tostring():
                iSimilarity[i][j] = True
    return iSimilarity.sum()


def generateFileGroup():
    print("---"*9, "Generate File Group", "---"*9)
    ic = ImageCollections()
    while ic.imageFile:
        tempkey: str = list(ic.imageFile.keys())[0]
        tempGroup: Dict[str, List[str]] = {}
        tempImageFile: ImageItem = ic.imageFile[tempkey]
        tempImageSize:int = tempImageFile.img.shape[0] * tempImageFile.img.shape[1]

        tempGroup[tempkey] = [tempkey]

        for iFile in ic.imageFile:
            if iFile == tempkey:
                continue
            currentImageFIle: ImageItem = ic.imageFile[iFile]

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
        print("{0} group finished.".format(tempkey))
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
    files: set[str] = set((x for x in dirs if os.path.isfile(x)))

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
