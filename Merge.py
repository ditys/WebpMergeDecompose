try:
    from PIL import Image
except:
    print("pip install Pillow")
    exit()
import os,time,ctypes,sys

ctypes.windll.kernel32.SetConsoleTitleW(sys.argv[0])

folders=[]
for i in os.listdir("MergePhotos/"):
    folders += [i]
try:
    for the_folder in folders:
        if os.path.isdir("MergePhotos/"+the_folder):
            print(the_folder+" is starting ... "+"Process:"+str(folders.index(the_folder)+1)+"/"+str(len(folders)),end="\r")
            filenames=[]
            for _,_,i in os.walk("MergePhotos/"+the_folder+"/"):
                filenames += i
            filestreams = []
            for i in filenames:
                filestreams+=[Image.open("MergePhotos/"+the_folder+"/"+i)]
            if not os.path.exists("Result_merge"):
                os.mkdir("Result_merge")
            filestreams[0].save("Result_merge/"+the_folder+".webp","WEBP",save_all=True,append_images=filestreams[1:],lossless=True)
            print("Folder: ",the_folder ," finished. "+"["+str(folders.index(the_folder)+1)+"/"+str(len(folders))+"]                                                                ")
        else :
            print(the_folder+" starting..."+"Process:"+str(folders.index(the_folder)+1)+"/"+str(len(folders)),end="\r")
            temp=Image.open("MergePhotos/"+the_folder)
            if not os.path.exists("Result_merge"):
                os.mkdir("Result_merge")
            temp.save("Result_merge/"+the_folder+".webp","WEBP",quality=100)
            print(the_folder,"finished.  "+"["+str(folders.index(the_folder)+1)+"/"+str(len(folders))+"]                               ")
except:
    input("\n\n\nSomething Error.\a")
    exit()

print("\n\nFinish all task.")
time.sleep(2)
exit()