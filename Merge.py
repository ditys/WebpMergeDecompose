from PIL import Image
import os,time

folders=[]
for _,i,_ in os.walk("MergePhotos/"):
    folders += i
try:
    for the_folder in folders:
        print(the_folder+" is starting..."+"Process:"+str(folders.index(the_folder)+1)+"/"+str(len(folders)),end="\r")
        filenames=[]
        for _,_,i in os.walk("MergePhotos/"+the_folder+"/"):
            filenames += i
        filestreams = []
        for i in filenames:
            filestreams+=[Image.open("MergePhotos/"+the_folder+"/"+i)]
        if not os.path.exists("Result_merge"):
            os.mkdir("Result_merge")
        filestreams[0].save("Result_merge/"+the_folder+".webp","WEBP",save_all=True,append_images=filestreams[1:])
        print("Folder: ",the_folder ," finished. "+"["+str(folders.index(the_folder)+1)+"/"+str(len(folders))+"]                                                                ")
except:
    input("\n",the_folder)

filenames=[]
for _,_,i in os.walk("MergePhoto/"):
    filenames += i
filestreams = []
for i in filenames:
    print(i+" starting..."+"Process:"+str(filenames.index(i)+1)+"/"+str(len(filenames)),end="\r")
    temp=Image.open("MergePhoto/"+i)
    if not os.path.exists("Result_merge"):
        os.mkdir("Result_merge")
    temp.save("Result_merge/"+i+".webp","WEBP")
    print(i,"finished.  "+"["+str(filenames.index(i)+1)+"/"+str(len(filenames))+"]                               ")
print("\n\nFinish all task.")
time.sleep(2)
exit()