import os,shutil

def four_digits(x):
    if x<10:
        return "000"+str(x)
    if x<100:
        return "00"+str(x)
    if x<1000:
        return "0"+str(x)
    else:
        return str(x)

def three_digits(x):
    if x<10:
        return "00"+str(x)
    if x<100:
        return "0"+str(x)
    else:
        return str(x)

def two_digits(x):
    if x<10:
        return "0"+str(x)
    else:
        return str(x)

filenames = []
for _,_,i in os.walk("."):
    filenames+=i

for i in range(1,24):
    p_file_name = "ev"+three_digits(i) # the string is exist in file‘s name,which is part of cg's name

    os.mkdir(p_file_name)
    for j in filenames:
        if p_file_name in j:
            shutil.move(j,p_file_name)