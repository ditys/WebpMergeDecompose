from PIL import Image
import os
import multiprocessing
try:
	os.mkdir("Result")
except:
	print("create Result Error")

def Worker(fs: multiprocessing.Queue, all_task: int):
	while not fs.empty():
		i = fs.get()
		f = Image.open(i)
		f.save("./Result/"+i,compress_level = 0)
		f.close()

if __name__ == "__main__":
	multiprocessing.freeze_support()
	ld = [x for x in os.listdir() if x[-4:] in (".png",".PNG")]
	files = multiprocessing.Queue()
	
	for i in ld:
		files.put(i)
	processList = []
	for _ in range(3):
		processList.append(multiprocessing.Process(target=Worker,args=(files,files.qsize())))
		processList[-1].start()
	for i in processList:
		i.join()