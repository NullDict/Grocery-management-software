from stock_member_function import*


class history_frame_init:
    def __init__(self, parent: ttk.Frame) -> None:
        self.parent = parent
        self.purchase_history_data = []
        self.db = DB_history()
        self.notebook = ttk.Notebook(self.parent)
        self.sell_frame = ttk.Frame(self.notebook)
        self.purchase_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sell_frame, text='销售历史')
        self.notebook.add(self.purchase_frame, text='采购历史')
        self.sell_button = ttk.Button(
            self.parent, text='销售历史', command=self.select_sell, bootstyle='success-outline')
        self.purchase_button = ttk.Button(
            self.parent, text='采购历史', command=self.select_purchase, bootstyle='success-outline')
        self.sell_button.grid(column=0, row=0, sticky=(E, W, S, N))
        self.purchase_button.grid(column=1, row=0, sticky=(E, W, S, N))
        self.notebook.grid(column=0, row=1, columnspan=18,
                           rowspan=50, sticky=(E, W, S, N))
        for i in range(18):
            self.parent.columnconfigure(i, weight=1)
        for i in range(51):
            self.parent.rowconfigure(i, weight=1)
        self.sell_frame.columnconfigure(0, weight=1)
        self.sell_frame.rowconfigure(0, weight=1)
        self.purchase_frame.columnconfigure(0, weight=1)
        self.purchase_frame.rowconfigure(0, weight=1)
        self.purchase_table_deploy()
        self.sell_table_deploy()
        self.select_sell()
        #self.notebook.bind('<Enter>',lambda e:self.flush_data())

    def select_sell(self):
        self.sell_button.config(bootstyle='success')
        self.purchase_button.config(bootstyle='success-outline')
        self.notebook.select(self.sell_frame)

    def select_purchase(self):
        self.purchase_button.config(bootstyle='success')
        self.sell_button.config(bootstyle='success-outline')
        self.notebook.select(self.purchase_frame)
        self.purchase_history_table.reload(self.purchase_data_load())

    def sell_table_deploy(self):
        self.sell_history_data = self.sell_data_load()
        sell_history_table_id = ['id', 'turnover', 'volume',
                                 'cost', 'catagory', 'batch', 'storage', 'member']
        sell_history_table_name = ['成交日期', '交易额',
                                   '交易量', '成本价', '种类', '批次', '存储位置', '会员']
        self.sell_history_table = table_viewS(
            self.sell_frame, columnid=sell_history_table_id, showname=sell_history_table_name,
            data=self.sell_history_data, readonly=1, columnwidth=100)
        self.sell_history_table.grid(column=0, row=0, sticky=(E, W, S, N))
        self.sell_history_table.load()

    def purchase_table_deploy(self):
        self.purchase_history_data = self.purchase_data_load()
        purchase_history_table_id = [
            'id', 'catagory', 'batch', 'price', 'quantity', 'selling_price', 'expire', 'storage']
        purchase_history_table_showname = [
            '标识号', '种类', '批次', '总进价', '总进货量', '预期售价', '到期日期', '存放位置']
        self.purchase_history_table = table_viewS(
            self.purchase_frame, columnid=purchase_history_table_id, showname=purchase_history_table_showname,
            data=self.purchase_history_data, readonly=1, columnwidth=100)
        self.purchase_history_table.grid(column=0, row=0, sticky=(E, W, S, N))
        self.purchase_history_table.load()

    def purchase_data_load(self):
        raw_data = []
        raw_data = self.db.purchase_data_load()
        if len(raw_data) == 0:
            return [[]]
        for row in raw_data:
            row.append(time.mktime(time.strptime(
                (row[0][-19:-1]+row[0][-1]), "%Y-%m-%d %H:%M:%S")))
        raw_data = sorted(raw_data, key=(lambda x: float(x[-1])))
        raw_data.reverse()
        for row in raw_data:
            del row[-1]
        self.purchase_history_data = raw_data
        return raw_data

    def sell_data_load(self):
        raw_data = []
        raw_data = self.db.sell_data_load()
        if len(raw_data) == 0:
            return[[]]
        for row in raw_data:
            row[0] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row[0]))
        self.sell_history_data = raw_data
        return raw_data

    def flush_data(self):
        self.purchase_history_table.reload(self.purchase_data_load())
        self.sell_history_table.reload(self.sell_data_load())

class order_frame_init:
    def __init__(self, parent: ttk.Frame) -> None:
        self.parent = parent
        self.order_data_array = []
        self.db = DB_order()
        self.insert_panel_exist = False
        order_column_id = ['id', 'customer', 'number', 'catagory',
                           'quantity', 'booking_date', 'remarks', 'state']
        order_showname = ['订单号', '客户', '客户电话',
                          '订购种类', '订购数/(斤)', '订购日期', '备注', '订单状态']
        self.order_data_array = self.order_data_load()
        self.order_table = table_viewS(
            self.parent, columnid=order_column_id, showname=order_showname, data=self.order_data_array, columnwidth=100)
        self.order_table.load()
        self.new_order_button = ttk.Button(
            self.parent, text='新建订单', command=self.new_order, bootstyle='success')
        self.handle_order_menubutton=ttk.Menubutton(self.parent, text='处理订单',)
        # self.finish_order_button = ttk.Button(
        #     self.parent, text='处理订单', command=self.modify_order_state)
        self.apply_order_modify_button = ttk.Button(
            self.parent, text='应用修改', command=self.apply_all, bootstyle='info')

        self.order_table.grid(column=0, row=0, columnspan=5,
                              rowspan=5, sticky=(E, W, S, N))
        self.new_order_button.grid(
            column=1, row=5, padx=5, pady=5, sticky=(W, S, N, E))
        self.handle_order_menubutton.grid(
            column=2, row=5, padx=5, pady=5, sticky=(W, S, N, E))
        self.apply_order_modify_button.grid(
            column=3, row=5, padx=5, pady=5, sticky=(W, S, N, E))
        for i in range(5):
            self.parent.columnconfigure(i, weight=1)
            self.parent.rowconfigure(i, weight=2)
        self.parent.rowconfigure(5, weight=1)

        def handle_expired(mode):
            if mode != 5:
                t = self.db.expired_order_state_update(mode)
                if t == True:
                    messagebox.showinfo(title='修改成功', message='修改成功')
                    self.order_table.reload(self.order_data_load())
                else:
                    messagebox.showerror(
                        title='修改失败', message='数据库错误，类型为：{}'.format(t))
                    self.order_table.reload(self.order_data_load())
            else:
                t = self.db.order_expired_delete()
                if t == True:
                    messagebox.showinfo(title='修改成功', message='修改成功!')
                    self.order_table.reload(self.order_data_load())
                else:
                    messagebox.showerror(
                        title='修改失败', message='数据库错误，类型为：{}'.format(t))

                    self.order_table.reload(self.order_data_load())

        def handle_selected(mode):
            selected_array = self.order_table.selected_value()
            key_array = []
            for row in selected_array:
                key_array.append(row[0])
            r = self.db.order_state_update(key_array, mode)
            if r == True:

                messagebox.showinfo(title='修改成功', message='修改成功!')
                self.order_table.reload(self.order_data_load())
            else:
                messagebox.showerror(
                    title='修改失败', message='数据库错误，错误行及类型为：{}'.format(r))
                self.order_table.reload(self.order_data_load())
        handle_order_menu=ttk.Menu(self.parent,tearoff=False)
        self.handle_order_menubutton.config(menu=handle_order_menu)
        handle_order_menu.add_command(label='将所有标记订单标记为完成',command=lambda: handle_selected(0))
        handle_order_menu.add_separator()
        handle_order_menu.add_command(label='将所有标记订单标记为取消',command=lambda:handle_selected(-1))
        handle_order_menu.add_separator()
        handle_order_menu.add_command(label='将所有已过期订单标记为取消',command=lambda: handle_expired(-1))
        handle_order_menu.add_separator()
        handle_order_menu.add_command(label='将所有已过期订单从记录中删除',command=lambda: handle_expired(5))
        handle_order_menu.add_separator()
        handle_order_menu.add_command(label='将所有已过期订单标记为完成',command=lambda: handle_expired(0))

    def order_data_load(self):
        raw_data = []
        raw_data = self.db.order_data_load()
        if len(raw_data) == 0:
            return [[]]
        for row in raw_data:
            if row[-1] == 1:
                row[-1] = '未处理'
            if row[-1] == 0:
                row[-1] = '完成'
            if row[-1] == -1:
                row[-1] = '取消'
        self.order_data_array = raw_data
        return raw_data

    def new_order(self):
        def cancel_insert():
            new_order_win.destroy()
            self.insert_panel_exist = False

        def combobox_init():
            customer_combobox.config(values=self.db.check_member())
            number_combobox.config(values=self.db.check_number())
            catagrory_combobox.config(values=self.db.check_catagory())

        def datetime_wash(signal=0):
            if signal == 0:
                unwashed_date = ordered_date_entry.get()
            else:
                unwashed_date = signal
            washed_date = ''
            for i in unwashed_date:
                if i == '：':
                    washed_date = washed_date+':'
                    continue
                washed_date = washed_date+i
            return washed_date

        def date_insert():
            t = str(Querybox.get_date(ordered_date_label))+' ' + \
                time.strftime("%H:%M:%S", time.localtime())
            ordered_date_entry.delete(0, 'end')
            # try:
            ordered_date_entry.insert('end', t)

        def auto_match(mode):
            if mode == 'member':
                match_result = self.db.auto_matching(
                    mode, customer_combobox.get())
                if len(match_result) == 1:
                    number_combobox.delete(0, 'end')
                    number_combobox.insert('end', match_result[0])
            elif mode == 'number':
                match_result = self.db.auto_matching(
                    mode, number_combobox.get())
                if len(match_result) == 1:
                    customer_combobox.delete(0, 'end')
                    customer_combobox.insert('end', match_result[0])

        def validate_order(id):
            if id == 'customer':
                raw_customer_list = self.db.check_member()
                washed_customer_list = []
                for item in raw_customer_list:
                    if customer_combobox.get() in item:
                        washed_customer_list.append(item)
                customer_combobox.config(values=washed_customer_list)
                if customer_combobox.get() == '':
                    customer_combobox.config(values=raw_customer_list)
            if id == "number":
                raw_number_list = self.db.check_number()
                washed_number_list = []
                for item in raw_number_list:
                    if number_combobox.get() in item:
                        washed_number_list.append(item)
                number_combobox.config(values=washed_number_list)
                if number_combobox.get() == '':
                    number_combobox.config(values=raw_number_list)
            if id == "quantity":
                quantity_entry.config(bootstyle='default')
                if re.compile('^[0-9]+\.?[0-9]*$').match(quantity_entry.get()):
                    quantity_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if quantity_entry.get() != '':
                        notice_label.config(
                            text='预定量格式错误', width=42, justify='center')
                        quantity_entry.config(bootstyle='danger')
            if id == 'date':
                washed_date = datetime_wash()
                ordered_date_entry.config(bootstyle='default')
                if verify_datetime(washed_date):
                    ordered_date_entry.config(bootstyle='default')
                    notice_label.config(
                        text='', width=42, justify='center')
                else:
                    if ordered_date_entry.get() != '':
                        notice_label.config(
                            text='日期时间格式错误', width=42, justify='center')
                        ordered_date_entry.config(bootstyle='danger')
            return True

        def apply_insert_order():
            _insert_row = []
            _insert_row.append(str(hex(int(time.mktime(time.localtime())))))
            _insert_row.append(customer_combobox.get())
            _insert_row.append(number_combobox.get())
            _insert_row.append(catagrory_combobox.get())
            _insert_row.append(quantity_entry.get())
            _insert_row.append(ordered_date_entry.get())
            _insert_row.append(remarks_entry.get())
            _insert_check = self.data_examine(_insert_row)
            if len(_insert_check[0]) == 0:
                error_show_window = ttk.Toplevel()
                pop_menu(error_show_window)
                error_show_window.resizable(0, 0)
                win_initialize(error_show_window, 600, 346, '错误列表')
                show_text = ttk.Text(error_show_window, width=600, height=346)
                show_text.grid()
                show_text.insert('end', _insert_check[1])
                show_text.insert('end', '存在错误，插入失败！')
                show_text.config(state='disabled')
            if len(_insert_check[0]) != 0 and len(_insert_check[1]) != 0:
                _insert_check[0].append(1)
                t = self.db.order_data_insert(_insert_check[0])
                error_show_window = ttk.Toplevel()
                pop_menu(error_show_window)
                error_show_window.resizable(0, 0)
                win_initialize(error_show_window, 600, 346, '警告列表')
                show_text = ttk.Text(error_show_window, width=600, height=346)
                show_text.grid()
                show_text.insert('end', _insert_check[1])
                if t != True:
                    show_text.insert('end', t)
                    show_text.insert('end', '插入失败，数据库发现错误！')
                    show_text.config(state='disabled')
                    return False
                show_text.insert('end', '插入成功，但存在隐患！')
                show_text.config(state='disabled')
                cancel_insert()
                self.order_table.reload(self.order_data_load())
            if len(_insert_check[0]) != 0 and len(_insert_check[1]) == 0:
                _insert_check[0].append(1)
                t = self.db.order_data_insert(_insert_check[0])
                if t == True:
                    messagebox.showinfo(title='插入成功', message='插入成功！')
                    cancel_insert()
                    self.order_table.reload(self.order_data_load())
                else:
                    messagebox.showerror(
                        parent=new_order_win, title='插入失败', message='数据库错误！，类型为：{}'.format(t))

        if self.insert_panel_exist == True:
            return False
        new_order_win = ttk.Toplevel()
        pop_menu(new_order_win)
        win_initialize(new_order_win, 800, 462, '新建订单')
        new_order_win.resizable(0, 0)
        self.insert_panel_exist = True
        new_order_win.protocol("WM_DELETE_WINDOW", cancel_insert)

        customer_label = ttk.Label(new_order_win, text='顾客姓名  :')
        customer_combobox = ttk.Combobox(
            new_order_win, width=20, validate='all', validatecommand=lambda: validate_order('customer'))
        number_label = ttk.Label(new_order_win, text='顾客电话  ：')
        number_combobox = ttk.Combobox(
            new_order_win, width=20, validate='all', validatecommand=lambda: validate_order('number'))
        catagrory_label = ttk.Label(new_order_win, text='商品种类')
        catagrory_combobox = ttk.Combobox(new_order_win, width=20)
        quantity_label = ttk.Label(new_order_win, text='订购量/斤：')
        quantity_entry = ttk.Entry(
            new_order_win, width=20, validate='all', validatecommand=lambda: validate_order('quantity'))
        ordered_date_label = ttk.Label(new_order_win, text='预订时间：')
        ordered_date_entry = ttk.Entry(
            new_order_win, width=20, validate='all', validatecommand=lambda: validate_order('date'))
        remarks_label = ttk.Label(new_order_win, text='备注      :')
        remarks_entry = ttk.Entry(new_order_win, width=20)
        notice_label = ttk.Label(
            new_order_win, text='', width=42, justify='center')

        apply_order_insert_button = ttk.Button(
            new_order_win, text='确认插入', command=apply_insert_order, bootstyle='success')
        cancel_insert_button = ttk.Button(
            new_order_win, text='取消插入', bootstyle='danger')
        combobox_init()
        ordered_date_entry.bind('<Double-1>', lambda e: date_insert())
        customer_combobox.bind('<<ComboboxSelected>>',
                               lambda e: auto_match('member'))
        number_combobox.bind('<<ComboboxSelected>>',
                             lambda e: auto_match('number'))

        customer_label.grid(column=0, row=0, padx=(30, 5),
                            pady=5, sticky=(E, W))
        customer_combobox.grid(column=1, row=0, columnspan=2,
                               padx=5, pady=5, sticky=(E, W))
        number_label.grid(column=3, row=0, padx=5, pady=5, sticky=(E, W))
        number_combobox.grid(column=4, row=0, columnspan=2,
                             padx=(5, 30), pady=5, sticky=(E, W))
        catagrory_label.grid(column=0, row=1, padx=(30, 5),
                             pady=5, sticky=(E, W))
        catagrory_combobox.grid(column=1, row=1, columnspan=2,
                                padx=5, pady=5, sticky=(E, W))
        quantity_label.grid(column=3, row=1, padx=5, pady=5, sticky=(E, W))
        quantity_entry.grid(column=4, row=1, columnspan=2,
                            padx=(5, 30), pady=5, sticky=(E, W))
        ordered_date_label.grid(column=0, row=2, padx=(
            30, 5), pady=5, sticky=(E, W))
        ordered_date_entry.grid(column=1, row=2, columnspan=2,
                                padx=5, pady=5, sticky=(E, W))
        remarks_label.grid(column=3, row=2, padx=5, pady=5, sticky=(E, W))
        remarks_entry.grid(column=4, row=2, columnspan=2,
                           padx=(5, 30), pady=5, sticky=(E, W))
        notice_label.grid(column=2, row=3, columnspan=4,
                          padx=5, pady=5, sticky=(W, S, N, E))
        apply_order_insert_button.grid(
            column=1, row=4, padx=5, pady=6, sticky=(E, W))
        cancel_insert_button.grid(
            column=4, row=4, padx=(5, 100), pady=6, sticky=(E, W))
        for i in range(5):
            new_order_win.columnconfigure(i, weight=2)
            new_order_win.rowconfigure(i, weight=1)
        new_order_win.columnconfigure(1, weight=1)
        new_order_win.columnconfigure(2, weight=1)

    def apply_delete(self):
        delete_array = self.order_table.delete_passing()
        t = self.db.order_data_delete(delete_array)
        if t != True:
            messagebox.showerror(
                title='删除时发生错误', message='发生错误的行及错误类型为'.format(t))
        self.order_table.reload(self.order_data_load())

    def data_examine(self, data_row):
        error_string = '警告！\n'
        if data_row[1] == '':
            error_string += '尽管客户名称不是必须的，但不建议空置!\n'
        if data_row[2] == '':
            error_string += '尽管客户电话不是必须的，但不建议空置!\n'
        if data_row[3] == '':
            error_string += '错误！商品种类不能为空'
        if re.compile('^[0-9]+\.?[0-9]*$').match(data_row[4]) == None:
            error_string += '错误！错误的订购量格式，订购量应为一个数字，在保存时将保\n存两位小数!\n'
        else:
            data_row[4] = str(Decimal(data_row[4]).quantize(Decimal('0.00')))
        washed_date = ''
        for i in data_row[5]:
            if i == '：':
                washed_date += ':'
                continue
            washed_date += i
        data_row[5] = washed_date
        if verify_datetime(washed_date) == False:
            error_string += '错误！错误的时间格式，时间格式应为形如2222-11-22 22:22:22，且客观上可存在的时\n间!\n'
        if data_row[6] == '':
            data_row[6] = '   '
        try:
            if data_row[7] == '未处理':
                data_row[7] = 1
            elif data_row[-1] == '完成':
                data_row[7] = 0
            elif data_row[-1] == '取消':
                data_row[7] = -1
            else:
                error_string += '错误的订单状态！正确的订单状态应为“未处理”、“完成”，“取消”其中的一种\n'
        except:
            pass
        if error_string == '警告！\n':
            return [data_row, []]
        if '错误' not in error_string:
            return [data_row, error_string]
        if '错误' in error_string:
            return [[], '\n订单号'+data_row[0]+'检查发现问题：'+error_string+'该行插入失败']

    def apply_modify(self):
        raw_modified_data = self.order_table.deliver()
        error_array = []
        for row in raw_modified_data:
            row = self.data_examine(row)
            r = True
            if len(row[0]) != 0:
                r = self.db.order_data_update(row[0])
            if len(row[1]) != 0 or r != True:
                try:
                    error_row = ['订单号'+row[0][0], ':检查发现问题:'+row[1]]
                except:
                    error_row = [row[1]]
                if r != True:
                    error_row.append('数据库发现问题'+r+'插入失败')
                else:
                    if '错误' not in row[1]:
                        error_row.append('插入成功')
                error_array.append(error_row)
        if len(error_array) != 0:
            error_show_window = ttk.Toplevel()
            pop_menu(error_show_window)
            error_show_window.resizable(0, 0)
            win_initialize(error_show_window, 600, 346, '错误列表')
            show_text = ttk.Text(error_show_window, width=600, height=346)
            show_text.grid()
            for row in error_array:
                show_text.insert('end', row)
            show_text.insert('end', '\n其他行插入成功！')
            show_text.config(state='disabled')
        else:
            messagebox.showinfo(title='修改成功', message='修改成功！')
        self.order_table.reload(self.order_data_load())

    def apply_all(self):
        self.apply_modify()
        self.apply_delete()

    def flush_data(self):
        self.order_table.reload(self.order_data_load())
