import os

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

    os.system("mkdir "+p_file_name)
    for j in filenames:
        if p_file_name in j:
            os.system("move "+j+" "+p_file_name)

