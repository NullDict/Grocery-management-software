import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
'''设置窗口大小和名称的类,不受窗口类型的影响,使用方法为win_geometry(窗口名,宽度,高度),
此类不进行继承,经过处理的窗口按原类调用'''


class win_initialize:
    def __init__(self, master: ttk.Window, inputwidth, inputheight, title='untitled'):
        self.master = master
        self.width = inputwidth
        self.height = inputheight
        self.titile = title
        self.master.title(self.titile)
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()
        width = self.width
        height = self.height
        x = int((screenwidth-width)/2)
        y = int((screenheight-height)/2)
        if self.width >= int(13*screenwidth/14):
            x = 0
        if self.height >= int(12*screenheight/14):
            y = 0
        # if self.height-screenheight <= int(screenheight/12) and self.width == screenwidth:
        #     try:
        #         self.master.state('zoomed')
        #     except:
        #         self.master.attributes('-zoomed', True)
        #     return None
        # if width>=screenwidth or height>=screenheight:
        #     try:
        #         self.master.state('zoomed')
        #     except:
        #         self.master.attributes('-zoomed', True)
        #     return None
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# --------------------------------------------------------------------------------------------------
    # 使用实例化Treeview的方法对该类进行实例化，
    # 必要传入的参数有columnid：一个列index的列表；
    # showname，一个与columnid对应的显示列名的列表
    # columnwidth，列宽度；其余参数按treeview类传入
    #!!!!!只能接受数据库cursor反馈的数据


class table_view(ttk.Treeview):
    def __init__(self, parent, columnid, showname,  data, columnwidth=100, selectmode=BROWSE, readonly=0, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, column=columnid,
                              show='headings', selectmode=BROWSE, *args, **kwargs)
        TreeviewStyle = ttk.Style()
        TreeviewStyle.configure('Treeview', rowheight=40)
        self.parent = parent
        self.columnid = columnid
        self.showname = showname
        self.columnwidth = columnwidth
        self.database_rows = data
        self.selectmode = selectmode
        self.readonly = readonly
        self.amended_array = []
        self.delete_array = []
        self.tag_configure('amended', background='#009688', foreground='white')
        self.tag_configure('deleted', background='#F44336', foreground='white')
        self.tag_configure('outdated', background='#FF5722',
                           foreground='white')
        for i in range(len(columnid)):
            self.column(self.columnid[i],
                        width=self.columnwidth, anchor='center')
            self.heading(self.columnid[i], text=self.showname[i])
        self.bind('<Double-1>', self.entry_deploy)
    # 双击触发entry

    def entry_deploy(self, *args):
        def entry_destroy(*args):
            TreeviewEntry.destroy()
            return False
    # 不对entry中的值做任何处理，直接摧毁
        # def srollbar_entry_destroy(event):
        #     if event.x >= self.winfo_width() or event.y >= self.winfo_height() or event.x <= 0 or event.y <= 0:
        #         try:
        #             TreeviewEntry.get()
        #         except:
        #             pass
        #         else:
        #             value_deliver()
        #     pass
        # 检测到有人点击滚轮条，直接删除entry
        # 相关动作以在table_viewS中内置，该方法弃用

        def value_deliver():
            if value_list[value_id] == TreeviewEntry.get():
                TreeviewEntry.destroy()
                self.reload()
                return False
            value_list[value_id] = TreeviewEntry.get()
            # templist = (value_list[0], value_list[value_id], value_id)   #老式值返回方案，已弃用
            TreeviewEntry.destroy()
            temp = []
            for row in self.delete_array:
                if value_list[0] == row[0]:
                    temp.append(row)
                    break
            for item in temp:
                self.delete_array.remove(row)
            temp = []
            for row in self.amended_array:
                if value_list[0] == row[0]:
                    temp.append(row)
                    break
            for row in temp:
                self.amended_array.remove(row)
            self.amended_array.append(value_list)
            self.reload()
            return True

            # 修改行所有的值会被作为一个列表添加到self.amended_array中
            # 在老式返回方案中
            # deliver方法向self.amended_array末尾添加一个含三个元素的元组
            # 元组构成（所在行第一列当作主键的元素值，修改后的值，被修改元素的索引）
        if(args[0] == 'd' or self.readonly == 1):
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Entry):
                    widget.destroy()
            return True
        box = self.bbox(self.selection())
        TreeviewEntry = ttk.Entry(
            self, justify='center', width=25)
        column_len = len(self.columnid)
        value_list = list(self.item(self.selection(), option='values'))
        if len(box) < 3:
            return False
        bwidth = int(box[2]/column_len)
        entry_x = box[0]
        value_id = 0
        # 点击y轴是否在列范围内，且此时Treeview应为单选模式
        # ----------------------------------------------------------------------------------------------------------------------------

        if (args[0].y in range(box[1], box[1]+box[3])) and self.selectmode == BROWSE:
            for i in range(column_len):  # 默认第一列为不可更改的primary key
                if int(args[0].x) in range(entry_x+(i+1)*bwidth, entry_x+(i+2)*bwidth):
                    entry_x += (i+1)*bwidth  # if直接从第二列判定鼠标坐标是否在范围内
                    value_id += (i+1)  # 确定所在列index，改index为所在列的值列表的index
                    if value_id >= len(self.columnid):
                        return False
                    TreeviewEntry.place(
                        x=entry_x, y=box[1], width=bwidth, height=box[3], anchor=NW)
                    TreeviewEntry.insert(-1, value_list[value_id])
                    self.see(self.selection())
                    TreeviewEntry.focus_set()
                    TreeviewEntry.bind(
                        '<FocusOut>', lambda event: value_deliver())
                    self.bind('<Configure>', lambda event: entry_destroy())
                    #self.parent.bind('<1>', srollbar_entry_destroy)
                    #self.bind('<Leave>', srollbar_entry_destroy)
                    TreeviewEntry.bind(
                        '<MouseWheel>', lambda event: entry_destroy())
                    self.bind('<MouseWheel>', lambda event:  entry_destroy())
                    self.parent.bind(
                        '<MouseWheel>', lambda event:  entry_destroy())
                    TreeviewEntry.bind(
                        '<Return>', lambda event: value_deliver())
                    TreeviewEntry.bind(
                        '<Escape>', lambda event: entry_destroy())
        return 0
        # 进行监视的三个动作分别为：entry失焦：直接摧毁entry中止输入；
        # sheetview大小改变：直接摧毁entry中止输入，此举是防止窗口大小改变后entry在错误位置
        # 回车键被按下：执行值传递

    def clear(self):
        childrens = self.get_children()
        for i in childrens:
            self.delete(i)
        return True
        # 清空sheetview上的所有内容

    def deliver(self):
        temp = self.amended_array
        self.amended_array = []
        return temp
        # 将值传出后重置实例内部存储的值

    def delete_passing(self):
        temp = []
        for row in self.delete_array:
            temp.append(row[0])
        self.delete_array = []
        return temp

    def get_amended(self):
        return self.amended_array
        # 传出值，但不重置实例存储数据

    def get_deleted(self):
        return self.delete_array

    def load(self):
        insert_flag = 0
        for row in self.database_rows:
            for amended_row in self.amended_array:
                if row[0] == amended_row[0]:
                    self.insert('', 'end', values=amended_row, tags='amended')
                    insert_flag = 1
                    break
            for deleted_row in self.delete_array:
                if row[0] == deleted_row[0]:
                    self.insert('', 'end', values=deleted_row, tags='deleted')
                    insert_flag = 1
                    break
            if insert_flag == 0:
                self.insert('', 'end', values=row)
            insert_flag = 0
        return True

    def entry_state(self, state):
        if state == 0:
            self.config(selectmode=EXTENDED)
            self.selectmode = EXTENDED
            return True
        if state == 1:
            self.config(selectmode=BROWSE)
            self.selectmode = BROWSE
            return True
        return False

    def reload(self, data=0):
        if data != 0:
            self.database_rows = data
        self.clear()
        self.load()
        return True

    def delete_row(self):
        delete_table_index = self.selection()
        delete_index_dict = {}
        for row in self.delete_array:
            delete_index_dict[row[0]] = row
        for item in delete_table_index:
            if(self.item(item, option='values'))[0] not in delete_index_dict:
                self.delete_array.append(
                    list(self.item(item, option='values')))
            else:
                if (list(self.item(item, option='values'))) in self.database_rows:
                    self.delete_array.remove(
                        delete_index_dict[(self.item(item, option='values'))[0]])
                if (list(self.item(item, option='values'))) not in self.database_rows:
                    self.amended_array.append(
                        list(self.item(item, option='values')))
                    self.delete_array.remove(
                        delete_index_dict[(self.item(item, option='values'))[0]])
        self.reload()
        temp = []
        for row in self.amended_array:
            for delete_row in self.delete_array:
                if row[0] == delete_row[0]:
                    temp.append(row)
                    break
        for row in temp:
            self.amended_array.remove(row)
        temp = []
        self.reload()
        return True

    def selected_value(self):
        temp = []
        for index in self.selection():
            temp.append(self.item(index, option='values'))
        return temp


class table_viewS(ttk.Frame):
    def __init__(self, parent, columnid, showname,  data, columnwidth=100, selectmode=BROWSE, readonly=0, *args, **kwargs):
        ttk.Frame.__init__(self, parent)
        # 变量转接
        self.parent = parent
        self.columnid = columnid
        self.showname = showname
        self.columwidth = columnwidth
        self.data = data
        self.selectmode = selectmode
        self.readonly = readonly
        self.args = args
        self.kargs = kwargs

        # 内部变量
        self.search_result = []
        self.delete_array = []
        self.multiselect_var = ttk.IntVar(value=1)

        # 内部方法
        def search():
            data_array = self.data
            for row in data_array:
                for item in row:
                    if search_entry.get().upper() in str(item).upper():
                        self.search_result.append(row)
                        break
            self.temp_load(self.search_result)
            self.search_result = []
            return True

        def reset():
            self.reload()
            return True

        def multi_select():
            if self.multiselect_var.get() == 0:
                self.InnerTableview.entry_state(self.multiselect_var.get())
            if self.multiselect_var.get() == 1:
                self.InnerTableview.entry_state(self.multiselect_var.get())
                temp_id_array = self.InnerTableview.selection()
                for item in temp_id_array:
                    self.InnerTableview.selection_remove(item)
            return True

        # def delete():
        #     pass

        # 组件定义
        self.InnerTableview = table_view(
            self, self.columnid, self.showname,  self.data, self.columwidth, selectmode=self.selectmode, readonly=self.readonly)
        search_entry = ttk.Entry(
            self, width=40, validate='key', validatecommand=search)
        search_entry.bind('<Return>', lambda event: search)
        search_label = ttk.Label(self, text='  搜索:', justify=RIGHT)
        scrollbar = ttk.Scrollbar(
            self, command=self.InnerTableview.yview)

        def scroll_command(*args):
            self.InnerTableview.entry_deploy('d')
            scrollbar.set(first=args[0], last=args[1])
        self.InnerTableview.config(yscrollcommand=scroll_command)
        search_button = ttk.Button(self, text='搜索', command=search)
        ToolTip(search_button, text="点击搜索")
        reset_button = ttk.Button(self, text='刷新', command=reset)
        ToolTip(reset_button, text="退出搜索恢复到默认视野")
        multiselect_button = ttk.Checkbutton(
            self, text='多选模式', variable=self.multiselect_var, command=multi_select, onvalue=0, offvalue=1, bootstyle="warning-square-toggle")
        ToolTip(multiselect_button,
                text='''开启多选模式，按住Ctrl键点击待删除行，开启后无法触发修改，关闭后恢复。如果想取消修改
                ，双击需取消删除行的任一可修改项后，按Enter键将行状态修改为待修改即可。''', wraplength=90)
        delete_button = ttk.Button(
            self, text='删除', command=self.delete_row, bootstyle='warning')
        if self.readonly == 1:
            delete_button.config(state='disable')
            multiselect_button.config(state='disable')
        if readonly != 1:
            ToolTip(delete_button, text="将目标标记为删除，点击应用修改后生效", wraplength=10)
        else:
            ToolTip(delete_button, text="查询模式下不可进行删除操作！", wraplength=10)
        search_label.grid(column=0, row=0, padx=(10, 0),
                          pady=5,  sticky=(W, S, N, E))
        search_entry.grid(column=1, row=0, columnspan=3,
                          padx=(0, 5), pady=5, sticky=(W, S, N, E))
        search_button.grid(column=4, row=0, padx=5,
                           pady=5, sticky=(W, S, N, E))
        reset_button.grid(column=5, row=0, padx=5, pady=5, sticky=(W, S, N, E))
        multiselect_button.grid(column=6, row=0, padx=5,
                                pady=5, sticky=(W, S, N, E))
        delete_button.grid(column=7, row=0, padx=5,
                           pady=5, sticky=(W, S, N, E))
        self.InnerTableview.grid(
            column=0, row=1, columnspan=8, rowspan=6, sticky=(W, S, N, E))
        scrollbar.grid(column=8, row=1, rowspan=6, sticky=(W, S, N, E))
        for i in range(6):
            self.columnconfigure(i, weight=1)
        for i in range(1, 7):
            self.rowconfigure(i, weight=1)

# 传递table_view的方法
    def clear(self):
        t = self.InnerTableview.clear()
        return t

    def deliver(self):
        t = self.InnerTableview.deliver()
        return t

    def delete_passing(self):
        t = self.InnerTableview.delete_passing()
        return t

    def get_amended(self):
        t = self.InnerTableview.get_amended()
        return t

    def get_deleted(self):
        t = self.InnerTableview.get_deleted()
        return t

    def load(self):
        t = self.InnerTableview.load()
        return t

    def reload(self, data=0):
        if data != 0:
            self.data = data
        else:
            data = self.data
        t = self.InnerTableview.reload(data)
        return t

    def temp_load(self, data=0):
        t = self.InnerTableview.reload(data)
        return t

    def entry_state(self, state):
        t = self.InnerTableview(state)
        return t

    def delete_row(self):
        t = self.InnerTableview.delete_row()
        return t

    def selected_value(self):
        t=self.InnerTableview.selected_value()
        return t