from PIL import Image
import os
try:
	os.mkdir("Result")
except:
	print("create Result Error")
ld = os.listdir()
ld = [x for x in ld if x[-4:] in (".png",".PNG")]
for i in ld:
	f = Image.open(i)
	f.save("./Result/"+i,compress_level = 0)
	f.close()