import re

from bs4 import BeautifulSoup


class HtmlParser(object):
    def GetAuthorId(self, s):
        def Getid(spannode):
            authorId=re.findall(r'authorId=\w+&',spannode.a['href'])[0].replace('authorId=','').replace('&','')
            return authorId
        soup = BeautifulSoup(s.text, 'html.parser')
        span=soup.find_all('span',class_='docTitle')
        if len(span)==0:
            print("找不到人")
            return False
        if len(span)==1:
            authorId=Getid(span[0])
            return authorId
        #输出找到的所有人,选择。
        if len(span)>1:
            bianhao=0
            for spans in span:
                bianhao+=1
                name=spans.a.text
                fathernode=spans.parent.parent.parent
                danwei=fathernode.find('div',class_='dataCol5').text.replace('\n','')
                diqu=fathernode.find('div',class_='dataCol6').text.replace('\n','')
                country=fathernode.find('div',class_='dataCol7').text.replace('\n','')
                print('编号:'+str(bianhao)+' 姓名：'+name+' 单位：'+danwei+' 地区：'+diqu+' 国家：'+country)
            i=input('输入选择的编号：')
            return Getid(span[int(i)-1])

    def GetAuthorMessage(self, s2):
        fout = open('output.html', 'w',encoding="UTF-8")
        fout.write(s2.text)
        soup2 = BeautifulSoup(open('output.html','r',encoding="UTF-8"), 'html.parser',from_encoding="UTF-8")
        namesec=soup2.find_all('div',class_='nameSection')
        span2=namesec[0].find_all('div',class_='authAffilcityCounty')
        namejihe=namesec[0].h1.text.replace(namesec[0].h1.span.text,'').replace('\n','').split(',')
        name=namejihe[-1].strip()+' '+namejihe[0]
        WenxinNum=soup2.find('a',id='docCntLnk').text
        area=str(span2[0].string).strip().replace('\n',' ')
        ArticlesLink=soup2.find_all('div',class_='authorResultsOptionalLinks')[0].a['href']
        return WenxinNum,name,area,ArticlesLink

    def GetArticles(self, s3):
        fout2 = open('output2.html', 'w',encoding="UTF-8")
        fout2.write(s3.text)
        soup3=BeautifulSoup(open('output2.html','r',encoding="UTF-8"), 'html.parser',from_encoding="UTF-8")
        spanarticle=soup3.find_all('span',class_='docTitle')
        list=[]
        for article in spanarticle:
            linka=article.a['href']
            #得到年份
            nian=article.parent.parent.find('div',class_='dataCol4').span.text.replace('\n','')
            list.append([linka,nian])
        return list

    def GetEmail(self, s4):
        fout3 = open('output3.html', 'w',encoding="UTF-8")
        fout3.write(s4.text)
        soup4=BeautifulSoup(open('output3.html','r',encoding="UTF-8"), 'html.parser',from_encoding="UTF-8")
        highlight=soup4.find_all('span',class_='ScopusTermHighlight')
        emailnotparse=highlight[0].parent.parent.find('a',class_='correspondenceEmail')
        return emailnotparse