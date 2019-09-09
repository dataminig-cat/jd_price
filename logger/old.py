def logging():
    # **文本框部分：提醒日志
    y_border = 670
    y_scroll = 940
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="#DCDCDC")
    self.l_raw = tk.StringVar(self.fFrame)  # 传入的字符变量
    self.l_raw.set(('初始化', 1, 2, 3))
    ttk.Label(self.fFrame, text='提醒日志', style="BW.TLabel").place(x=y_border, y=50)
    self.l_logs = tk.StringVar(self.fFrame)  # 传入的字符变量
    self.l_logs.set(('初始化', 1, 2, 3))
    self.logger = tk.Listbox(self.fFrame, listvariable=self.l_logs,
                             height=25, width=35)
    self.logger.place(x=y_border, y=100)
    # 滚动条
    scroll = tk.Scrollbar(self.fFrame, command=self.logger.yview)  # 类似回调函数
    scroll.place(x=y_scroll, y=100, height=500)
    self.logger.configure(yscrollcommand=scroll.set)