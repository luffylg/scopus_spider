import re

import requests
from bs4 import BeautifulSoup
#decode mail
def strip_email_protection(s):
    fp = re.findall(r'email-protection#[A-Za-z0-9]+', s)
    #parse email
    fp = fp[0].replace('email-protection#','')
    # print(fp)
    r = int(fp[:2], 16)
    email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
    # m = re.sub(r'<a class="__cf_email__".*?</a>', email, s)
    # #strip <script>
    # m = re.sub('<script.*?</script>', '', s, flags = re.DOTALL)
    return email



root='https://www.scopus.com/results/authorNamesList.uri'
#获取sid
def GetSid():
    root2='https://www.scopus.com/'
    a=requests.session()
    b=a.get(root2)
    #print(b.url)
    #print(a.cookies['SCSessionID'])
    return a.cookies['SCSessionID']

Name=input("name: ").replace(',','')
namelist=Name.strip().split()

xing=namelist[-1]
#print('xing: '+xing)
namelist.pop()
ming=" ".join(namelist)
#print('ming: '+ming)
#sid=GetSid()+':360'
#print(sid)
param={'origin':'searchauthorlookup',
       'src':'al',
       'edit':'',
       'poppUp':'',
       'basicTab':'',
       'affiliationTab':'',
       'advancedTab':'',
       'st1':xing,
       'st2':ming,
       'institute':'',
       '_exactSearch':'on',
       'orcidId':'',
       #'authSubject':'LFSC',
       '_authSubject':'on',
       #'authSubject':'HLSC',
        '_authSubject':'on',
        #'authSubject':'PHSC',
        '_authSubject':'on',
        #'authSubject':'SOSC',
        '_authSubject':'on',
        's':'AUTH--LAST--NAME({0}) AND AUTH--FIRST({1})'.format(ming,xing),
        'sdt':'al',
        'sot':'al',
        #'searchId':sid,
        #'sid':sid
       }

ses=requests.session()

s=ses.get(root,params=param)
# print(s.url)
#print(s.cookies)
#cook=s.cookies
soup = BeautifulSoup(s.text, 'html.parser')
span=soup.find_all('span',class_='docTitle')
if(len(span)==0):
    print("找不到人")
    exit()
#输出找到的所有人




authorId=re.findall(r'authorId=\w+&',span[0].a['href'])[0].replace('authorId=','').replace('&','')
# print(authorId)
# 获取作者详细信息页面
s2=ses.get('https://www.scopus.com/authid/detail.uri',params={'authorId':authorId})

# link='https://www.scopus.com'+span[0].a['href']
# print(link)
# s2=requests.get(link)
# print(s2.url)
# print(s2.history)

#print(s2.encoding)
#fout = open('output.html', 'w',encoding="UTF-8")
#fout.write(s2.text)
soup2 = BeautifulSoup(s2.text, 'html.parser')
namesec=soup2.find_all('div',class_='nameSection')
span2=namesec[0].find_all('div',class_='authAffilcityCounty')

namejihe=namesec[0].h1.text.replace(namesec[0].h1.span.text,'').replace('\n','').split(',')
name=namejihe[-1].strip()+' '+namejihe[0]

WenxinNum=soup2.find('a',id='docCntLnk').text
print('文献数：'+WenxinNum)
print(name)
print(str(span2[0].string).strip().replace('\n',' '))

#span3=soup2.find_all('span',class_='docTitle')
ArticlesLink=soup2.find_all('div',class_='authorResultsOptionalLinks')[0].a['href']
# print(ArticlesLink)

#requests redirected, not solved.
param2={
    'sort':'plf-f',
    'src':'s',
    'sid':'E26D65DE7B1033983443731737783381.iqs8TDG0Wy6BURhzD3nFA:1910',
    'sot':'aut',
    'sdt':'a',
    'sl':'18',
    'editSaveSearch':'',
    'txGid':'0'
}
param3={
    'author':'Weirong, Hong',
    'origin':'AuthorProfile',
    'zone':'documentsTab',
    'authorId':'55902039600'
}
s3=ses.get(ArticlesLink)
#s3=ses.get(ArticlesLink,params=param3)
#print(s3.history)
#print(s3.url)
#fout2 = open('output2.html', 'w',encoding="UTF-8")
#fout2.write(s3.text)
soup3=BeautifulSoup(s3.text, 'html.parser')
spanarticle=soup3.find_all('span',class_='docTitle')
for article in spanarticle:

    linka=article.a['href']
    s4=ses.get(linka)
    # print(s4.url)

    #得到年份
    nian=article.parent.parent.find('div',class_='dataCol4').span.text.replace('\n','')



    #fout3 = open('output3.html', 'w',encoding="UTF-8")
    #fout3.write(s4.text)

    soup4=BeautifulSoup(s4.text, 'html.parser')

    highlight=soup4.find_all('span',class_='ScopusTermHighlight')

    emailnotparse=highlight[0].parent.parent.find('a',class_='correspondenceEmail')
    if emailnotparse!=None:
        email=strip_email_protection(emailnotparse['href'])
        print(email)
        print('年份: '+nian)
        break


