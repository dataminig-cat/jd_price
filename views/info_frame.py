from db_tools.url import Curls
from db_tools.price import Cprice
from views.df_manager import DfManager
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from threading import Thread
# import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintertable import TableCanvas,TableModel
class InfoFrame(tk.Frame):
    def __init__(self, root,crawler=None):
        self.crawler = crawler
        self.dfm = DfManager()
        super().__init__(root, width=960, height=600, bg='#DCDCDC')
        self.initFrame()

    def show_table(self,data):
        iprice = Cprice()
        for gid,goods in data.items():
            pre_price = 0
            for inst in iprice.query(gid=gid):
                self.dfm.insert('price',[goods,inst.date_time,inst.price,inst.price-pre_price])
                pre_price = inst.price
        try:
            self.numberChosen['values'] = tuple(self.dfm.group_by('price',0))
        except KeyError:    # 数据库无数据
            pass


    def query_df(self,shops=None):
        '''获取单个商品价格变动表格数据'''
        items = [(i,'笔记本电脑', "2019-01-01", '150', '-10') for i in range(25)]
        for v in items:
            self.i_price.insert("", "end",values=v)
    def initFrame(self):
        # ** 功能标签
        y2 = 0
        label = ttk.Label(self, text='选择商品', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: GoodsTable(self.show_table))
        label.place(x=10, y=y2)
        label = ttk.Label(self, text='数据信息', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: self.catch_frame.tkraise())
        label.place(x=130, y=y2)
        label = ttk.Label(self, text='绘图界面', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: self.paint_frame.tkraise())
        label.place(x=70, y=y2)

        y3 = 25
        self.catch_frame = tk.Frame(self)
        self.catch_frame.place(x=7, y=y3, height=400, width=650)
        # ** 画图界面
        self.paint_frame = tk.Frame(self)
        self.paint_frame.place(x=7, y=y3, height=400, width=650)
        ttk.Label(self.paint_frame, text='X :', style="BW.TLabel").place(x=10, y=11)
        ttk.Label(self.paint_frame, text='Y :', style="BW.TLabel").place(x=120, y=11)
        style = ttk.Style()
        number = tk.StringVar()
        style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
        numberChosen = ttk.Combobox(self.paint_frame, width=6, textvariable=number, state='readonly')
        # numberChosen["values"] = ("1", "2", "3", "4")  # 设置下拉列表的值
        # numberChosen.current(0)  # 选择第一个
        numberChosen.bind("<<ComboboxSelected>>", )  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        # numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        numberChosen.place(x=40, y=11)
        #
        style = ttk.Style()
        number = tk.StringVar()
        style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
        numberChosen = ttk.Combobox(self.paint_frame, width=6, textvariable=number, state='readonly')
        numberChosen["values"] = ("1", "2", "3", "4")  # 设置下拉列表的值
        numberChosen.current(0)  # 选择第一个
        numberChosen.bind("<<ComboboxSelected>>", "")  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        numberChosen.place(x=150, y=11)

        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        # ax.scatter(x_data, y_data)
        # plt.ion()
        # plt.show()

        # 在Tk的GUI上放置一个画布，
        # matplotlib.use('TkAgg')
        self.fig = plt.figure(figsize=(6, 3.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.paint_frame)
        self.ax = self.fig.add_subplot(1, 1, 1)
        lines = self.ax.plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], 'r-', lw=5)
        self.canvas.get_tk_widget().place(x=10, y=40)

        # self.figure = Figure(figsize=(6,3.5), dpi=100)
        # self.canvas = FigureCanvasTkAgg(self.figure, master=self.paint_frame)
        # self.a = self.figure.add_subplot(111)
        # # 在[0,100]范围内随机生成sampleCount个数据点
        # x = np.random.randint(0, 100, size=50)
        # y = np.random.randint(0, 100, size=50)
        # color = ['b', 'r', 'y', 'g']
        # # 绘制这些随机点的散点图，颜色随机选取
        # self.a.scatter(x, y, s=3, color=color[np.random.randint(len(color))])
        # self.a.set_title('Demo: Draw N Random Dot')
        # # self.canvas.show()
        # self.canvas.get_tk_widget().place(x=10, y=40)
        # self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
        # ttk.Button(self.paint_frame, text='画图', command=self.drawPic).place(x=250, y=10)
        # label.bind('<Button-1>', lambda x: self.paint_frame.tkraise())
        # label.place(x=70, y=50)

        style = ttk.Style()
        number = tk.StringVar()
        style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
        self.numberChosen = ttk.Combobox(self.catch_frame, width=18, textvariable=number, state='readonly')
        # numberChosen["values"] = ("1", "2", "3", "4")  # 设置下拉列表的值
        self.numberChosen.bind("<<ComboboxSelected>>", lambda x: self.dfm.show_by('price', self.numberChosen.get()))
        # self.numberChosen['values'][self.numberChosen.current()]))  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        # numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        self.numberChosen.place(x=90, y=12)
        ttk.Button(self.catch_frame, text='筛选', command="", width=9).place(x=10, y=10)
        # ttk.Button(self.catch_frame, text='下一页', command="", width=9).place(x=160, y=10)
        ttk.Button(self.catch_frame, text='刷新', command="", width=9).place(x=240, y=10)
        ttk.Button(self.catch_frame, text='清空数据表', command=lambda: self.dfm.cls('price'), width=9).place(x=320, y=10)
        ttk.Button(self.catch_frame, text='导出表格').place(x=400, y=10)

        # ** 价格信息表格
        width = 100
        columns = {'id': ("id", width),
                   'goods': ('商品名称', width),
                   "date": ("记录时间", 200),
                   'price': ('价格', width),
                   'delta_price': ('价格变动', width)}
        self.i_price = self.dfm.getDf(self.catch_frame, 'price', columns, 15, 10, 45, True)
        self.dfm.setBar(self.catch_frame, self.i_price, (613, 45, 325), (20, 375, 570))
        # ** 日志表格
        x_border = 670
        self.log_frame = tk.Frame(self)
        self.log_frame.place(x=x_border, y=y3, height=485, width=270)
        columns = {'id': ("id", 25),
                   "date": ("记录时间", 75),
                   'name': ('商品名称', 100),
                   'status': ('状态', 50)}
        self.i_log = self.dfm.getDf(self.log_frame, 'logger', columns, 22, 0, 0, True)
        self.dfm.setBar(self.log_frame, self.i_log, (255, 0, 470), (0, 465, 250))

        self.alert_frame = tk.Frame(self)
        self.alert_frame.place(x=x_border, y=y3, height=485, width=270)
        columns = {'id': ("id", 25),
                   "date": ("记录时间", 75),
                   'name': ('商品名称', 75),
                   'delta_price': ('价格变动', 75)}
        self.i_alert = self.dfm.getDf(self.alert_frame, 'alert', columns, 22, 0, 0, True)
        self.dfm.setBar(self.alert_frame, self.i_alert, (255, 0, 470), (0, 465, 250))
        label = ttk.Label(self, text='采集日志', style="BW.TLabel")

        label.bind('<Button-1>', lambda x: self.log_frame.tkraise())
        label.place(x=x_border, y=y2)
        label = ttk.Label(self, text='提醒', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: self.alert_frame.tkraise())
        label.place(x=x_border + 70, y=y2)

class GoodsTable(tk.Tk):
    def __init__(self,show=None):
        '''
        :param show:触发主界面的数据显示
        '''
        super().__init__()
        # self.geometry('600x450+400+150')
        self.goodsId = {}
        self.show = show
        self.initFrame()
        self.add_data()
        self.mainloop()
    def initFrame(self):
        # *****界面区*****
        # 布局参数

        params = ['row','column','rowspan','columnspan']
        gridMap =  {'label':(0,0),
                'entry':(0,1),
                'search_button':(0,2),
                'table':(1,1,None,3),
                'next_page':(2,1),
                'modify':(2,2),
                'corfirm':(2,3)}
        cnfs = {}
        for k,vals in gridMap.items():
            dic = {}
            for i,v in enumerate(vals):
                dic[params[i]] = v
            cnfs[k] = dic
        ttk.Label(self, text='搜索', style="BW.TLabel").grid(cnfs['label'])

        self.keyword = tk.StringVar()   # 搜索框
        tk.Entry(self, borderwidth=3, width=40, textvariable=self.keyword, selectbackground='gray').grid(cnfs['entry'])
        ttk.Button(self, text='搜索', command="", width=9).grid(cnfs['search_button'])
        frame = tk.Frame(self)
        frame.grid(cnfs['table'])
        model = TableModel()
        self.table = TableCanvas(frame,model)
        self.table.show()
        ttk.Button(self, text='下一页', command="", width=9).grid(cnfs['next_page'])
        ttk.Button(self, text='修改', command=self.choic, width=9).grid(cnfs['modify'])
        ttk.Button(self, text='选择', command=self.choic, width=9).grid(cnfs['corfirm'])

    def add_data(self):
        iurls = Curls()
        data = {}
        for i,inst in enumerate(iurls.query()):
            self.goodsId[i] = (inst.id,inst.goods)
            dic = {}
            dic['goods'] = inst.goods
            dic['common_price'] = inst.common_price
            dic['expect_price'] = inst.expect_price
            dic['setting'] = inst.setting
            data[i] = dic
        self.table.model.importDict(data)

    def choic(self):
        try:
            if self.show is not None:
                data = {}
                for id in self.table.get_selectedRecordNames():
                    k,v = self.goodsId[id]
                    data[k] = v
                self.show(data)
            self.destroy()
        except IndexError:
            tk.messagebox.showinfo('提示', '重新选择')
