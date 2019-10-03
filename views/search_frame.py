import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
class SearchFrame(tk.Frame):
    def __init__(self,root,bulk_load=None):
        self.bulk_load =bulk_load
        self.iFrame = root.iFrame
        super().__init__(root,height=525, width=960)
        self.initFrame()
        self.data = []      # 数据，[{}]
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
        infoV = self.infoList[ind]  # 元组，item与之想对应
        path = item[0]  # 图片的地址名
        infoV[0].paste(Image.open(path).resize((100 , 100)))
        for i in range(1,4):
            infoV[i].set(item[i])
        return



    def deshow(self,ind,item):
        pass
        # Image.new('RGB', (height,width), (0, 255, 255))


    def Bind(self, label):
        '''鼠标移进去组建内部'''
        label.bind('<Motion>', self._baColor)
        label.bind('<Leave>', self._bcColor)
    def _baColor(self, event):
        '''alterColor改变组件背景色'''
        event.widget.configure(bg='#DCDCDC')
    def _bcColor(self, event):
        '''cancerColor取消组件背景色'''
        event.widget.configure(bg=self.bgcolor[event.widget.id % 2])
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
        ttk.Button(self, text='上一页', command='').place(x=x, y=y1)  # 下载按钮
        x += xpad
        ttk.Button(self, text='下一页', command='').place(x=x, y=y1)  # 下载按钮
        x += xpad
        ttk.Button(self, text='返回', command=lambda :self.iFrame.tkraise()).place(x=x, y=y1)  # 下载按钮
        x += xpad
        ttk.Button(self, text='确定', command="").place(x=x, y=y1)  # 下载按钮

        self._imgList = []  # 避免内存被释放
        # 展示商品的格子
        height,width = 100,100
        for i in range(2):
            for index in range(4):
                label = tk.Label(self,bg=self.bgcolor[i % 2])   #
                label.place(x=index*240,y=240*i,width=240,height=240)
                label.id = i
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
