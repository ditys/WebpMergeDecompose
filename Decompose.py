import sys
if len(sys.argv)>1:
    defile=sys.argv[1]
else:
    defile=input("keyin your file path:")
from PIL import Image,ImageSequence

webpf=Image.open(defile)
ite = ImageSequence.Iterator(webpf)
j=1
for i in ite:
    i.save("Result_decompose/"+str(j)+".png","PNG")
    j+=1
