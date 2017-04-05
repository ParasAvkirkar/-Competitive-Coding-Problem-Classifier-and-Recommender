import urllib2
import sys, os
from bs4 import BeautifulSoup

sys.path.append("../Utilities")
sys.path.append("../DataBase")
from sqlDB import connect_db
from retrying import retry

dic={}


@retry(wait_fixed=2000)
def MyUrlOpen(x):
    print(x)
    return urllib2.urlopen(x)

def ExtractUser(Url,handle):
    Page = MyUrlOpen(Url)
    Page = BeautifulSoup(Page, 'html.parser')
    Page=Page.find('table')
    Page = Page.find('tbody')
    rows = Page.findAll('tr')
    SubCnt={}
    date={}
    for row in rows:
        cols=row.findAll('td')
        if(cols[5].text.find("100")!=-1):
            date[cols[3].text]=cols[1].text
        try:
            SubCnt[cols[3].text]+=1
        except:
            SubCnt[cols[3].text]=1

    db = connect_db()
    cursor=db.cursor()
    for key in date:
        q="INSERT INTO codechef_prob_user_map (uname,prob_code,date,no_of_submissions) VALUES ('"+handle+"','"+key+"','"+date[key]+"','"+str(SubCnt[key])+"')"
        if(cursor.execute(q)==1):
            db.commit()
            print("success db")
        else:
            print("fail db")
    db.close()


def CreateLink():
    f = open('users_ids.txt', 'r')
    link0="https://www.codechef.com/submissions?page="
    link1="&sort_by=All&sorting_order=asc&language=All&status=All&year="
    link2="&handle="
    link3="&pcode=&ccode=&Submit=GO"
    cnt=0
    for handle in f:
        handle=handle.split("\n")[0]
        print(handle+"#"+str(cnt))
        cnt+=1;
        for year in range(2009,2018):
            Page=MyUrlOpen(link0+"0"+link1+str(year)+link2+handle+link3)
            Page=BeautifulSoup(Page,'html.parser')
            pages=Page.find('div',{'class':'pageinfo'})
            if(pages):
                pages=pages.text.split(" ")[2]
                pages=int(pages)
                for p in range(0,pages):
                    ExtractUser(link0+str(p)+link1+str(year)+link2+handle+link3,handle)

CreateLink()