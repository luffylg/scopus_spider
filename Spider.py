import re
import requests
from bs4 import BeautifulSoup

import html_downloader
import html_outputer
import html_parser





class SpiderMain(object):
    def __init__(self,xing,ming):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.xing=xing
        self.ming=ming
        self.param={'origin':'searchauthorlookup',
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

    def craw(self):
        root='https://www.scopus.com/results/authorNamesList.uri'
        ses=requests.session()#创建session
        s=ses.get(root,params=self.param)#搜索得到作者列表页面
        AuthorID=self.parser.GetAuthorId(s)#获取authorid
        if(AuthorID==False):
            return

        else:
            self.crawel(ses,AuthorID)

    def crawel(self,ses, AuthorID):
        s2=ses.get('https://www.scopus.com/authid/detail.uri',params={'authorId':AuthorID})# 获取作者详细信息页面
        message=self.parser.GetAuthorMessage(s2)#获取详细信息
        wenxin=message[0]
        AuthorName=message[1]
        area=message[2]
        lishi=message[4]
        if int(wenxin)<10:#文献数少于10，直接返回
            print('文献数为'+wenxin+'，不符合要求')
            return
        print('文献数：'+wenxin+' '+lishi)
        print(AuthorName)
        print(area)
        Articlelink=message[3]#获取作者所有文章页面链接
        s3=ses.get(Articlelink)#获取作者所有文章页面
        Articles=self.parser.GetArticles(s3)#获得所有文章链接及年份列表
        for lists in Articles:
            link=lists[0]
            nian=lists[1]
            s4=ses.get(link)#获取文章详细信息页面
            emailnotparse=self.parser.GetEmail(s4)#得到加密的邮件地址
            if emailnotparse!=None:
                email=strip_email_protection(emailnotparse['href'])
                print(email)
                print('年份: '+nian+'\n')
                break

class WenxianSpiderMain(object):
    def __init__(self,wenxian):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.wenxian=wenxian
        self.wenxianparse=self.wenxian.replace(' ','+')
        self.param={
            'numberOfFields':'0',
            'src':'s',
            'clickedLink':'',
            'edit':'',
            'editSaveSearch':'',
            'origin':'searchbasic',
            'authorTab':'',
            'affiliationTab':'',
            'advancedTab':'',
            'scint':'1',
            'menu':'search',
            'tablin':'',
            'searchterm1':self.wenxianparse,
            'field1':'TITLE_ABS_KEY',
            'dateType':'Publication_Date_Type',
            'yearFrom':'Before+1960',
            'yearTo':'Present',
            'loadDate':'7',
            'documenttype':'All',
            'subjects':'LFSC',
            '_subjects':'on',
            'subjects':'HLSC',
            '_subjects':'on',
            'subjects':'PHSC',
            '_subjects':'on',
            'subjects':'SOSC',
            '_subjects':'on',
            'st1':self.wenxianparse,
            'st2':'',
            'sot':'b',
            'sdt':'b',
            'sl':'101',
            's':'TITLE-ABS-KEY%28'+self.wenxianparse+'%29',
            #'sid':0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            #searchId:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            #txGid:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A15
            'sort':'plf-f',
            'originationType':'b',
            'rr':''
        }

        self.param2={
            'numberOfFields':'0',
            'src':'s',
            'clickedLink':'',
            'edit':'',
            'editSaveSearch':'',
            'origin':'searchbasic',
            'authorTab':'',
            'affiliationTab':'',
            'advancedTab':'',
            'scint':'1',
            'menu':'search',
            'tablin':'',
            'searchterm1':self.wenxian,
            'field1':'TITLE_ABS_KEY',
            'dateType':'Publication_Date_Type',
            'yearFrom':'Before 1960',
            'yearTo':'Present',
            'loadDate':'7',
            'documenttype':'All',
            'authSubject':'LFSC',
           '_authSubject':'on',
           'authSubject':'HLSC',
            '_authSubject':'on',
            'authSubject':'PHSC',
            '_authSubject':'on',
            'authSubject':'SOSC',
            '_authSubject':'on',
            'st1':self.wenxian,
            'st2':'',
            'sot':'b',
            'sdt':'b',
            'sl':'101',
            's':'TITLE-ABS-KEY({0})'.format(self.wenxian),
            # sid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # searchId:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # txGid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:7
            'sort':'plf-f',
            'originationType':'b',
            'rr':''
        }

    #输入文献名称爬取

    def craw(self):
        root='https://www.scopus.com/results/results.uri'
        ses=requests.session()#创建session
        s=ses.get(root,params=self.param2)#搜索得到文献列表页面
        soup = BeautifulSoup(s.text, 'html.parser')
        span=soup.find_all('span',class_='docTitle')
        if len(span)==0:
            print("找不到文献")
            return
        elif len(span)==1:
            link=span[0].a['href']
        else:
            bianhao=0
            links=[]
            mark=0
            link=''
            for spans in span:
                bianhao+=1
                links.append(spans.a['href'])
                biaoti=spans.a.text.strip().replace('\n','')
                if biaoti==self.wenxian:
                    mark=1
                    link=spans.a['href']
                    break
                zuozhemen=spans.parent.parent.find('div',class_='dataCol3').span.text.strip().replace('\n','')
                nian=spans.parent.parent.find('div',class_='dataCol4').span.text.strip().replace('\n','')
                if spans.parent.parent.find('div',class_='dataCol5').span.a is None:
                    kan=str(spans.parent.parent.find('div',class_='dataCol5').span.string).strip().replace('\n','')
                else:
                    kan=spans.parent.parent.find('div',class_='dataCol5').span.a.text.strip().replace('\n','')
                print('编号：'+str(bianhao)+' 标题：'+biaoti+' 作者：'+zuozhemen+' 年份：'+nian+' 出版刊物：'+kan)
            if mark==0:
                link=links[int(input('输入编号：'))-1]
        s2=ses.get(link)#进入文章页面
        #fout = open('output4.html', 'w',encoding="UTF-8")
        #fout.write(s2.text)
        soup2 = BeautifulSoup(s2.text, 'html.parser')
        atitles=soup2.find('div',id='authorlist').find_all('a',title='Show Author Details')
        idlist=[]
        spi=SpiderMain('a','b')#创建对象
        sum=0
        for atitle in atitles:
            authorId=re.findall(r'authorId=\w+&',atitle['href'])[0].replace('authorId=','').replace('&','')
            idlist.append(authorId)
            sum+=1
            print('第'+str(sum)+'作者')
            spi.crawel(ses,authorId)#利用得到的authorid复用SpiderMain中的方法









def seperatename(name):
    #获取姓和名
    namelist=name.strip().split()
    xing=namelist[-1]
    namelist.pop()
    ming=" ".join(namelist)
    return xing,ming

def strip_email_protection(s):
    #解密邮件地址
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
def zuozhe_mode():
    #通过输入人名查找审稿人
    name=input("人名: ").replace(',','')
    if name=='exit':
        exit()
    xing,ming=seperatename(name)
    #ming=seperatename(name)[1]
    obj_spider=SpiderMain(xing,ming)
    obj_spider.craw()

def wenxian_mode():
    #通过输入文献查找审稿人
    wenxian=input('文献标题：').strip()
    if wenxian=='exit':
        exit()
    obj_spider=WenxianSpiderMain(wenxian)
    obj_spider.craw()

if __name__=="__main__":

    while True:
        print()
        print('编号1为人名模式，编号2为文献模式，输入exit退出')
        flag=input('输入编号：').strip()
        if flag==str(1):
            zuozhe_mode()
        elif flag==str(2):
            wenxian_mode()
        elif flag=='exit':
            exit()
        else:
            print('输入不符合要求，重新输入')