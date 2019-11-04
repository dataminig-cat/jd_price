# 表格管理器
from tkinter import ttk
import tkinter as tk
class DfManager:
    def __init__(self):
        self.maps = {}  #得到不同表格实例
        # 需要一个容器来管理数据，以二位列表的形式
        self.data = {}      # 所有数据
        self.items = {}     # 存放每一项数据
        self.groups = {}    # 存放每一个组
    # 表格界面
    def getDf(self,root,id,columns,height,x,y,headings=False):
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

        self.maps[id] = dataframe
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

    # 表格插入
    def insert(self,id,msg):
        if id in self.data:
            self.data[id].append(msg)   # msg = [goods,date_time,price,price-pre_price]
            ith = len(self.data[id])
        else:
            self.data[id] = [msg]
            ith = 1
        return self.maps[id].insert("","end",text = "top",values=[ith] + msg) # 次序 + 其它数据信息
    def update(self,id,item,msg):
        return self.maps[id].item(item, values=msg)
    def group_by(self,id,ind):
        '''根据索引所在的列分组'''
        data = self.data[id]
        group = {}
        for i,l in enumerate(data):
            group[l[ind]] = group.get(l[ind],[]) + [i]  # 记录各组索引
        self.items[id] = group
        return group.keys()
    def show_by(self,id,key):
        '''分项展示'''
        data = self.data[id]
        self.cur_group = []
        for i,ind in enumerate(self.items[id][key]):
            self.cur_group.append(data[ind])
            self.maps[id].insert("","end",text = "top",values=[i+1]+data[ind]) # 次序 + 其它数据信息
    def set_group(self,groups):
        self.groups = groups
    def show_by_group(self,id,group):
        '''分组展示'''
        self.cls(id)
        data = self.data[id]
        count = 0
        for item in self.groups[group]:
            count += 1
            for ind in self.items[id][item]:
                self.maps[id].insert("", "end", text="top", values=[count] + data[ind])  # 次序 + 其它数据信息
    def cls(self,id):
        '''清空数据表'''
        df = self.maps[id]
        for k in df.get_children():
            df.delete(k)