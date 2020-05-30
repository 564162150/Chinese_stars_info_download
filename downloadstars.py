import requests
import sqlite3
from xpinyin import Pinyin
from bs4 import BeautifulSoup
from neo4jedit import starneo4j,deleteneo4j

#打开本地数据库
db = sqlite3.connect('./stars.db')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

#sqllit语句执行
def sqlq(sqltext):
    cursor.execute(sqltext)
    db.commit()
    return cursor.fetchall()

#清空历史数据
deleteneo4j()
sqlq("""DELETE from stars""")


#输入本次要下载的明星
startext=input('请输入想查找的【内地】明星：')
# startext='赵薇'

#转换拼音
p = Pinyin()
startextp=p.get_pinyin(startext, '')

#拼接初始链接
fristurl = 'http://www.ylq.com/neidi/%s/' % (startextp)


def getstars(sstar,url):
    #插入初始查询人
    sqlq("""INSERT INTO "stars"("starname", "starurl", "status") VALUES (\'%s\', \'%s\', 1)""" % (sstar, url))
    r = requests.get(url)  # 使用GET请求访问链接
    content = r.content
    if r.status_code == requests.codes.ok:
        # 获取链接数据
        soup = BeautifulSoup(content,'lxml')
        #找到关系表
        div_tag=soup('div',class_='hd starRelation')
        getstarsrelation(sstar,div_tag)
        sqlq("""UPDATE stars set status=1 where starname=\'%s\'""" %(sstar))
    wstars=sqlq("""select starname,starurl from stars where status=0""")
    for i in wstars:
        getstars(i[0], i[1])


def getstarsrelation(sstar,ftag):
    #获取关系值
    for a in ftag[0]('a'):
        title = str(a.get('title'))
        wstarsname = sqlq("""select count(1) from stars where starname=\'%s\'""" %(title))
        #判断如果现在表中已有这个人，则不再查询
        if wstarsname[0][0]:
            continue
        href = a.get('href')
        relation=str(a.span.em.string)
        print(href,'\n',title,'\n',relation,'\n')
        starneo4j(sstar, relation, title)
        sqlq("""INSERT INTO "stars"("starname", "starurl", "status") VALUES (\'%s\', \'%s\', 0)""" % (title, href))



#开始执行
getstars(startext,fristurl)

#1、输入需爬取的人
#2、依次进入待爬取人，和关联人页面
#3、抓取当前页关联人及关系(排除子关系人与当前关系人)
#4、存至图数据库
#5、直至当前这个待爬取人没有其他关系人