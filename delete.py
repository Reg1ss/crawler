import os

rootdir = '/home/kuangrx/PycharmProjects/crawler/results'
list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i in range(0,len(list)):
       path = os.path.join(rootdir,list[i])
       if os.path.isfile(path):
           fsize = os.path.getsize(path)
           print('id:',list[i])
           print('size:',fsize)
           countFile = 0
           if fsize==0:
               newname = 'f'+ countFile + '.jpg'
               countFile+=1
               os.rename(path+"/"+list[i], path+"/"+newname)