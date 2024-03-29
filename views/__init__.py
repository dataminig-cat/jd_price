from views.df_manager import *
import tkinter.messagebox
from tkinter.filedialog import askdirectory, askopenfilename
import matplotlib.pyplot as plt
import json
from views.search_frame import SearchFrame
from threading import Thread
from views.info_frame import InfoFrame
try:
    from db_tools.url import Curls
except:
    pass
class Itf(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('960x600+200+100')  # 设置窗口大小和相对屏幕位置
        self.resizable(0, 0)  # 阻止Python GUI的大小调整
        self.protocol("WM_DELETE_WINDOW", self.close)  # 关闭时触发时触发函数
        self.title("价格监测")
        self.xx, self.yy = 0, 0
        self.initFFrame()

    # *****功能区*****
    def callback(self, event):
        print("当前位置：", event.x, event.y, '\t间隔：', event.x - self.xx, event.y - self.yy)
        self.xx, self.yy = event.x, event.y

    def bulk_load(self):  #批量d导入
        def get_detail():
            iurls = Curls()
            urls = self.text.get(1.0, tk.END)
            urls = urls.split('\n')[:-1]
            if urls == ['']:
                tk.messagebox.showinfo('提示', '不能为空')
            else:
                for i in range(len(urls)):
                    iurls.update(f'url={urls[i]}',setting=1,goods='')
                self.crawl_goods(urls)
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
    def search(self):
        self.sFrame.tkraise()
        if self.crawler is not None:
            self.sFrame.data = []   # 清空数据表
            urls = ['https://search.jd.com/Search?keyword=%s&enc=utf-8&page=%d' % (self.v.get(), 1)]
            thread = Thread(target=self.crawler.search_goods,args=(urls,))
            thread.start()
    def crawl(self):
        if self.crawler is not  None:
            thread = Thread(target=self.crawler.run)
            thread.start()
    def crawl_goods(self,urls):
        if self.crawler is not None:
            thread = Thread(target=self.crawler.set_goods_name,args=(urls,))
            # thread.setDaemon(True)
            thread.start()
    def setting_(self):
        def show():
            mysql_name = e1.get()
            mysql_password =  e2.get()
            send_email_name = e3.get()
            craw_fre = e4.get()
            if mysql_name != '' and mysql_password != '':
                data['url'] = 'mysql+pymysql://'+mysql_name+':'+mysql_password+'@'+"localhost:3306/"
            if craw_fre != '':
                data['frq'] = craw_fre
            if send_email_name != '':
                data['receiver'] = send_email_name
            with open('setting.json', 'w', encoding='utf-8') as fw: #存入文件
                json.dump(data, fw, ensure_ascii=False, indent=4)
            setting_win.destroy()
        with open('setting.json', encoding='utf-8') as f:
            data = json.load(f)
        setting_win = tk.Tk()
        setting_win.geometry('600x450+400+150')
        ttk.Label(setting_win, text='设置', style="BW.TLabel").place(x=300, y=30)
        ttk.Label(setting_win, text='数据库名称', style="BW.TLabel").place(x=100, y=80)
        ttk.Label(setting_win, text='数据库密码', style="BW.TLabel").place(x=100, y=120)
        ttk.Label(setting_win, text='接受QQ邮箱账号', style="BW.TLabel").place(x=100, y=160)
        ttk.Label(setting_win, text='爬虫频率(天)', style="BW.TLabel").place(x=100, y=200)
        e1 = tk.Entry(setting_win,width=40)
        e2 = tk.Entry(setting_win,width=40)
        e3 = tk.Entry(setting_win, width=40)
        e4 = tk.Entry(setting_win, width=40)

        _,usr,psw,_ = data['url'].split(':')
        psw,_ = psw.split('@')
        e1.insert(0,usr[2:])
        e2.insert(0, psw)
        e3.insert(0,data['receiver'])
        e4.insert(0, data['frq'])
        e1.place(x=200, y=80)
        e2.place(x=200, y=120)
        e3.place(x=200, y=160)
        e4.place(x=200, y=200)

        tk.Button(setting_win, text="保存", width=10, command=show).grid(row=3, column=0, sticky="w", padx=80, pady=370)
        tk.Button(setting_win, text="退出", width=10, command=setting_win.destroy).grid(row=3, column=1, sticky="e", padx=150, pady=370)

    def initFFrame(self):
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
                iurls.update(f'url={url}', setting=1, )
                self.crawl_goods(urls=[url])
                tk.messagebox.showinfo('提示', '导入成功')

        path = tk.StringVar()
        # 创建一个名为File的菜单项
        menuBar = tk.Menu(self)
        self.config(menu=menuBar)
        menu_tool = tk.Menu(menuBar, tearoff=False)  # 工具栏
        menu_tool.add_command(label='导入文件', command=selectPath)
        menu_tool.add_command(label='设置', command=self.setting_)
        menuBar.add_cascade(label="菜单", menu=menu_tool)

        # 搜索商品
        y0 = 10
        ttk.Label(self, text='搜索商品：', style="BW.TLabel").place(x=10, y=y0)
        self.v = tk.StringVar()
        tk.Entry(self, borderwidth=3, width=40, textvariable=self.v, selectbackground='gray').place(x=70,
                                                                                                      y=y0)  # 输入框的位置设定
        ttk.Button(self, text='搜索', command=self.search, width=9).place(x=370, y=y0)

        # 爬虫需要的url输入框
        y1 = 40
        ttk.Label(self, text='导入链接：', style="BW.TLabel").place(x=10, y=y1)
        v = tk.StringVar()
        tk.Entry(self, borderwidth=3, width=40, textvariable=v, selectbackground='gray').place(x=70,
                                                                                                      y=y1)  # 输入框的位置设定
        ttk.Button(self, text='导入', command=insert_url, width=9).place(x=370, y=y1)
        ttk.Button(self, text='批量导入', command=self.bulk_load, width=9).place(x=450, y=y1)
        ttk.Button(self, text='开始爬取', command=self.crawl, width=9).place(x=530, y=y1)

        self.iFrame = InfoFrame(self)
        self.iFrame.place(x=0, y=75, height=525, width=960)
        self.sFrame = SearchFrame(self)
        self.sFrame.place(x=0, y=75, height=525, width=960)
        self.iFrame.tkraise()
        self.iFrame.bind("<Double-1>", self.callback)  # 调试用：输出鼠标位置
    def set_crawler(self,crawler):
        self.crawler = crawler
        self.iFrame.crawler = crawler

    def close(self):
        plt.close(self.iFrame.fig)
        self.destroy()