#定义parser方法从直接复制的参考文献中得到可以用于查询的文献标题
import re


def parser(title,method):
    # re.sub用于替换字符串中的匹配项
    nima=title
    def parser1(title):
        # [1]name, name2, et al. 或name, name2. ***[J]***
        re.sub(r'^\[\d+\].+(et\sal\.|\.)','',title)
        re.sub(r'\[[A-Z]\].+]','',title)
        return title
    def parser2(title):
        # name... (2000). 或2000(a)***. 或， Journal name***
        pattern1=re.compile(r'.+(,\s|,|\.\s)(\d{4}|\d{4}a|\d{4}b|Year|\(\d{4}\))(\.|:)')
        pattern2=re.compile(r'((\[[A-Z]\]\.)|(\.\s)|(,\s[A-Z\d])).+$')
        a=re.sub(pattern1,'',title,1)
        c=re.sub(pattern2,'',a,1)
        # st=re.findall(pattern1,title)[0]
        # title=title.replace(st,'')
        return c
    def parser3(title):
        # ***“name”***
        pattern1=re.compile(r'.+\s“')
        pattern2=re.compile(r',”.+')
        a=re.sub(pattern1,'',title,1)
        c=re.sub(pattern2,'',a,1)
        # st=re.findall(pattern1,title)[0]
        # title=title.replace(st,'')
        return c
    operator = {'1':parser1,'2':parser2,'3':parser3}
    hh=operator.get(method)(title)


    return hh


titles=open('spider.txt','r',encoding='utf-8').readlines()
a=''
for title in titles:
    #rstrip() 删除 string 字符串末尾的指定字符
    print(parser(title.rstrip('\n'),'2'))
# for title in titles:
#     a+=title.replace('\n','')
# a.replace('\n','')
# print(a)
# parser(a,2)