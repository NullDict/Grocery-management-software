import re
import tkinter as tk
import ttkbootstrap as ttk
import time
import datetime
from tkinter import messagebox
from ttkbootstrap.constants import *
from db_classes import *
from StableClass import *
from ttkbootstrap.tooltip import ToolTip
from decimal import Decimal

Querybox = ttk.dialogs.dialogs.Querybox


def verify_date(datetime_str):
    try:
        datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def verify_datetime(datetime_str):
    try:
        datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def stamp_to_time_str(time_stamp,mode=1):
    if mode == 1:
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
    elif mode == 2:
        time_str = time.strftime("%Y-%m-%d", time.localtime(time_stamp))
    return time_str
    
def time_str_to_stamp(time_str,mode=1):
    if mode == 1:
        time_stamp = int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")))
    elif mode == 2:
        time_stamp = int(time.mktime(time.strptime(time_str, "%Y-%m-%d")))
    return time_stamp
class pop_menu:
    def __init__(self, parent) -> None:
        self.event = None

        def popmenu_post(event):
            self.event = event
            menu.post(event.x_root, event.y_root)

        def commands(type):
            if type == 0:
                self.event.widget.event_generate('<<Copy>>')
            if type == 1:
                self.event.widget.event_generate('<<Paste>>')
            if type == 2:
                self.event.widget.event_generate('<<Cut>>')
        self.parent = parent
        menu = ttk.Menu(self.parent, tearoff=0)
        menu.add_command(label="复制", command=lambda: commands(0))
        menu.add_separator()
        menu.add_command(label="粘贴", command=lambda: commands(1))
        menu.add_separator()
        menu.add_command(label="剪切", command=lambda: commands(2))
        self.parent.bind('<3>', popmenu_post)

class member_frame_init:
    def __init__(self, parent: ttk.Frame) -> None:
        self.insert_panel_exist = False
        member_columnid = ['id', 'name', 'wallet', 'points', 'date']
        member_showname = ['电话号码', '姓名', '余额', '消费积分', '注册日期']
        self.parent = parent
        self.db = DB_member()
        self.data = self.db.data_load()
        self.member_table = table_viewS(
            self.parent, columnid=member_columnid, showname=member_showname, data=self.data, columnwidth=100)
        ToolTip(self.member_table,text='''选中任一行，双击待修改数据后开启修改\n电话号码为关键信息不可修改，如需修改请重新创建会员''')
        self.member_table.load()
        self.new_button = ttk.Button(
            self.parent, text='添加用户', command=self.new_member, bootstyle='success')
        self.apply_button = ttk.Button(
            self.parent, text='应用修改', command=self.apply_all, bootstyle='info')
        self.tips_label = ttk.Label(self.parent, text='❓', justify='center')
        ToolTip(self.tips_label,
                text='''如果想取消修改，双击需取消删除行的任一可修改项后，按Enter键将行选项修改为待修改即可。\n注意！！！！在这种情况下您必须点击应用修改''', wraplength=200)
        self.member_table.grid(column=0, row=0, columnspan=5,
                               rowspan=5, sticky=(W, S, N, E))
        self.new_button.grid(column=1, row=5, padx=5,
                             pady=5, sticky=(W, S, N, E))
        self.tips_label.grid(column=2, row=5, padx=5, pady=5)
        self.apply_button.grid(column=3, row=5, padx=5,
                               pady=5, sticky=(W, S, N, E))
        for i in range(5):
            self.parent.columnconfigure(i, weight=1)
        for i in range(5):
            self.parent.rowconfigure(i, weight=2)
        self.parent.rowconfigure(5, weight=1)
# ------------------------------------------------------------------------------------------------------------------------------------------

    def new_member(self):
        def validate(id):
            if id == 'number':
                if re.compile('^[+1]\d{6,15}$').match(number_entry.get()):
                    number_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if number_entry.get() != '':
                        notice_label.config(
                            text='          错误的电话号码格式，电话号码应为以+或数字开头,8至16位长', width=42, justify='center')
                        number_entry.config(bootstyle='danger')
            if id == 'points':
                if re.compile('^[0-9]+\.?[0-9]*$').match(points_entry.get()):
                    points_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if points_entry.get() != '':
                        notice_label.config(
                            text='          错误的积分格式，积分必须为一个大于零的数字，保存时只保存整数部分', width=42, justify='center')
                        points_entry.config(bootstyle='danger')
            if id == 'wallet':
                if re.compile('^[0-9]+\.?[0-9]*$').match(wallet_entry.get()):
                    wallet_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if wallet_entry.get() != '':
                        notice_label.config(
                            text='      错误的余额格式，积分必须为一个大于零的数字，保存时保存到小数点后两位', width=42, justify='center')
                        wallet_entry.config(bootstyle='danger')
            return True

        def cancel_insert():
            new_member_win.destroy()
            self.insert_panel_exist = False

        def date_insert():
            t = str(Querybox.get_date(register_date_label))
            register_date_entry.config(state='normal')
            register_date_entry.delete(0, 'end')
            try:
                register_date_entry.insert('end', t)
            except:
                register_date_entry.insert('end', t)
            register_date_entry.config(state='readonly')

        def apply_insert():
            if re.compile('^[+1]\d{6,15}$').match(number_entry.get()) == None:
                messagebox.showerror(parent=new_member_win,
                                     title='电话号码格式错误', message='电话号码格式错误，请修正！')
                return False
            if re.compile('^[0-9]+\.?[0-9]*$').match(points_entry.get()) == None:
                messagebox.showerror(parent=new_member_win,
                                     title=' 积分格式错误', message='积分格式错误，请修正！')
                return False
            if re.compile('^[0-9]+\.?[0-9]*$').match(wallet_entry.get()) == None:
                messagebox.showerror(parent=new_member_win,
                                     title=' 余额格式错误', message='余额格式错误，请修正！')
                return False
            if name_entry == '':
                messagebox.showerror(parent=new_member_win,
                                     title=' 用户名错误', message='用户名不能为空！')
                return False
            if register_date_entry == '':
                messagebox.showerror(parent=new_member_win,
                                     title=' 注册日期错误', message='注册日期不能为空！')
                return False
            information_set = []
            information_set.append(number_entry.get())
            information_set.append(name_entry.get())
            information_set.append(
                str(Decimal(wallet_entry.get()).quantize(Decimal('0.00'))))
            information_set.append(str(int(points_entry.get())))
            information_set.append(register_date_entry.get())
            t = self.db.data_insert(information_set)
            if t != True:
                messagebox.showerror(
                    title='错误', message='错误类型:{}\n插入失败'.format(t))
                self.data = self.db.data_load()
                self.member_table.reload(self.data)
                return False
            self.data = self.db.data_load()
            self.member_table.reload(self.data)
            messagebox.showinfo(title='插入成功', message='插入成功')
            cancel_insert()
            return True
        # ---------------------------------------------------------------------
        if self.insert_panel_exist:
            self.insert_panel_exist == True
            return False
        self.insert_panel_exist = True
        label_font_style = ttk.Style()
        label_font_style.configure(
            style='notice.TLabel', font=('Helvetica', 14))
        new_member_win = ttk.Toplevel()
        pop_menu(new_member_win)
        win_initialize(new_member_win, 800, 462, '新增用户')
        new_member_win.resizable(0, 0)
        name_label = ttk.Label(new_member_win, text='姓名:')
        name_entry = ttk.Entry(new_member_win, justify='left')
        register_date_label = ttk.Label(new_member_win, text='注册日期:')
        register_date_entry = ttk.Entry(new_member_win, justify='left',
                                        validate='all', validatecommand=lambda: validate('date'))
        wallet_label = ttk.Label(new_member_win, text='余额:')
        wallet_entry = ttk.Entry(new_member_win, justify='left',
                                 validate='all', validatecommand=lambda: validate('wallet'))
        points_label = ttk.Label(new_member_win, text='积分:')
        points_entry = ttk.Entry(new_member_win, justify='left',
                                 validate='all', validatecommand=lambda: validate('points'))
        number_label = ttk.Label(new_member_win, text='电话:')
        number_entry = ttk.Entry(new_member_win, justify='left',
                                 validate='all', validatecommand=lambda: validate('number'))
        notice_label = ttk.Label(
            new_member_win, text='',
            width=42, justify='center', style='notice.TLabel')
        # notice_label2=ttk.Label(new_member_win,text='',justify='center')
        apply_button = ttk.Button(
            new_member_win, text='确认插入', bootstyle='success', command=apply_insert)
        exit_button = ttk.Button(
            new_member_win, text='取消插入', bootstyle='danger', command=cancel_insert)

        # points_entry.insert(0,'0')
        register_date_entry.config(state='readonly')
        register_date_entry.bind('<1>', lambda e: date_insert())
        # -------------------------------------------------------------------------------------------------------------------------
        name_label.grid(column=1, row=0, padx=5, pady=5, stick=(E, W, S, N))
        name_entry.grid(column=2, row=0, columnspan=2,
                        padx=5, pady=5, stick=(E, W, S, N))
        register_date_label.grid(
            column=4, row=0, padx=5, pady=5, stick=(E, W, S, N))
        register_date_entry.grid(column=5, row=0, columnspan=2, padx=(
            5, 50), pady=5, stick=(E, W, S, N))
        wallet_label.grid(column=1, row=1, padx=5, pady=5, stick=(E, W, S, N))
        wallet_entry.grid(column=2, row=1, columnspan=2,
                          padx=5, pady=5, stick=(E, W, S, N))
        points_label.grid(column=4, row=1, padx=5, pady=5, stick=(E, W, S, N))
        points_entry.grid(column=5, row=1, columnspan=2,
                          padx=(5, 50), pady=5, stick=(E, W, S, N))
        number_label.grid(column=1, row=2, padx=5, pady=5, stick=(E, W, S, N))
        number_entry.grid(column=2, row=2, columnspan=5,
                          padx=(5, 50), pady=5, stick=(E, W, S, N))
        notice_label.grid(column=1, row=3, columnspan=6,
                          padx=5, pady=5, stick=(E, W, S, N))
        # notice_label2.grid(column=1,row=4,columnspan=6,padx=5,pady=5,stick=(E,W ))
        apply_button.grid(column=1, row=5, columnspan=2,
                          padx=(50, 5), pady=20, stick=(E, W, S, N))
        exit_button.grid(column=6, row=5, padx=(
            5, 50), pady=20, stick=(E, W, S, N))
        # -------------------------------------------------------------------------------------------------------------------------
        for i in range(7):
            new_member_win.columnconfigure(i, weight=1)
        for i in range(6):
            new_member_win.rowconfigure(i, weight=1)
        new_member_win.protocol("WM_DELETE_WINDOW", cancel_insert)
        # #第一行
        # name_label.place(x = 92,y = 68,width = 145,height = 52)
        # name_entry.place(x = 273,y = 68,width = 180,height = 52)
        # register_date_label.place(x = 537,y = 68,width = 145,height = 52)
        # register_date_entry.place(x = 719,y = 68,width = 180,height = 52)
        # #第二行
        # wallet_label.place(x = 92,y = 212,width = 145,height = 52)
        # wallet_entry.place(x = 273,y =212,width = 180,height = 52)
        # points_label.place(x = 537,y = 212,width = 145,height = 52)
        # points_entry.place(x = 719,y = 212,width = 180,height = 52)
        # #第三行
        # number_label.place(x = 92,y = 319,width = 145,height = 52)
        # number_entry.place(x = 273,y = 318,width = 628,height = 52)
        # #状态反馈行
        # notice_label1.place(x = 92,y = 383,width = 807,height = 52)
        # notice_label2.place(x = 92,y = 451,width = 807,height = 52)
        # #按钮行
        # apply_button.place(x = 92,y = 506,width = 114,height = 52)
        # exit_button.place(x = 815,y = 506,width = 114,height = 52)

    def delete_member(self):
        delete_list = self.member_table.delete_passing()
        if delete_list == []:
            return False
        t = self.db.data_delete(delete_list)
        if t != True:
            messagebox.showerror(
                title='删除值时发生错误', message='发生错误行的电话号码及错误类型为:{}'.format(t))
        del t
        self.data = self.db.data_load()
        self.member_table.reload(self.data)

    def modify_member(self):
        data_rows = self.member_table.deliver()
        error_list = []
        able_to_apply_row = []
        for row in data_rows:
            error_row = []
            if re.compile('^[+1]\d{6,15}$').match(row[0]) == None:
                error_row.append('电话号码格式错误')
            if re.compile('^[0-9]+\.?[0-9]*$').match(row[2]) == None:
                error_row.append('余额格式错误')
            if re.compile('^[0-9]+\.?[0-9]*$').match(row[3]) == None:
                error_row.append('积分格式错误')
            if row[1] == '':
                error_row.append('姓名不能为空')
            if verify_date(row[4]) == False:
                error_row.append('错误的时间格式')
            if error_row == []:
                able_to_apply_row.append(row)
            else:
                error_list.append(['电话号码为'+row[0]+'的行发现错误：', error_row])
                error_row = []
        for row in able_to_apply_row:
            row[2] = str(Decimal(row[2]).quantize(Decimal('0.00')))
            row[3] = str(int(row[3]))
        result = self.db.date_update(able_to_apply_row)
        self.data = self.db.data_load()
        self.member_table.reload(self.data)
        if error_list != [] or result != True:
            error_show_window = ttk.Toplevel()
            pop_menu(error_show_window)
            error_show_window.resizable(0, 0)
            win_initialize(error_show_window, 600, 346, '错误列表')
            show_text = ttk.Text(error_show_window, width=600, height=346)
            show_text.grid()
            if error_list != []:
                for row in error_list:
                    show_text.insert('end', row)
                    show_text.insert(tk.INSERT, '\n')
            if result != True:
                for row in result:
                    show_text.insert('end', row)
                    show_text.insert(tk.INSERT, '\n')
            show_text.insert('end', '其他行均修改成功！')
            show_text.config(state='disabled')
        if error_list == [] and result == True:
            messagebox.showinfo(title='修改成功', message='所有修改操作都成功了！')

    def apply_all(self):
        self.delete_member()
        self.modify_member()
    def flush_data(self):
        self.data = self.db.data_load()
        self.member_table.reload(self.data)

class stock_frame_init:
    def __init__(self, parent: ttk.Frame) -> None:
        self.parent = parent
        self.db = DB_stock()
        self.insert_panel_exist = False
        self.__auto_count_flag = [0, 0, 0]
        stock_columnid = ['id', 'catagory', 'batch', 'price',
                          'quantity', 'unit_price', 'sell_price', 'date', 'period']
        stock_showname = ['货物识别码', '种类', '批次',
                          '总进价(元)', '总货量(斤)', '存放位置', '计划售价(元/斤)', '进货时间', '剩余保质期/天']
        #self.data = self.db.data_load()
        self.data = self.data_load()
        self.stock_table = table_viewS(
            self.parent, columnid=stock_columnid, showname=stock_showname, data=self.data, columnwidth=100)
        ToolTip(self.stock_table,text='''选中任一行后，在该行待修改值上双击开启修改\n货物识别码不可修改
        注意:对种类和批次的修改不会被记录，如需修改此类关键信息请重新新增进货。''')
        self.stock_table.load()
        self.new_button = ttk.Button(
            self.parent, text='新增进货', bootstyle='success', command=self.new_stock)
        self.loss_button = ttk.Button(
            self.parent, text='  报损  ', bootstyle='warning',command=self.report_loss)
        self.apply_button = ttk.Button(
            self.parent, text='应用修改', bootstyle='info', command=self.appply_stock_all)
        self.stock_table.grid(column=0, row=0, columnspan=5,
                              rowspan=5, sticky=(W, S, N, E))
        self.new_button.grid(column=1, row=5, padx=5,
                             pady=5, sticky=(W, S, N, E))
        self.loss_button.grid(column=2, row=5, padx=5,
                              pady=5, sticky=(W, S, N, E))
        self.apply_button.grid(column=3, row=5, padx=5,
                               pady=5, sticky=(W, S, N, E))
        for i in range(5):
            self.parent.columnconfigure(i, weight=1)
        for i in range(5):
            self.parent.rowconfigure(i, weight=2)
        self.parent.rowconfigure(5, weight=1)

    def new_stock(self):
        def cancel_insert():
            new_stock_win.destroy()
            self.insert_panel_exist = False

        def batch_check():
            catagory_entry.config(bootstyle='default')
            batch_combobox.config(state='readonly')
            batch_checklist = self.db.batch_check(catagory_entry.get())
            spare_batch = []
            for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if i not in batch_checklist:
                    spare_batch.append(i)
            if spare_batch == []:
                if batch_combobox.get != '':
                    notice_label.config(text='已达到最大批次,\n请手动输入批次号')
                batch_combobox.config(state='normal')
                batch_combobox.delete(0,'end')
                batch_combobox.insert(0,'请输入批次号')
                batch_combobox.config(values=[])
            else:
                batch_combobox.config(values=spare_batch)
                batch_combobox.current(0)
                period_combobox.current(1)
            if catagory_entry.get() == '':
                notice_label.config(text='商品种类不能为空！',)
                catagory_entry.config(bootstyle='danger')
            return True

        def set_default_style():
            quantity_entry.config(bootstyle='default')
            total_price_entry.config(bootstyle='default')
            unit_price_entry.config(bootstyle='default')

        def date_insert():
            t = str(Querybox.get_date(date_label))+' '+time.strftime("%H:%M:%S",time.localtime())
            date_entry.delete(0, 'end')
            # try:
            date_entry.insert('end', t)
            # except:
            #     date_entry.insert('end', t)

        def datetime_wash(signal=0):
            if signal == 0:
                unwashed_date = date_entry.get()
            else:
                unwashed_date = signal
            washed_date = ''
            for i in unwashed_date:
                if i == '：':
                    washed_date = washed_date+':'
                    continue
                washed_date = washed_date+i
            return washed_date

        def auto_ccount():
            total_price_entry.config(state='normal')
            quantity_entry.config(state='normal')
            unit_price_entry.config(state='normal')
            if self.__auto_count_flag[0] == 1 and self.__auto_count_flag[1] == 1:
                if total_price_entry.get() == '' or quantity_entry.get() == '':
                    return False
                if int(float(total_price_entry.get())) == 0 or int(float(quantity_entry.get())) == 0:
                    return False
                temp = float(total_price_entry.get()) / \
                    float(quantity_entry.get())
                temp = str(Decimal(temp).quantize(Decimal('0.00')))
                unit_price_entry.delete(0, 'end')
                unit_price_entry.insert(0, temp)
                unit_price_entry.config(state='disable')
                self.__auto_count_flag[2] = 0
                set_default_style()
            elif self.__auto_count_flag[0] == 1 and self.__auto_count_flag[2] == 1:
                if unit_price_entry.get() == '' or quantity_entry.get() == '':
                    return False
                if int(float(unit_price_entry.get())) == 0 or int(float(quantity_entry.get())) == 0:
                    return False
                temp = float(unit_price_entry.get()) * \
                    float(quantity_entry.get())
                temp = str(Decimal(temp).quantize(Decimal('0.00')))
                total_price_entry.delete(0, 'end')
                total_price_entry.insert(0, temp)
                total_price_entry.config(state='disable')
                self.__auto_count_flag[1] = 0
                set_default_style()
            elif self.__auto_count_flag[1] == 1 and self.__auto_count_flag[2] == 1:
                if total_price_entry.get() == '' or unit_price_entry.get() == '':
                    return False
                if int(float(total_price_entry.get())) == 0 or int(float(unit_price_entry.get())) == 0:
                    return False
                temp = float(total_price_entry.get()) / \
                    float(unit_price_entry.get())
                temp = str(Decimal(temp).quantize(Decimal('0.00')))
                quantity_entry.delete(0, 'end')
                quantity_entry.insert(0, temp)
                quantity_entry.config(state='disable')
                self.__auto_count_flag[0] = 0
                set_default_style()

        def stock_insert_validate(id):
            if id == 'quantity':
                self.__auto_count_flag[0] = 0
                quantity_entry.config(bootstyle='default')
                if re.compile('^[0-9]+\.?[0-9]*$').match(quantity_entry.get()):
                    quantity_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                    self.__auto_count_flag[0] = 1
                    if self.__auto_count_flag[1] == 1 and self.__auto_count_flag[2] == 1:
                        self.__auto_count_flag[0] = 0
                else:
                    if quantity_entry.get() != '':
                        notice_label.config(
                            text='进货量格式错误', width=42, justify='center')
                        quantity_entry.config(bootstyle='danger')
                auto_ccount()
            if id == 'total':
                self.__auto_count_flag[1] = 0
                total_price_entry.config(bootstyle='default')
                if re.compile('^[0-9]+\.?[0-9]*$').match(total_price_entry.get()):
                    total_price_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                    self.__auto_count_flag[1] = 1
                    if self.__auto_count_flag[0] == 1 and self.__auto_count_flag[2] == 1:
                        self.__auto_count_flag[1] = 0
                else:
                    if total_price_entry.get() != '':
                        notice_label.config(
                            text='总进价格式错误', width=42, justify='center')
                        total_price_entry.config(bootstyle='danger')
                auto_ccount()
            if id == 'unit':
                self.__auto_count_flag[2] = 0
                unit_price_entry.config(bootstyle='default')
                if re.compile('^[0-9]+\.?[0-9]*$').match(unit_price_entry.get()):
                    unit_price_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                    self.__auto_count_flag[2] = 1
                    if self.__auto_count_flag[0] == 1 and self.__auto_count_flag[1] == 1:
                        self.__auto_count_flag[2] = 0
                else:
                    if unit_price_entry.get() != '':
                        notice_label.config(
                            text='单位定价格式错误', width=42, justify='center')
                        unit_price_entry.config(bootstyle='danger')
            if quantity_entry.get() == '':
                self.__auto_count_flag[0] = 0
            if total_price_entry.get() == '':
                self.__auto_count_flag[1] = 0
            if unit_price_entry.get() == '':
                self.__auto_count_flag[2] = 0
            auto_ccount()
            if id == 'sell':
                sell_price_entry.config(bootstyle='default')
                if re.compile('^[0-9]+\.?[0-9]*$').match(sell_price_entry.get()):
                    sell_price_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if sell_price_entry.get() != '':
                        notice_label.config(
                            text='预期售价格式错误', width=42, justify='center')
                        sell_price_entry.config(bootstyle='danger')
            if id == 'date':
                washed_date = datetime_wash()
                date_entry.config(bootstyle='default')
                if verify_datetime(washed_date):
                    date_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if date_entry.get() != '':
                        notice_label.config(
                            text='日期时间格式错误', width=42, justify='center')
                        date_entry.config(bootstyle='danger')
            if id == 'period':
                period_entry.config(bootstyle='default')
                if re.compile('^[0-9]+\.?[0-9]*$').match(period_entry.get()):
                    period_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if period_entry.get() != '':
                        notice_label.config(
                            text='保质时长格式错误', width=42, justify='center')
                        period_entry.config(bootstyle='danger')
            return True

        def insert_data_wash():
            washed_data = []
            washed_data.append(catagory_entry.get()+batch_combobox.get())
            washed_data.append(catagory_entry.get())
            washed_data.append(batch_combobox.get())
            washed_data.append(
                str(Decimal(total_price_entry.get()).quantize(Decimal('0.00'))))
            washed_data.append(
                str(Decimal(quantity_entry.get()).quantize(Decimal('0.00'))))
            washed_data.append(
                str(Decimal(sell_price_entry.get()).quantize(Decimal('0.00'))))
            washed_data.append(datetime_wash())
            time_row = [0.0, 0.0, 0.0, 0.0]
            if period_combobox.get() == period_unit[0]:
                time_row[0] = float(period_entry.get())
            if period_combobox.get() == period_unit[1]:
                time_row[1] = float(period_entry.get())
            if period_combobox.get() == period_unit[2]:
                time_row[1] = 7*float(period_entry.get())
            if period_combobox.get() == period_unit[3]:
                time_row[2] = float(period_entry.get())
            if period_combobox.get() == period_unit[4]:
                time_row[3] = float(period_entry.get())
            washed_data.append(time_row)
            if storage_combobox.get()!='':
                washed_data.append(storage_combobox.get())
            else:
                washed_data.append('未定义')
            return washed_data

        def apply_stock_insert():
            error_string = '发现错误！\n'
            if catagory_entry.get() == '':
                error_string += '商品种类不能为空！\n'
            if batch_combobox.get() == '':
                error_string += '批次不能为空！\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(quantity_entry.get()) == None:
                error_string += '总进货量格式错误！进货量应为一个大于零的数字，保存时将保留两位小数。\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(total_price_entry.get()) == None:
                error_string += '总进价格式错误！总进价应为一个大于零的数字，保存时将保存两位小数。\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(sell_price_entry.get()) == None:
                error_string += '预期售价格式错误！预期售价应为一个大于零的数字，保留时将保存两位小数。\n'
            if verify_datetime(datetime_wash()) == False:
                error_string += '错误的进货日期格式！进货日期格式应为形如2222-11-22 22:22:22且客观上存在的时间。\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(period_entry.get()) == None:
                error_string += '错误的保质时长格式！保质时长应为一个大于零的数字，保存时将保存两位小数。\n'
            if period_combobox.get == '':
                error_string += '未知错误！时长单位不应该为空！\n'
            if error_string != '发现错误！\n':
                error_show_window = ttk.Toplevel()
                pop_menu(error_show_window)
                error_show_window.resizable(0, 0)
                win_initialize(error_show_window, 600, 346, '错误列表')
                show_text = ttk.Text(error_show_window, width=600, height=346)
                show_text.grid()
                show_text.insert('end', error_string)
                show_text.config(state='disable')
            else:
                insert_data = insert_data_wash()
                stock_insert_result = self.db.stock_data_insert(insert_data)
                if stock_insert_result == True:
                    cancel_insert()
                    messagebox.showinfo(title='插入成功', message='插入成功')
                    self.data = self.data_load()
                    self.stock_table.reload(self.data)
                else:
                    messagebox.showerror(
                        parent=new_stock_win, title='插入失败', message='插入失败，原因：{}'.format(stock_insert_result))
            return True

        if self.insert_panel_exist == True:
            return False
        new_stock_win = ttk.Toplevel()
        pop_menu(new_stock_win)
        win_initialize(new_stock_win, 800, 462, '新建进货')
        new_stock_win.resizable(0, 0)
        self.insert_panel_exist = True
        new_stock_win.protocol("WM_DELETE_WINDOW", cancel_insert)
        batch_var = ttk.StringVar()
        period_unit_var = ttk.StringVar()
        period_unit = ['小时', '天', '周', '月', '年']

        catagory_label = ttk.Label(new_stock_win,       text='商品种类　　　　 :')
        catagory_entry = ttk.Entry(
            new_stock_win, width=20, validate='all', validatecommand=batch_check)
        ToolTip(catagory_entry, text='商品种类名，不能为空')
        batch_label = ttk.Label(new_stock_win,          text='商品批次　　　　 :')
        batch_combobox = ttk.Combobox(
            new_stock_win, width=2, textvariable=batch_var)
        ToolTip(batch_combobox, text='显示当前可用批次，仅当默认批次全部占用后可自定义批次')
        quantity_label = ttk.Label(new_stock_win,       text='总货量/斤　　　:')
        quantity_entry = ttk.Entry(new_stock_win, width=20, validate='all',
                                   validatecommand=lambda: stock_insert_validate('quantity'))
        ToolTip(quantity_entry, text='总进货量应为一个大于零的数字，在保存时将保存两位小数')
        total_price_label = ttk.Label(new_stock_win,    text='总进价/元　　　　:')
        total_price_entry = ttk.Entry(
            new_stock_win, width=20, validate='all', validatecommand=lambda: stock_insert_validate('total'))
        ToolTip(total_price_entry, text='总进价应为一个大于零的数字，在保存时将保存两位小数')
        unit_price_label = ttk.Label(new_stock_win,     text='单位进价(元/斤):')
        unit_price_entry = ttk.Entry(
            new_stock_win, width=20, validate='all', validatecommand=lambda: stock_insert_validate('unit'))
        ToolTip(unit_price_entry,
                text='''单位进价应为一个大于零的数字，在保存时将保存两位小数\n事实上单位进价并不会被保存,仅总进价和总进货量将被保存，若其中任一值未给出将自动计算生成''')
        sell_price_label = ttk.Label(new_stock_win,     text='预计售价　　　　 :')
        sell_price_entry = ttk.Entry(
            new_stock_win, width=20, validate='all', validatecommand=lambda: stock_insert_validate('sell'))
        ToolTip(sell_price_entry, text='计划售价应为一个大于零的数字，在保存时将保存两位小数')
        date_label = ttk.Label(new_stock_win,           text='进货日期　　　　 :')
        date_entry = ttk.Entry(new_stock_win, width=20, validate='all',
                               validatecommand=lambda: stock_insert_validate('date'))
        ToolTip(
            date_entry, text='''双击输入框打开时间选择框，日期时间应为形如2222-11-22 22:22:22且客观上可存在的日期''')
        period_label = ttk.Label(new_stock_win,         text='保质期　　　　　 :')
        period_entry = ttk.Entry(new_stock_win, width=20, validate='all',
                                 validatecommand=lambda: stock_insert_validate('period'))
        ToolTip(period_entry, text='此次应填入预期的保存日期，应为一个大于零的数字，在保存时将保存两位小数')
        period_combobox = ttk.Combobox(
            new_stock_win, width=2, textvariable=period_unit_var)
        ToolTip(period_combobox, text='请选择正确的计时单位')
        batch_combobox.config(state='readonly')
        period_combobox.config(values=tuple(period_unit), state='readonly')
        storage_label=ttk.Label(new_stock_win,text='存放位置　　　　 :')
        storage_combobox=ttk.Combobox(new_stock_win, width=20,values=self.db.storage_check())
        ToolTip(storage_combobox,text='非必填项，若空置将保存为未定义')
        iventory_label=ttk.Label(new_stock_win,text='当前货物记录数为:')
        iventory_entry=ttk.Entry(new_stock_win,width=20,bootstyle='info',justify='center')
        iventory_entry.insert(0,len(self.data))
        iventory_entry.config(state='readonly')



        apply_insert_button = ttk.Button(
            new_stock_win, text='      确认插入      ', command=apply_stock_insert, bootstyle='success')
        cancel_insert_button = ttk.Button(
            new_stock_win, text='取消插入', command=cancel_insert, bootstyle='danger')

        notice_label = ttk.Label(
            new_stock_win, text='', width=25, justify='center')

        new_stock_win.bind('<Motion>', lambda e: stock_insert_validate(0))
        batch_combobox.bind('<1>', lambda e: batch_check())
        date_entry.bind('<Double-1>', lambda e: date_insert())

        catagory_label.grid(column=0, row=0, padx=(30, 5),
                            pady=5, sticky=(E, W))
        catagory_entry.grid(column=1, row=0, columnspan=2,
                            padx=5, pady=5, sticky=(E, W))
        batch_label.grid(column=3, row=0, padx=5, pady=5, sticky=(E, W))
        batch_combobox.grid(column=4, row=0, columnspan=2,
                            padx=(5, 30), pady=5, sticky=(E, W))
        quantity_label.grid(column=0, row=1, padx=(30, 5),
                            pady=5, sticky=(E, W))
        quantity_entry.grid(column=1, row=1, columnspan=2,
                            padx=5, pady=5, sticky=(E, W))
        total_price_label.grid(column=3, row=1, padx=5, pady=5, sticky=(E, W))
        total_price_entry.grid(column=4, row=1, columnspan=2,
                               padx=(5, 30), pady=5, sticky=(E, W))
        unit_price_label.grid(column=0, row=2, padx=(
            30, 5), pady=5, sticky=(E, W))
        unit_price_entry.grid(column=1, row=2, columnspan=2,
                              padx=5, pady=5, sticky=(E, W))
        sell_price_label.grid(column=3, row=2, padx=5, pady=5, sticky=(E, W))
        sell_price_entry.grid(column=4, row=2, columnspan=2,
                              padx=(5, 30), pady=5, sticky=(E, W))
        date_label.grid(column=0, row=3, padx=(30, 5), pady=5, sticky=(E, W))
        date_entry.grid(column=1, row=3, columnspan=2,
                        padx=5, pady=5, sticky=(E, W))
        period_label.grid(column=3, row=3, padx=5, pady=5, sticky=(E, W))
        period_entry.grid(column=4, row=3, padx=(5, 0), pady=5, sticky=(E, W))
        period_combobox.grid(column=5, row=3, padx=(
            0, 30), pady=5, sticky=(E, W))
        storage_label.grid(column=0, row=4, padx=(30, 5), pady=5, sticky=(E, W))
        storage_combobox.grid(column=1, row=4, columnspan=2,
                        padx=5, pady=5, sticky=(E, W))
        iventory_label.grid(column=3, row=4, padx=5, pady=5, sticky=(E, W))
        iventory_entry.grid(column=4, row=4, columnspan=2,
                              padx=(5, 30), pady=5, sticky=(E, W))

        notice_label.grid(column=2, row=5, columnspan=4,
                          padx=5, pady=5, sticky=(W, S, N, E))
        apply_insert_button.grid(
            column=1, row=6, padx=5, pady=6, sticky=(E, W))
        cancel_insert_button.grid(
            column=4, row=6, padx=5, pady=6, sticky=(E, W))
        for i in range(5):
            new_stock_win.columnconfigure(i, weight=1)
        for i in range(7):
            new_stock_win.rowconfigure(i, weight=1)
        catagory_entry.focus_set()
        
    def report_loss(self):
        for row in self.data:
            temp_row=[]
            if float(row[-1])<0.0:
                temp_row.append(int(time.mktime(time.localtime())))
                temp_row.append(row[4])
                temp_row.append(row[3])
                temp_row.append(row[1])
                temp_row.append(row[2])
                temp_row.append(row[5])
                self.db.report_loss(temp_row)
        self.flush_data()
        messagebox.showinfo(title='注意',message='所有修改已应用')

    def data_load(self):
        self.data = []
        to_be_cleaned = []
        to_be_cleaned = self.db.data_load()
        for row in to_be_cleaned:
            temp = []
            for i in range(5):
                temp.append(row[i])
            temp.append(row[8])
            temp.append(row[5])
            temp.append(row[6])
            t = str(Decimal(float(row[7])/86400).quantize(Decimal('0.00')))
            temp.append(t)
            self.data.append(temp)
        self.data = sorted(self.data, key=(lambda x: float(x[-1])))
        return self.data

    def apply_stock_modify(self):
        def datetime_wash(signal=0):
            if signal == 0:
                return False
            unwashed_date = signal
            washed_date = ''
            for i in unwashed_date:
                if i == '：':
                    washed_date = washed_date+':'
                    continue
                washed_date = washed_date+i
            return washed_date

        data_rows = self.stock_table.deliver()
        error_list = []
        able_to_apply_row = []
        for row in data_rows:
            error_string = '发现错误！\n'
            if row[0] == '':
                error_string += '未知错误！识别码丢失！\n'
            if row[1] == '':
                error_string += '商品种类不能为空！\n'
            if row[2] == '':
                error_string += '批次不能为空！\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(row[3]) == None:
                error_string += '总进价格式错误！总进价应为一个大于零的大于零的数字，保存时将保存两位小数。\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(row[4]) == None:
                error_string += '总进货量格式错误！进货量应为一个大于零的大于零的数字，保存时将保留两位小数。\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(row[6]) == None:
                error_string += '预期售价格式错误！预期售价应为一个大于零的大于零的数字，保留时将保存两位小数。\n'
            if verify_datetime(datetime_wash(row[7])) == False:
                error_string += '错误的进货日期格式！进货日期格式应为形如2222-11-22 22:22:22且客观上存在的时间。\n'
            if re.compile('^[0-9]+\.?[0-9]*$').match(row[8]) == None:
                error_string += '错误的保质时长格式！保质时长应为一个大于零的大于零的数字，保存时将保存两位小数。\n'
            if error_string != '发现错误！\n':
                error_list.append(['识别码为'+row[0]+'的行发现错误：', error_string])
            else:
                able_to_apply_row.append(row)

        for row in able_to_apply_row:
            row[3] = str(Decimal(float(row[3])).quantize(Decimal('0.00')))
            row[4] = str(Decimal(float(row[4])).quantize(Decimal('0.00')))
            row[6] = str(Decimal(float(row[6])).quantize(Decimal('0.00')))
            time_row = [0.0, float(row[8]), 0.0, 0.0]
            row[8] = time_row
            t=row[5]
            del row[5]
            if t=='':
                row.append('未定义')
            else:    
                row.append(t)
        result = self.db.stock_date_update(able_to_apply_row)
        self.data = self.db.data_load()
        self.stock_table.reload(self.data)
        if error_list != [] or result != True:
            error_show_window = ttk.Toplevel()
            pop_menu(error_show_window)
            error_show_window.resizable(0, 0)
            win_initialize(error_show_window, 600, 346, '错误列表')
            show_text = ttk.Text(error_show_window, width=600, height=346)
            show_text.grid()
            if error_list != []:
                for row in error_list:
                    show_text.insert('end', row)
                    show_text.insert(tk.INSERT, '\n')
            if result != True:
                for row in result:
                    show_text.insert('end', row)
                    show_text.insert(tk.INSERT, '\n')
            show_text.insert('end', '其他行均修改成功！')
            show_text.config(state='disabled')
        if error_list == [] and result == True:
            messagebox.showinfo(title='修改成功', message='所有修改操作都成功了！')

    def apply_stock_delete(self):
        delete_list = self.stock_table.delete_passing()
        if delete_list == []:
            return False
        t = self.db.stock_data_delete(delete_list)
        if t != True:
            messagebox.showerror(
                title='删除值时发生错误', message='发生错误行的货物识别码及错误类型为:{}'.format(t))
        del t
        self.data = self.db.data_load()
        self.stock_table.reload(self.data)
        return True

    def appply_stock_all(self):
        self.apply_stock_modify()
        self.apply_stock_delete()
        self.data = self.data_load()
        self.stock_table.reload(self.data)

    def flush_data(self):
        self.data = self.data_load()
        self.stock_table.reload(self.data)
