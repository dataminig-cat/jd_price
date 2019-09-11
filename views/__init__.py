from views.df_manager import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory, askopenfilename
from db_tools import Curls

#功能基类
class basefFrame:
    def __init__(self, root):
        '''初始化'''
        self.dfm = DfManager()
        self.root = root
        self.fFrame = tk.Frame(root, width=960, height=600, bg='#DCDCDC')
        self.fFrame.place(x=0, y=0)
        self.fFrame.bind("<Double-1>",self.callback)   #调试用：输出鼠标位置
        self.xx,self.yy = 0,0
        self.fFrame = self.initFrame()


    def callback(self,event):
        print("当前位置：", event.x, event.y,'\t间隔：',event.x-self.xx,event.y-self.yy)
        self.xx,self.yy = event.x,event.y


    def bulk_load(self):  #批量下载
        def get_detail():
            iurls = Curls()
            urls = self.text.get(1.0, tk.END)
            urls = urls.split('\n')[:-1]
            if urls == ['']:
                tk.messagebox.showinfo('提示', '不能为空')
            else:
                for i in range(len(urls)):
                    iurls.insert_urls(urls, 1)
                tk.messagebox.showinfo('提示', '导入成功')
            bulk_win.destroy()

        def cancel_win():
            bulk_win.destroy()
        bulk_win = tk.Tk()
        bulk_win.geometry('600x450+400+150')
        self.bulk_fFrame = tk.Frame(bulk_win, width=500, height=300, bg='#DCDCDC')
        self.bulk_fFrame.place(x = 50, y= 50)
        ttk.Label(bulk_win, text='批量导入', style="BW.TLabel").place(x=250, y=20)
        self.text = tk.Text(self.bulk_fFrame, height=21, width=67, selectbackground='gray')  # 输入框的位置设定
        self.text.place(x=10, y=10)
        ttk.Button(bulk_win, text='导入', command=get_detail, width=9).place(x=150, y=370)
        ttk.Button(bulk_win, text='取消', command=cancel_win, width=9).place(x=350, y=370)

        # d = MyDialog(self.root, title='批量输入')

    def initFrame(self):
        def selectPath():
            # path_ = askdirectory()
            path_ = askopenfilename()
            path.set(path_)
            print(path_)  # 传目录

        def insert_url():
            iurls = Curls()
            url = v.get()
            if url == "":
                tk.messagebox.showinfo('提示', '不能为空')
            else:
                iurls.insert_urls(url, 1)
                tk.messagebox.showinfo('提示', '导入成功')
        path = tk.StringVar()
        # 创建一个名为File的菜单项
        menuBar = tk.Menu(self.root)
        self.root.config(menu=menuBar)
        menu_tool = tk.Menu(menuBar, tearoff=False)  # 工具栏
        menu_tool.add_command(label='导入文件', command=selectPath)
        menu_tool.add_command(label='批量导入', command="")
        menuBar.add_cascade(label="工具", menu=menu_tool)


        style = ttk.Style()
        number = tk.StringVar()
        style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
        numberChosen = ttk.Combobox(self.fFrame, width=6, textvariable=number, state='readonly')
        numberChosen["values"] = ("1", "2", "3", "4") # 设置下拉列表的值
        numberChosen.current(0)  # 选择第一个
        numberChosen.bind("<<ComboboxSelected>>", "")  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        numberChosen.place(x=10, y=51)


        ttk.Button(self.fFrame, text='上一页', command="", width=9).place(x=80, y=50)
        ttk.Button(self.fFrame, text='下一页', command="", width=9).place(x=160, y=50)
        ttk.Button(self.fFrame, text='刷新', command="", width=9).place(x=240, y=50)
        ttk.Button(self.fFrame, text='清空数据表', command="", width=9).place(x=320, y=50)
        ttk.Button(self.fFrame, text='Go', command="", width=9).place(x=560, y=50)
        tk.Entry(self.fFrame, borderwidth=3, width=9, selectbackground='gray').place(x=450, y=50)             # 输入框的位置设定
        ttk.Label(self.fFrame, text='跳转到', style="BW.TLabel").place(x=400, y=52)
        ttk.Label(self.fFrame, text='页', style="BW.TLabel").place(x=530, y=52)
        # ttk.Label(self.fFrame, text='提醒日志', style="BW.TLabel").place(x=670, y=40)

        #爬虫需要的url输入框
        ttk.Label(self.fFrame, text='导入链接：', style="BW.TLabel").place(x=10, y=12)
        v = tk.StringVar()
        tk.Entry(self.fFrame, borderwidth=3, width=40, textvariable=v,  selectbackground='gray').place(x=70, y=10)  # 输入框的位置设定
        ttk.Button(self.fFrame, text='导入', command=insert_url, width=9).place(x=370, y=10)
        ttk.Button(self.fFrame, text='批量导入', command=self.bulk_load, width=9).place(x=450, y=10)

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
        self.i_log = self.dfm.getDf(self.log_frame,'logger',columns,22,0,0,True)
        self.dfm.setBar(self.log_frame,self.i_log,(255,0,470),(0,465,250))

        self.alert_frame = tk.Frame(self.fFrame)
        self.alert_frame.place(x=x_border,y=100,height=485,width=270)
        columns = {'id':("id",25),
                   "date":("记录时间",75),
                   'name': ('商品名称', 75),
                   'delta_price':('价格变动',75)}
        self.i_alert = self.dfm.getDf(self.alert_frame,'alert',columns,22,0,0,True)
        self.dfm.setBar(self.alert_frame,self.i_alert,(255,0,470),(0,465,250))
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
        self.i_price = self.dfm.getDf(self.fFrame,'price',columns,15,10,100)
        self.dfm.setBar(self.fFrame,self.i_price,(613,100,325),(10,430,620))

        for i in range(25):
            self.i_price.insert("","end",text = "top",values=(i,"2019-01-01",'150','-10'))

    def runLogger(self):
        pass


class Main(tk.Tk):
    def __init__(self,user ='root',passw='123456'):
        super().__init__()
        self.geometry('960x600+200+100')  # 设置窗口大小和相对屏幕位置
        # self.resizable(0, 0)  # 阻止Python GUI的大小调整
        # self.protocol("WM_DELETE_WINDOW", crawlerutils.p)  # 关闭时触发时触发函数
        self.title("价格监测")
        self.initFFrame()

    def initFFrame(self):
        frame = basefFrame(self)
        self.dfm = frame.dfm
