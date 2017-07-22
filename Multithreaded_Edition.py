#python3.5
from urllib.request import urlopen
import re,csv,time,threading

baseurl = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.4350.FPLQkk&category=50025969&city=%BD%B9%D7%F7&trade_type=1&sorder=1&auction_start_seg=-1'
page = 0
def geturls(): #获取所有网页url
    html = urlopen(baseurl).read().decode('gbk')
    reg = r'itemUrl":"(//sf\.taobao\.com/sf_item/\d+.htm)'
    urls = re.findall(reg,html)
    return urls

def getdate(url):#获得每个网页的数据
    html = urlopen('https:'+url).read().decode('gbk')
    reg1 = r'<title>(.+?) -  司法拍卖 - 阿里拍卖 - 闲鱼拍卖</title>'

    title = re.findall(reg1,html,re.S)#内容

    reg2 = r' <em class="m-i">&yen;</em><span class="J_Price">(.+?)</span></span>'
    price = re.findall(reg2,html) #起拍价，加价幅度，保证金，评估价
    reg3 = r'<span class="J_WangWang" data-nick="(.+?)"></span>'
    cldw = re.findall(reg3,html)

    reg4 =r'<p>联系咨询方式：<em>(.+?)</em>'
    linkman = re.findall(reg4,html) #联系人

    reg5 = r'</em> (.+?)</p>'
    tel = re.findall(reg5,html)
    data =(title,price[0],price[3],cldw,linkman,tel)
    return data
def downdata(data):
    with open(r'/home/cailujia/Desktop/tbsfdata2.csv','a+') as f:
        writer = csv.writer(f)
        writer.writerow(data)#('标题','起拍价','评估价','处理单位','联系人','电话')
        f.close()
st = time.time()
urls = geturls()
def main(url):
    try:
        data = getdate(url)
        downdata(data)
    except:
        print('此采集页异常%s'%url)
        pass
threads = []
#for url in urls:
#    print(url)
for url in urls:
    t = threading.Thread(target=main,args=(url,))
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()


et = time.time()
tt = et - st

print('数据采集完毕')
print('共花费%s秒'%tt)
#使用多线程耗时6秒左右，比单线程（16秒左右）快了将近三倍
