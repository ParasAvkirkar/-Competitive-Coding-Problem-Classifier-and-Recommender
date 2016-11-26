import urllib
import BeautifulSoup
from CreateCsvFile import CreateCsv
MySoup=BeautifulSoup.BeautifulSoup
Url="https://www.hackerearth.com"

def GetTitle(Soup):
    Temp=Soup.find("div",{"id":"problem-title"})
    return Temp.text

def GetTextAndCons(Soup):
    Body=Soup.find("div",{"class":"starwars-lab"})
    Body=Body.findAll(["p","ul"])
    Flag=0
    Text=""
    Constraints=""
         
    for Tag in Body:
        Temp=Tag.text
        Temp=Temp.lower()
            
        if Temp.find("input")==0:
            Flag=1
        elif Temp.find("constraints")==0:
            Flag=2
        elif Temp.find("sample input")==0:
            Flag=3
            
        if Flag==0:
            Text+=Temp
        elif Flag==2:
            Constraints+=Temp
    return {"Text":Text,"Constraints":Constraints}

def GetExplanation(Soup):
    Explanation=""
    Ex=Soup.find("div",{"class":"less-margin"})
    Explanation+=Ex.text
    if Explanation.find("Memory Limit")!=-1:
        Explanation=""
    return Explanation

def GetTags(Soup):
    Temp=Soup.findAll("span",{"class":"dark small less-margin-right tags-list weight-400"})
    Tags=""
    for t in Temp:
        Tags=Tags+t.text
    return Tags

def GetLimits(Soup):
    Limits=Soup.find("div",{"class":"standard-margin light small problem-guidelines"})
    Limits=Limits.text    
    TlIndex=Limits.find("Time Limit:")
    MlIndex=Limits.find("Memory Limit:")
    SlIndex=Limits.find("Source Limit:")
    MsIndex=Limits.find("Marking Scheme:")
    dic={}
    dic["TimeLimit"]=Limits[TlIndex+len("TimeLimit:"):MlIndex]
    dic["TimeLimit"]=dic["TimeLimit"].split("sec")[0]+"sec"
    dic["MemoryLimit"]=Limits[MlIndex+len("Memory Limit:"):SlIndex]
    dic["MemoryLimit"]=dic["MemoryLimit"].split("MB")[0]+"MB"
    dic["SourceLimit"]=Limits[SlIndex+len("Source Limit:"):MsIndex]
    dic["SourceLimit"]=dic["SourceLimit"].split("KB")[0]+"KB"
    return dic

def ProcessProbs(Catagory,SubCatagory,ProbLinks):
    
    Problem={};
    Problem["Catagory"]=Catagory
    Problem["SubCatagory"]=SubCatagory
    for Link in ProbLinks[:50]:
        Page= urllib.urlopen(Url+Link).read()
        Soup=MySoup(Page)
        
        #get title
        Problem["Title"]=GetTitle(Soup)
        #got title
        
        #get tags
        Problem["Tags"]=GetTags(Soup)
        #got tags
        
        #get limits
        dic=GetLimits(Soup)
        Problem["TimeLimit"]=dic["TimeLimit"]
        Problem["MemoryLimit"]=dic["MemoryLimit"]
        Problem["SourceLimit"]=dic["SourceLimit"]
        #got limits
        
        #get problem text and constraints
        dic=GetTextAndCons(Soup)
        Problem["Text"]=dic["Text"]
        Problem["Constraints"]=dic["Constraints"]
        #got problem text and constraints

        #get explanation
        Problem["Explanation"]=GetExplanation(Soup)
        #got explanation

        #convert to csv
        CreateCsv("HackerEarthData.csv",Problem)
    
def HackerEarth(domain):
    Page= urllib.urlopen(Url+domain).read()
    MainPage=MySoup(Page)
    MainPage=MainPage.find("ul",{"class" : "subtrack-list no-list-style"})
    MainPage=MainPage.findAll("a")
    
    Links=[]
    
    Catagories=[]
    SubCatagories=[]
    
    for Link in MainPage:
        Links.append(Link["href"])
        
    
    for Link in Links:
        
        ProbLinks=[]
        i=1
        Flag=True
        Tokens=Link.split("/")
        if Tokens[-3] not in Catagories:
            Catagories.append(Tokens[-3])
        SubCatagories.append(Tokens[-2])
        
        CurrentCat=Tokens[-3]
        CurrentSubCat=Tokens[-2]
       
        print Link
        Page=urllib.urlopen(Url+Link+"practice-problems/%s/"%i).read()
        Soup=MySoup(Page)
        
        while (Flag==True):
            
            Temp=Soup.findAll("a",{"class":"dark"})
            for t in Temp:
                ProbLinks.append(t["href"])
            i+=1
            Page=urllib.urlopen(Url+Link+"practice-problems/%s/"%i).read()
            Soup=MySoup(Page);
            if Soup.find("link",{"rel":"canonical"})["href"].split("/")[-2]=="1":
                Flag=False

        ProcessProbs(CurrentCat,CurrentSubCat,ProbLinks)
        

#domains for hackerearth
domain1 = "/practice/algorithms"
domain2= "/practice/math"
#domains for hackeearth
HackerEarth(domain1)
HackerEarth(domain2)
