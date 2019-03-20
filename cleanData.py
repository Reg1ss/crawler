import os
import filetype

def getEnds(path):
    ends = []
    for file in os.listdir(path):
        print(file)
        end = filetype.guess('/home/kuangrx/pics/results_baidu/1')
        if end not in ends:
            ends.append(end)
    return ends

def del_files(path):
    for root , dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png") or name.endswith(".gif"):   #指定要删除的格式
                os.remove(os.path.join(root, name))
                print ("Delete File: " + os.path.join(root, name))
# test
if __name__ == "__main__":
    path = '/home/kuangrx/pics/results_baidu'
    #del_files(path)
    print(getEnds(path))