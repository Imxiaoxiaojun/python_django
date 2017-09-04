# -*- coding: UTF-8 -*-
from Tkinter import *
import ttk
from DBUtil import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Search(Frame):
    def search(self):
        self.vd_list = []
        items = self.vdList.get_children()
        [self.vdList.delete(item) for item in items]
        vd_name = str(self.searchName.get()).strip()
        vd_type = str(self.searchType.get()).strip()
        if vd_name != "" and vd_type != "":
            vd_name = '%' + vd_name + '%'
            param = [vd_name]
            conn = Mysql()
            sql = "select ftp_name,ftp_url from ftplink where ftp_name like %s order by ftp_name asc "
            self.vd_list.extend(conn.getAll(sql, param))
        for i in range(len(self.vd_list)):
            self.vdList.insert('', i, values=(self.vd_list[i]['ftp_name'], self.vd_list[i]['ftp_url']))

    def create_widgets(self):
        self.name = ttk.Label(self.searchframe)
        self.name["text"] = "Name:"
        self.name.pack(side=LEFT)

        self.searchName = ttk.Entry(self.searchframe, width=15)
        self.searchName.focus()
        self.searchName.pack(side=LEFT)

        self.searchType = ttk.Combobox(self.searchframe, width=6)
        self.searchType['values'] = ['电影', '电视剧']
        self.searchType.current(0)  # 设置初始显示值，值为元组['values']的下标
        self.searchType.config(state='readonly')  # 设为只读模式
        self.searchType.pack(side=LEFT)

        self.search = ttk.Button(self.searchframe, command=self.search)
        self.search["text"] = "Search"
        self.search.pack(side=LEFT)

        self.vdList = ttk.Treeview(self.bottomframe, columns=['name', 'url'], show='headings')
        self.vdList.heading('name', text='name')
        self.vdList.heading('url', text='url')
        vbar = ttk.Scrollbar(root, orient=VERTICAL, command=self.vdList.yview)
        self.vdList.configure(yscrollcommand=vbar.set)
        self.vdList.grid(row=0, column=0, sticky=NSEW)
        self.vdList.pack(padx=100, ipady=150, side=LEFT)
        vbar.grid()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(side=TOP)

        self.searchframe = Frame(root)
        self.searchframe.pack(side=TOP)

        self.bottomframe = Frame(root)
        self.bottomframe.pack(side=TOP)
        self.create_widgets()


root = Tk()
root.geometry("800x600")
app = Search(master=root)
app.mainloop()

root.mainloop()
