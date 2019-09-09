# 表格管理器
from tkinter import ttk
import tkinter as tk
class DfManager:
    def __init__(self):
        self.maps = {}  #得到不同表格实例
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
        return self.maps[id].insert("","end",text = "top",values=msg)

    def update(self,id,item,msg):
        return self.maps[id].item(item, values=msg)
