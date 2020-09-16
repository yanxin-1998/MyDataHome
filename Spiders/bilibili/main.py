# https://passport.bilibili.com/login
import requests,re,os,xlsxwriter,json


class BiliBili(object):
    def __init__(self, cookie):
        self.DedeUserID = re.findall('DedeUserID=(\d+);',cookie)[0]
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        cookie_dict = {}
        list = cookie.split(';')
        for i in list:
            try:
                cookie_dict[i.split('=')[0]] = i.split('=')[1]
            except IndexError:
                cookie_dict[''] = i
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie_dict)

    #获取关注信息
    def get_follows(self,amount=None): #amount获取数量
        self.headers['referer']='https://space.bilibili.com/{}/fans/follow'.format(self.DedeUserID)
        if amount==None: amount=20  #默认获取前二十条
        res=self.session.get('https://api.bilibili.com/x/relation/followings?vmid={}&pn=1&ps={}&order=desc&jsonp=jsonp&callback=__jp7'.format(self.DedeUserID,amount),headers=self.headers)
        #关注的up主的ID，简介，描述
        unames = re.findall('"uname":"(.*?)"', res.text)
        signs = re.findall('"sign":"(.*?)"', res.text)
        descs = re.findall('"desc":"(.*?)"', res.text)

        file_path = os.path.join(os.path.dirname(__file__) + '/follows.xlsx')
        book = xlsxwriter.Workbook(file_path)
        sheet = book.add_worksheet()
        sheet.write(0, 0, '关注up主')
        sheet.write(0, 1, '简介')
        sheet.write(0, 2, '描述')

        for index,uname in enumerate(unames):
            sheet.write(index+1, 0, uname)
            sheet.write(index+1, 1, signs[index])
            sheet.write(index+1, 2, descs[index])

    #获取粉丝信息
    def get_fans(self,amount=None):
        self.headers['referer']='https://space.bilibili.com/{}/fans/fans'.format(self.DedeUserID)
        if amount==None: amount=20
        res=self.session.get('https://api.bilibili.com/x/relation/followers?vmid={}&pn=1&ps={}&order=desc&jsonp=jsonp&callback=__jp7'.format(self.DedeUserID,amount),headers=self.headers)
        #粉丝的ID，简介，描述
        unames = re.findall('"uname":"(.*?)"', res.text)
        signs = re.findall('"sign":"(.*?)"', res.text)
        descs = re.findall('"desc":"(.*?)"', res.text)

        file_path = os.path.join(os.path.dirname(__file__) + '/fans.xlsx')
        book = xlsxwriter.Workbook(file_path)
        sheet = book.add_worksheet()
        sheet.write(0, 0, '粉丝')
        sheet.write(0, 1, '简介')
        sheet.write(0, 2, '描述')


        for index, uname in enumerate(unames):
            sheet.write(index + 1, 0, uname)
            sheet.write(index + 1, 1, signs[index])
            sheet.write(index + 1, 2, descs[index])

    #获取收藏夹内容
    def get_favlist(self,amount=None):
        #先取得media_id
        self.headers['referer']='https://space.bilibili.com/318175050/favlist'
        res=self.session.get('https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=318175050&jsonp=jsonp',headers=self.headers)
        media_id=json.loads(res.text)["data"]["list"][0]["id"]
        #获取收藏夹内容并保存json文件
        if amount==None: amount=20
        url='https://api.bilibili.com/x/v3/fav/resource/list?media_id={}&pn=1&ps={}&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'.format(media_id,amount)
        res=self.session.get(url,headers=self.headers)
        medias_data=json.loads(res.text)['data']['medias']
        file_path = os.path.join(os.path.dirname(__file__) + '/favlist.json')
        with open(file_path,'w') as f:
            json.dump(medias_data,fp=f)

# cookies="_uuid=1DFFFF8C-C2C0-714D-1CCA-73C83113D46E54240infoc; buvid3=6D51A099-6E63-4E35-BB54-7A95A7666497155806infoc; CURRENT_FNVAL=16; rpdid=|(J~R~|)~Y|l0J'ul)~mYJYm~; LIVE_BUVID=AUTO6915879803352779; sid=5d4o6bif; bsource=search_baidu; bp_video_offset_318175050=409120988142431488; DedeUserID=318175050; DedeUserID__ckMd5=c1d10230906a37b7; SESSDATA=9ada1e46%2C1609669296%2Cd098d*71; bili_jct=e60eeb3d2915c8f42729d14f57f00122; PVID=1"
# a=BiliBili(cookies)
# a.get_follows()
# a.get_fans()
# a.get_favlist()
