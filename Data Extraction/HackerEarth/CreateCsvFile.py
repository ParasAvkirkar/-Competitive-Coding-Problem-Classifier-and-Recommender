import csv
import os

def CreateCsv(File,Problem):

    for K,V in Problem.items():
        Problem[K]=V.encode("utf-8")
    
    MyFile=open(File,'a')
    W = csv.DictWriter(MyFile, Problem.keys())
    if os.stat(File).st_size==0:
        W.writeheader()
    W.writerow(Problem)        
