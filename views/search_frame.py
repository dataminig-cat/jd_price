import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from io import BytesIO
import requests
import datetime
try:
    from db_tools.url import Curls
except:
    pass
class SearchFrame(tk.Frame):
    def __init__(self,root,bulk_load=None):
        self.bulk_load =bulk_load
        self.iFrame = root.iFrame
        super().__init__(root,height=525, width=960)
        self.initFrame()
        self.data = []      # 传入的商品数据，[{}]
        self.chooseDict = {}    # 选择导入的商品
        self.cur_page = 1
    def add_data(self,item):
        '''
        :param item:{}
        :return:
        '''
        self.data.append(item)
        length = len(self.data)
        if length <= self.cur_page * 8:
            self.show(length % 8,item)

    def show(self,ind,item):
        # 背景色
        infoV = self.infoList[ind]  # 元组，item与之想对应
        path = item[0]  # 图片的地址名
        if path[:4] == 'http':
            rsp = requests.get(path)
            img = Image.open(BytesIO(rsp.content))
        else:
            img = Image.open(path)
        infoV[0].paste(img.resize((100 , 100)))
        for i in range(1,4):
            infoV[i].set(item[i])
        return
    def deshow(self,ind):
        infoV = self.infoList[ind]  # 元组，item与之想对应
        infoV[0].paste(Image.new('RGB', (100,100), (255, 255, 255)))
        for i in range(1, 4):
            infoV[i].set('')
    def flushLabelBg(self,ind):
        if ind in self.chooseDict:
            self.labelList[ind%8].configure(bg='#FFFF00')
        else:
            self.labelList[ind%8].configure(bg=self.bgcolor[ind%8 % 4 % 2])
    def next_page(self):
        if self.cur_page * 8 < len(self.data):
            if len(self.data) <= (self.cur_page+1)*8:
                for i in range(self.cur_page * 8,(len(self.data))):
                    self.show(i % 8,self.data[i])
                    self.flushLabelBg(i)
                for i in range(len(self.data), (self.cur_page+1)*8):
                    self.deshow(i % 8)
                    self.flushLabelBg(i)
            else:
                for i in range(self.cur_page * 8,(self.cur_page+1)*8):
                    self.show(i % 8,self.data[i])
                    self.flushLabelBg(i)
            self.cur_page += 1
    def pre_page(self):
        if self.cur_page != 1:
            self.cur_page -= 1
            for i in range((self.cur_page-1) * 8,min(len(self.data),self.cur_page*8)):
                self.show(i % 8,self.data[i])
                self.flushLabelBg(i)

    def dump_goods(self):
        if self.chooseDict:
            iurls = Curls()
            for k,(goods,url) in self.chooseDict.items():
                iurls.update(f'url={url}',setting=1,goods=goods,origin_time=datetime.datetime.now())
                self.labelList[k % 8].configure(bg=self.bgcolor[k % 8 % 4 % 2])
            self.chooseDict = {}
            self.chooseV.set("已选择：0")
    def Bind(self, label):
        '''鼠标移进去组建内部'''
        label.bind('<Motion>', self._baColor)
        label.bind('<Leave>', self._bcColor)
        label.bind("<Button-1>", self.__bchoose)
        label.bind("<Button-3>", self.__bcancel)
        label.bind("<Double-1>", self.dump_goods)  # 双击下载或打开

    def __bchoose(self, event):
        if self.data:
            i, j = event.widget.id
            ind =(self.cur_page-1) * 8 + j
            if ind not in self.chooseDict:
                if ind < len(self.data):
                    info = self.data[ind]
                    self.chooseDict[ind] = (info[2],info[-1])
                    event.widget.configure(bg='#FFFF00')
                    self.chooseV.set(f"已选择：{len(self.chooseDict)}")
    def __bcancel(self, event):
        i, j = event.widget.id
        ind = (self.cur_page-1) * 8 + j
        if ind in self.chooseDict:
            event.widget.configure(bg=self.bgcolor[i % 2])
            del self.chooseDict[ind]
            self.chooseV.set(f"已选择：{len(self.chooseDict)}")
    def _baColor(self, event):
        '''alterColor改变组件背景色'''
        i, j = event.widget.id
        ind = (self.cur_page - 1) * 8 + j
        if ind not in self.chooseDict:
            event.widget.configure(bg='#DCDCDC')
    def _bcColor(self, event):
        '''cancerColor取消组件背景色'''
        i, j = event.widget.id
        ind = (self.cur_page - 1) * 8 + j
        if ind not in self.chooseDict:
            event.widget.configure(bg=self.bgcolor[i % 2])
    def initFrame(self):
        '''显示信息的列表'''
        self.infoList = []  #[（图片,价格，名称，店铺）]
        y, ypad = 0, 125  # y位置、y间隔
        self.bgcolor = ('#FFFFFF', '#F5F5F5')  # '#DCDCDC'FFFFFF
        cnf = {'sticky':tk.N+tk.E+tk.W}
        tk.Label(self,bg=self.bgcolor[0], width = 56, height = 7,font=('',25)).grid(cnf,row=0,column=0)
        tk.Label(self, bg=self.bgcolor[1], width = 56, height = 7,font=('',25)).grid(cnf,row=1,column=0)
        y1 = 490
        x,xpad = 500,100
        ttk.Button(self, text='上一页', command=self.pre_page).place(x=x, y=y1)  # 下载按钮
        x += xpad
        ttk.Button(self, text='下一页', command=self.next_page).place(x=x, y=y1)  # 下载按钮
        x += xpad
        ttk.Button(self, text='返回', command=lambda :self.iFrame.tkraise()).place(x=x, y=y1)  # 下载按钮
        x += xpad
        ttk.Button(self, text='确定', command=self.dump_goods).place(x=x, y=y1)  # 下载按钮
        self.chooseV = tk.StringVar(self,"已选择：0")
        ttk.Label(self,textvariable=self.chooseV).place(x=10,y=y1)
        self._imgList,self.labelList = [],[]  # 避免内存被释放
        # 展示商品的格子
        height,width = 100,100
        for i in range(2):
            for index in range(4):
                label = tk.Label(self,bg=self.bgcolor[i % 2])   #
                label.place(x=index*240,y=240*i,width=240,height=240)
                label.id = i,i*4+index
                self.labelList.append(label)
                self.Bind(label)
                img = Image.new('RGB', (height,width), (0, 255, 255))  # 初始化一张84*125的白色(255,255,255)图片
                img = ImageTk.PhotoImage(img)
                # id = self.filmIdList[event.widget.id]
                img.paste(Image.open('data/c08f5b9802f56855.jpg').resize((height, width)))
                labelImg = tk.Label(self, height=height, width=width, image=img, bg=self.bgcolor[(1+i) % 2])
                labelImg.place(x=45+index*240, y=10+i*240)
                self._imgList.append(img)
                # 价格
                priceV = tk.StringVar(self)
                priceV.set(6989)
                tk.Label(self,textvariable=priceV,font=('',14) , bg=self.bgcolor[i % 2]).place(x=25+index*240,y=130+240*i)
                goodsV = tk.StringVar(self)
                goodsV.set('''华硕(ASUS) 灵耀Deluxe13 英特尔酷睿i7 13.3英寸轻薄笔记本电脑(i7-8565U 8G''')
                tk.Label(self,height =4, textvariable=goodsV, font=('', 10),justify = 'left',anchor='w',wraplength = 200,
                         bg=self.bgcolor[i % 2]).place(x=25 + index * 240,y=155 + 240 * i)
                shopsV = tk.StringVar(self)
                shopsV.set('''华硕京东自营官方旗舰店''')
                tk.Label(self,height =1, textvariable=shopsV, font=('', 8),justify = 'left',anchor='w',wraplength = 200,
                         bg=self.bgcolor[i % 2]).place(x=50 + index * 240,y=210 + 240 * i)
                self.infoList.append((img,priceV,goodsV,shopsV))
        '''华硕(ASUS) 灵耀Deluxe13 英特尔酷睿i7 13.3英寸轻薄笔记本电脑(i7-8565U 8G'''
        '''华硕京东自营官方旗舰店'''
