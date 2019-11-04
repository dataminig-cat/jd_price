from views.df_manager import DfManager
import json
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Simhei']
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintertable import TableCanvas,TableModel
import time
try:
    from db_tools.url import Curls
    from db_tools.price import Cprice
except:
    pass
class InfoFrame(tk.Frame):
    def __init__(self, root,crawler=None):
        self.crawler = crawler
        self.dfm = DfManager()
        super().__init__(root, width=960, height=600, bg='#DCDCDC')
        self.initFrame()
        self.init_sys()
    def to_csv(self):
        choice = self.numberChosen.get()
        if choice == '':
            data = self.dfm.data['price']
        else:
            data = [self.dfm.data['price'][i] for i in self.dfm.items['price'][choice]]
        fileTypes = [ ('csv files', '.csv'),('all files', '.*')]
        # define options for opening
        options = {}
        options['filetypes'] = fileTypes
        options['initialdir'] = './data/'
        options['initialfile'] = f'{time.strftime("%Y%m%d%H%M%S",time.localtime())}.csv'
        # options['title'] = ;
        path_ = asksaveasfilename(**options)
        if path_ != '':
            if path_[:-4] != '.csv': path_ += '.csv'
            with open(path_,'w',newline='',encoding='gbk') as f:
                cv1 = csv.writer(f, dialect='excel', delimiter=',')
                cv1.writerow(['商品名称', '记录时间','价格','价格变动'])
                cv1.writerows(data)

    # ****功能区
    def init_sys(self):
        '''初始化系统系统'''
        self.drawed,self.selected = set(),set()         # 去重
        # 加载常用组合
        try:
            with open('data/combo.json', 'r', encoding='utf-8') as f:  # 常用组合
                self.combo = json.load(f)
        except:
            self.combo = {}
        try:
            for k,lGoodsId in self.combo.items():
                self.dump_to_dfm(lGoodsId)
            self.groupCombo['values'] =  self.pGroupCombo['values'] = tuple(self.combo.keys())
            self.numberChosen['values'] = self.paintChosen['values'] = tuple(self.dfm.group_by('price', 0))# 单选框的取值
        except:   #数据库中无数据  或者数据库密码错误
            pass
    def dump_to_dfm(self,lGoodsId):
        '''将数据载入表格管理器
        :param lGoodsId:[id:goods]
        :return:
        '''
        iprice = Cprice()
        for gid,goods in lGoodsId:
            if goods not in self.selected:
                self.selected.add(goods)
                rst = iprice.query(gid=gid)
                if rst:
                    inst = rst[0]
                    pre_price = inst.price
                    self.dfm.insert('price', [goods, inst.date_time, inst.price, inst.price - pre_price])
                    for inst in rst[1:]:
                        self.dfm.insert('price',[goods,inst.date_time,inst.price,inst.price-pre_price])
                        pre_price = inst.price
    def update_combo(self,name,lGoodsId):
        '''更新常用组合'''
        self.combo[name] = lGoodsId
        # 1.载入数据
        self.dump_to_dfm(lGoodsId)
        # 2.更新选项
        self.groupCombo['values'] = self.pGroupCombo['values']  = tuple(self.combo.keys())
        self.numberChosen['values'] = self.paintChosen['values'] = tuple(self.dfm.group_by('price', 0))  # 单选框的取值
        return self.combo
    def load_options(self,lGoodsId):
        '''加载商品选项'''
        self.dump_to_dfm(lGoodsId)
        try:
            self.numberChosen['values'] = self.paintChosen['values'] =tuple(self.dfm.group_by('price',0)) # 单选框的取值
        except KeyError:    # 数据库无数据
            pass
    def show_table(self,event):
        '''以表格的形式显示数据'''
        self.dfm.cls('price')
        for goods in self.shunt(event):
            self.dfm.show_by('price', goods)
    def shunt(self,event):
        '''分流器，按组或者按项'''
        strs = event.widget.get()
        if strs in self.combo:
            lGoodsId = self.combo[strs]  # [(id,goods)]
            for goodsId in lGoodsId:
                yield goodsId[1]
        else:
            yield strs
    def drawPic(self,event):
        '''根据商品名字进行画图'''
        for goods in self.shunt(event):
            if goods not in self.drawed:
                self.drawed.add(goods)
                plt.xticks(rotation=20)
                data = self.dfm.data['price']
                x,y = [],[]
                for ind in self.dfm.items['price'][goods]:
                    x.append(data[ind][1].date())
                    y.append(data[ind][2])
                lines = self.ax.plot(x,y, '-', lw=2,label=goods[:10])    # 取前五个字
        plt.legend()
        self.canvas.draw()
    def drawCls(self):
        '''清除图像'''
        self.drawed = set()
        self.ax.cla()
        self.canvas.draw()
    def initFrame(self):
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
        # ** 功能标签
        y2 = 0
        label = ttk.Label(self, text='选择商品', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: GoodsTable(self.update_combo,self.load_options))
        label.place(x=10, y=y2)
        label = ttk.Label(self, text='数据信息', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: self.catch_frame.tkraise())
        label.place(x=130, y=y2)
        label = ttk.Label(self, text='绘图界面', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: self.paint_frame.tkraise())
        label.place(x=70, y=y2)

        y3 = 25
        self.paint_frame = tk.Frame(self)
        self.paint_frame.place(x=7, y=y3, height=450, width=650)
        self.catch_frame = tk.Frame(self)
        self.catch_frame.place(x=7, y=y3, height=450, width=650)

        # **** 画图界面
        ttk.Label(self.paint_frame, text='选择商品:', style="BW.TLabel").place(x=10, y=11)
        ttk.Button(self.paint_frame, text='清除', command=self.drawCls).place(x=450, y = 10)
        self.paintChosen = ttk.Combobox(self.paint_frame, width=18, state='readonly')
        self.paintChosen.bind("<<ComboboxSelected>>", self.drawPic)  # 绑定事件,(下拉列表框被选中时，绑定函数)
        self.paintChosen.place(x=85, y=11)
        self.pGroupCombo = ttk.Combobox(self.paint_frame, width=18, state='readonly')
        self.pGroupCombo.bind("<<ComboboxSelected>>", self.drawPic)  # 绑定事件,(下拉列表框被选中时，绑定函数)
        self.pGroupCombo.place(x=235, y=11)
        self.fig = plt.figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.paint_frame)  # 在Tk的GUI上放置一个画布，
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.canvas.get_tk_widget().place(x=10, y=40)
        # **** 表格展示界面
        self.numberChosen = ttk.Combobox(self.catch_frame, width=18, state='readonly')          # 组合框
        self.numberChosen.bind("<<ComboboxSelected>>", self.show_table)
        self.numberChosen.place(x=90, y=12)
        self.groupCombo = ttk.Combobox(self.catch_frame, width=18, state='readonly')          # 组合框
        self.groupCombo.bind("<<ComboboxSelected>>", self.show_table)
        self.groupCombo.place(x=240, y=12)
        ttk.Button(self.catch_frame, text='筛选', command="", width=9).place(x=10, y=10)
        ttk.Button(self.catch_frame, text='刷新', command="", width=9).place(x=390, y=10)
        ttk.Button(self.catch_frame, text='清空数据表', command=lambda: self.dfm.cls('price'), width=9).place(x=470, y=10)
        ttk.Button(self.catch_frame, text='导出表格', command=self.to_csv).place(x=550, y=10)
        # 价格信息表格
        width = 100
        columns = {'id': ("id", width),
                   'goods': ('商品名称', width),
                   "date": ("记录时间", 200),
                   'price': ('价格', width),
                   'delta_price': ('价格变动', width)}
        self.i_price = self.dfm.getDf(self.catch_frame, 'price', columns, 18, 10, 45, True)
        self.dfm.setBar(self.catch_frame, self.i_price, (613, 45, 390), (10, 432, 600))
        # 日志表格
        x_border = 670
        self.alert_frame = tk.Frame(self)
        self.alert_frame.place(x=x_border, y=y3, height=485, width=270)
        columns = {'id': ("id", 25),
                   "date": ("记录时间", 75),
                   'name': ('商品名称', 75),
                   'delta_price': ('价格变动', 75)}
        self.i_alert = self.dfm.getDf(self.alert_frame, 'alert', columns, 22, 0, 0, True)
        self.dfm.setBar(self.alert_frame, self.i_alert, (255, 0, 470), (0, 465, 250))
        self.log_frame = tk.Frame(self)
        self.log_frame.place(x=x_border, y=y3, height=485, width=270)
        columns = {'id': ("id", 25),
                   "date": ("记录时间", 75),
                   'name': ('商品名称', 100),
                   'status': ('状态', 50)}
        self.i_log = self.dfm.getDf(self.log_frame, 'logger', columns, 22, 0, 0, True)
        self.dfm.setBar(self.log_frame, self.i_log, (255, 0, 470), (0, 465, 250))
        label = ttk.Label(self, text='采集日志', style="BW.TLabel")

        label.bind('<Button-1>', lambda x: self.log_frame.tkraise())
        label.place(x=x_border, y=y2)
        label = ttk.Label(self, text='提醒', style="BW.TLabel")
        label.bind('<Button-1>', lambda x: self.alert_frame.tkraise())
        label.place(x=x_border + 70, y=y2)

class GoodsTable(tk.Toplevel):
    def __init__(self,update_combo,show=None):
        '''
        :param show:触发主界面的数据显示
        '''
        super().__init__()
        self.resizable(0, 0)  # 阻止Python GUI的大小调整
        self.title("选择商品")
        self.goodsId = {}
        self.show = show        # 将数据载入表格管理器
        self.update_combo = update_combo      # 更新常用组合
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
        ttk.Button(self, text='设为组合', command=self.set_combo, width=9).grid(cnfs['next_page'],sticky=tk.E)
        ttk.Button(self, text='修改', command=self.modify, width=9).grid(cnfs['modify'])
        ttk.Button(self, text='选择', command=self.choic, width=9).grid(cnfs['corfirm'])

    def set_combo(self):
        comboName = askstring("设置常用组合", "组合名称", initialvalue='笔记本')   # 组合名称
        goodsId = []
        for id in self.table.get_selectedRecordNames():
            goodsId.append(self.goodsId[id])
        combo= self.update_combo(comboName,goodsId)     # 更新常用组合
        with open('data/combo.json','w',encoding='utf-8') as f: # 存入文件
            json.dump(combo,f)
        self.choic()

    def add_data(self):
        '''加载配置、数据'''
        iurls = Curls()
        self.data = {}
        data = {}
        for i,inst in enumerate(iurls.query()):
            self.goodsId[i] = (inst.id,inst.goods)
            dic = {}
            dic['goods'] = inst.goods
            dic['common_price'] = inst.common_price
            dic['expect_price'] = inst.expect_price
            dic['setting'] = inst.setting
            data[i] = dic
            self.data[i] = dic.copy()
        self.table.model.importDict(data)

    def choic(self):
        try:
            if self.show is not None:
                lGoodsId = []
                for id in self.table.get_selectedRecordNames():
                    lGoodsId.append(self.goodsId[id])
                self.show(lGoodsId)
            self.destroy()
        except IndexError:
            tk.messagebox.showinfo('提示', '重新选择')
    def modify(self):
        iurls = Curls()
        for k,vals in self.table.model.data.items():
            if self.data[k] != vals:
                iurls.update(f'id={self.goodsId[k][0]}',**vals)
