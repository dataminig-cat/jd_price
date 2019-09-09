import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory, askopenfilename

#功能基类
class basefFrame:
    def __init__(self, root):
        '''初始化'''
        self.root = root
        self.fFrame = tk.Frame(root, width=960, height=600, bg='#DCDCDC')
        self.fFrame.place(x=0, y=0)
        self.fFrame.bind("<Double-1>",self.callback)   #调试用：输出鼠标位置
        self.xx,self.yy = 0,0
        self.fFrame = self.initFrame()


    def callback(self,event):
        print("当前位置：", event.x, event.y,'\t间隔：',event.x-self.xx,event.y-self.yy)
        self.xx,self.yy = event.x,event.y

    def initFrame(self):
        def selectPath():
            # path_ = askdirectory()
            path_ = askopenfilename()
            path.set(path_)
            print(path_)  # 传目录

        path = tk.StringVar()
        # 创建一个名为File的菜单项
        menuBar = tk.Menu(self.root)
        self.root.config(menu=menuBar)
        menu_tool = tk.Menu(menuBar, tearoff=False)  # 工具栏
        menu_tool.add_command(label='读取', command=selectPath)
        menu_tool.add_command(label='保存', command="")
        menuBar.add_cascade(label="语言", menu=menu_tool)

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
        number = tk.StringVar()
        numberChosen = ttk.Combobox(self.fFrame, width=6, textvariable=number, state='readonly')
        numberChosen["values"] = ("1", "2", "3", "4") # 设置下拉列表的值
        numberChosen.current(0)  # 选择第一个
        numberChosen.bind("<<ComboboxSelected>>", "")  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        numberChosen.place(x=10, y=21)


        ttk.Button(self.fFrame, text='上一页', command="", width=9).place(x=80, y=20)
        ttk.Button(self.fFrame, text='下一页', command="", width=9).place(x=160, y=20)
        ttk.Button(self.fFrame, text='刷新', command="", width=9).place(x=240, y=20)
        ttk.Button(self.fFrame, text='清空数据表', command="", width=9).place(x=320, y=20)
        ttk.Button(self.fFrame, text='Go', command="", width=9).place(x=560, y=20)
        tk.Entry(self.fFrame, borderwidth=3, width=9, selectbackground='gray').place(x=450, y=20)             # 输入框的位置设定
        ttk.Label(self.fFrame, text='跳转到', style="BW.TLabel").place(x=400, y=22)
        ttk.Label(self.fFrame, text='页', style="BW.TLabel").place(x=530, y=22)

        ttk.Label(self.fFrame, text='总页数：', style="BW.TLabel").place(x=10, y=500)
        ttk.Label(self.fFrame, text='采集设置：', style="BW.TLabel").place(x=10, y=530)

        ttk.Label(self.fFrame, text='当前页数：', style="BW.TLabel").place(x=200, y=500)
        ttk.Label(self.fFrame, text='导出csv：', style="BW.TLabel").place(x=200, y=530)

        ttk.Label(self.fFrame, text='总条数：', style="BW.TLabel").place(x=400, y=500)
        ttk.Label(self.fFrame, text='筛选：', style="BW.TLabel").place(x=400, y=530)

        # ** 日志表格
        x_border = 670
        ttk.Label(self.fFrame, text='数据信息', style="BW.TLabel").place(x=10, y=50)
        self.log_frame = tk.Frame(self.fFrame)
        self.log_frame.place(x=x_border,y=100,height=485,width=270)
        columns = {'id':("id",25),
                   "date":("记录时间",75),
                   'name': ('商品名称', 100),
                   'status':('状态',50)}
        self.i_log = self.getDf(self.log_frame,columns,22,0,0,True)
        self.setBar(self.log_frame,self.i_log,(255,0,470),(0,465,250))

        self.alert_frame = tk.Frame(self.fFrame)
        self.alert_frame.place(x=x_border,y=100,height=485,width=270)
        columns = {'id':("id",25),
                   "date":("记录时间",75),
                   'name': ('商品名称', 75),
                   'delta_price':('价格变动',75)}
        self.i_alert = self.getDf(self.alert_frame,columns,22,0,0,True)
        self.setBar(self.alert_frame,self.i_alert,(255,0,470),(0,465,250))
        label = ttk.Label(self.fFrame, text='采集日志', style="BW.TLabel")

        label.bind('<Button-1>',lambda x: self.log_frame.tkraise())
        label.place(x=x_border, y=50)
        label = ttk.Label(self.fFrame, text='提醒', style="BW.TLabel")
        label.bind('<Button-1>',lambda x:self.alert_frame.tkraise())
        label.place(x=x_border+70, y=50)
        # ** 价格信息表格
        width = 100
        columns = {'id':("id",width),
                   "date":("记录时间",width),
                   'price':('价格',width),
                   'delta_price':('价格变动',width)}
        self.i_price = self.getDf(self.fFrame,columns,15,10,100)
        self.setBar(self.fFrame,self.i_price,(613,100,325),(10,430,620))

        for i in range(25):
            self.i_price.insert("","end",text = "top",values=(i,"2019-01-01",'150','-10'))
        for i in range(25):
            self.i_log.insert("","end",text = "top",values=(i,"2019-01-01",'笔记本','成功'))
        for i in range(25):
            self.i_alert.insert("","end",text = "top",values=(i,"2019-01-01",'150','-10'))

    def runLogger(self):
        pass

    def getDf(self,root,columns,height,x,y,headings=False):
        '''
        :param columns: {"col":('name',width)}
        :param height:  raw_nums
        :param headings: whether show the first col
        :return:
        '''
        dataframe = ttk.Treeview(root, columns=tuple(columns.keys()),
                                 height=height)
        if headings:
            dataframe['show'] = 'headings'
        for col,(name,width) in columns.items():
            dataframe.column(col, width=width, anchor='center')  # 表示列,不显示
            dataframe.heading(col, text=name)  # 显示表头
        dataframe.place(x=x,y=y)
        return dataframe
    def setBar(self,root,widget,vplace,hplace):
        '''
        :param root:
        :param widget:
        :param vplace: (x,y,length)
        :param hplace:
        :return:
        '''
        # 垂直滚动条
        vbar =  tk.Scrollbar(root,orient=tk.VERTICAL,command=widget.yview)
        widget.configure(yscrollcommand = vbar.set)
        x,y,height = vplace
        vbar.place(x=x,y=y,height=height)
        # 水平滚动条
        hbar =  tk.Scrollbar(root,orient=tk.HORIZONTAL,command=widget.xview)
        widget.configure(xscrollcommand = hbar.set)
        x, y, height = hplace
        hbar.place(x=x,y=y,width=height)


class Main(tk.Tk):
    def __init__(self,user ='root',passw='123456'):
        super().__init__()
        self.geometry('960x600+200+100')  # 设置窗口大小和相对屏幕位置
        # self.resizable(0, 0)  # 阻止Python GUI的大小调整
        # self.protocol("WM_DELETE_WINDOW", crawlerutils.p)  # 关闭时触发时触发函数
        self.title("价格监测")
        self.initFFrame()
        # self.mainloop()

    def initFFrame(self):
        frame = basefFrame(self)

