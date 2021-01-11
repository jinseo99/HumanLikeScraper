from os import listdir
import os

folder = 'YacStorage/'
allFile = {}

round_ = 0
for item in listdir(folder):
    if item.endswith(".zip"):
        filepath = folder + item
        allFile[item[:-4]] = round(os.path.getsize(filepath), round_)

another_folder = folder+"files/"

for item in listdir(another_folder):
    if item.endswith(".zip"):
        filepath = another_folder + item
        allFile[item[:-4]] = round(os.path.getsize(filepath), round_)

rev_dict = {} 
for key, value in allFile.items(): 
    rev_dict.setdefault(value, set()).add(key)

result = []
for key, values in rev_dict.items():
    if(len(values)>1):
        result.append(key)

result = [key for key, values in rev_dict.items() if len(values) > 1] 


for key in result:
    deleted = False
    """
    for item in list(rev_dict[key]):
        if item.endswith(')'):
            if deleted:
                break
            filepath = folder +item + '.zip'
            print('delete', filepath)
            #os.remove(filepath)
            deleted =True
    """
    if not deleted:
        print("files to consider", rev_dict[key])

print(len(result))