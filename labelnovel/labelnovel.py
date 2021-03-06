import os
import re
import chardet
import time

def get_chardet(filename):
    data=open(filename,'rb').read()
    coding=chardet.detect(data)
    return coding['encoding']

def wordlabel(filename,colors):
    encoding=get_chardet('data/'+filename)
    if encoding=='GB2312':
        encoding='GBK'
    text=open('data/'+filename,'r',encoding=encoding).read()
    html='<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<meta charset="utf-8">\r\n<title>{title}</title>\r\n</head>\r\n<body>{body}\r\n</body>\r\n</html>'
    body=''
    textline='<p>{line}</p>'
    wordcolor='<span style="background:{color}">{word}</span>'
    points=['.',',','?','!',"'",'《','》',':',';','"','\r\n','\n']
    for line in open('data/'+filename,'r',encoding=encoding):
        body+=textline.format(line=line)+'\r\n'
    for key in colors:
        body=body.replace(key,wordcolor.format(color=colors[key],word=key))
    return html.format(body=body,title=filename.replace('.txt',''))

def loadcolor():
    encoding=get_chardet('settings/color')
    if encoding=='GB2312':
        encoding='GBK'
    colors={}
    for line in open('settings/color','r',encoding=encoding):
        line=line.replace('\r','').replace('\n','').replace(' ','')
        try:
            colors[line.split('-')[0]]=line.split('-')[-1]
        except:
            continue
    return colors

def main():
    colors=loadcolor()
    for filename in os.listdir('data'):
        if filename.endswith('txt'):
            try:
                html=wordlabel(filename,colors)
            except:
                print(filename,'failed')
                continue
            f=open('result/%s.html'%(filename.replace('.txt','')),'w',encoding='utf-8')
            f.write(html)
            f.close()
            print(filename,'ok')
    time.sleep(50)
main()
