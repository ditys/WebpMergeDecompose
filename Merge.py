from PIL import Image,ImageSequence
import os

folders=[]
for _,i,_ in os.walk("MergePhotos/"):
    folders += i
try:
    for the_folder in folders:
        print(the_folder+" is starting...",end="\r")
        filenames=[]
        for _,_,i in os.walk("MergePhotos/"+the_folder+"/"):
            filenames += i
        filestreams = []
        for i in filenames:
            filestreams+=[Image.open("MergePhotos/"+the_folder+"/"+i)]
        filestreams[0].save("Result_merge/"+the_folder+".webp","WEBP",save_all=True,append_images=filestreams[1:])
        print("Folder: ",the_folder ," finished.          ")
except:
    print(the_folder)

filenames=[]
for _,_,i in os.walk("MergePhoto/"):
    filenames += i
filestreams = []
for i in filenames:
    print(i+" starting...",end="\r")
    temp=Image.open("MergePhoto/"+i)
    temp.save("Result_merge/"+i+".webp","WEBP")
    print(i,"finished.                                 ")