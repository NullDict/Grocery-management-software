from order_history_functions import *

class checkout_frame_init:
    def __init__(self, parent: ttk.Frame) -> None:
        self.parent = parent
        self.catagory_array = []
        self.order_array = []
        self.db = DB_checkout()
        self.catagory_array = self.db.get_available_catagory()
        self.catagory_array.reverse()
        self.order_array = self.db.order_data_load()
        self.insert_panel_exist = False
        self.catagory_dict = {}
        self.catagory_button_dict = {}
        self.member_list = self.db.member_load()
        self.pagination = 0
        self.current = False
        self.current_catagory_row = False
        self.count_rate = False
        self.current_member = False
        self.wallet_pay = ttk.IntVar(value=0)
        self.shopcart_list = []
        self.shopcart_dict = {}
        self.current_order = [False, False]
        # 商品名单框架
        self.infomation_frame = ttk.Frame(self.parent, relief=SUNKEN)
        self.catagory_frame = ttk.Frame(
            self.parent, relief=RAISED, bootstyle='secondary')
        self.former_button = ttk.Button(
            self.parent, text='<<上一页', command=lambda: self.page_turn(0), bootstyle='info')
        self.next_button = ttk.Button(
            self.parent, text='下一页>>', command=lambda: self.page_turn(1), bootstyle='info')
        if len(self.catagory_array) <= 25:
            self.former_button.config(state='readonly')
            self.next_button.config(state='readonly')
        self.order_button = ttk.Button(
            self.parent, text='从订单导入', command=self.order_panel)

        self.infomation_frame.grid(
            column=0, row=0, columnspan=4, rowspan=25, padx=(0, 1), sticky=(W, S, E, N))
        self.catagory_frame.grid(
            column=4, row=0, columnspan=3, rowspan=24, padx=(1, 0), sticky=(W, S, E, N))
        self.order_button.grid(column=6, row=25, pady=5, sticky=(W, S, E, N))

        for index, item in enumerate(self.catagory_array):
            self.catagory_dict[index] = item
            self.catagory_button_dict[index] = ttk.Button(
                self.catagory_frame, text=self.catagory_dict[index],
                command=lambda arg=index: self.button_matching(arg))
        self.former_button.grid(
            column=4, row=24, padx=(0, 1), sticky=(W, S, E, N))
        ttk.Button(self.parent, text='❓', bootstyle='secondary').grid(
            column=5, row=24, padx=(1, 1), sticky=(W, S, E, N))
        self.next_button.grid(
            column=6, row=24, padx=(1, 0), sticky=(W, S, E, N))

        for i in range(7):
            self.parent.columnconfigure(i, weight=1)
        for i in range(26):
            self.parent.rowconfigure(i, weight=1)

        for i in range(self.pagination*25, (self.pagination+1)*25):
            if i == len(self.catagory_array):
                break
            self.catagory_button_dict[i].grid(
                column=i % 5, row=i//5, padx=1, pady=1, sticky=(W, S, E, N))

        for i in range(5):
            self.catagory_frame.columnconfigure(i, weight=1)
            self.catagory_frame.rowconfigure(i, weight=1)

        # 交易信息框架
        self.catagory_label = ttk.Label(self.infomation_frame, text='商品种类:')
        self.catagory_combobox = ttk.Combobox(
            self.infomation_frame, width=20, values=self.catagory_array, validate='all',
            validatecommand=lambda: self.check_out_validate('catagory'))
        self.batch_label = ttk.label = ttk.Label(
            self.infomation_frame, text='商品批次:')
        self.batch_combobox = ttk.Combobox(self.infomation_frame, width=20, validate='all',
                                           validatecommand=lambda: self.check_out_validate('batch'))
        self.quantity_label = ttk.Label(self.infomation_frame, text='数量/斤:')
        self.quantity_entry = ttk.Entry(self.infomation_frame, width=20, validate='all',
                                        validatecommand=lambda: self.check_out_validate('quantity'))
        self.price_label = ttk.Label(self.infomation_frame, text='价格／元:')
        self.price_entry = ttk.Entry(self.infomation_frame, width=20, validate='all',
                                     validatecommand=lambda: self.check_out_validate('price'))
        self.auto_sum_button = ttk.Button(
            self.infomation_frame, text='计算', command=self.auto_sum)
        self.cost_label = ttk.Label(self.infomation_frame, text='商品成本:')
        self.cost_entry = ttk.Entry(self.infomation_frame, width=20, validate='all',
                                    validatecommand=lambda: self.check_out_validate('cost'))
        self.member_name_label = ttk.Label(self.infomation_frame, text='会员姓名:')
        self.member_name_combobox = ttk.Combobox(self.infomation_frame, width=20, validate='focusout',
                                                 validatecommand=lambda: self.check_out_validate('member'))
        self.number_label = ttk.Label(self.infomation_frame, text='客户电话:')
        self.number_combobox = ttk.Combobox(self.infomation_frame, width=20, validate='focusout',
                                            validatecommand=lambda: self.check_out_validate('number'))
        self.wallet_label = ttk.Label(self.infomation_frame, text='客户余额:')
        self.wallet_entry = ttk.Entry(self.infomation_frame, width=20)
        self.notice_entry = ttk.Entry(self.infomation_frame, justify=CENTER)

        self.add_button = ttk.Button(
            self.infomation_frame, text='添加到购物车', command=self.add_to_shop_cart, bootstyle='success')
        self.shopcart_menu = ttk.Menu(self.infomation_frame, tearoff=False)
        self.shopcart_menubutton = ttk.Menubutton(
            self.infomation_frame, text='当前购物车', bootstyle='info', menu=self.shopcart_menu)
        self.apply_button = ttk.Button(
            self.infomation_frame, text='结算', command=self.final_checkout, bootstyle='danger')
        self.wallet_entry.config(state='readonly')
        self.notice_entry.config(state='readonly')

        self.wallet_pay_checkbutton = ttk.Checkbutton(
            self.infomation_frame, text='使用会员钱包结算', variable=self.wallet_pay, offvalue=0, onvalue=1, bootstyle="warning-round-toggle")

        self.catagory_label.grid(
            column=0, row=0, padx=(30, 5), pady=5, sticky=(E, W))
        self.catagory_combobox.grid(
            column=1, row=0, columnspan=2, padx=5, pady=5, sticky=(E, W))
        self.batch_label.grid(column=3, row=0, padx=5, pady=5, sticky=(E, W))
        self.batch_combobox.grid(
            column=4, row=0, columnspan=2, padx=(5, 30), pady=5, sticky=(E, W))
        self.quantity_label.grid(
            column=0, row=1, padx=(30, 5), pady=5, sticky=(E, W))
        self.quantity_entry.grid(
            column=1, row=1, columnspan=2, padx=5, pady=5, sticky=(E, W))
        self.price_label.grid(column=3, row=1, padx=5, pady=5, sticky=(E, W))
        self.price_entry.grid(column=4, row=1, padx=(
            5, 0), pady=5, sticky=(E, W))
        self.auto_sum_button.grid(
            column=5, row=1, padx=(0, 30), pady=5, sticky=(E, W))
        self.cost_label.grid(column=0, row=2, padx=(
            30, 5), pady=5, sticky=(E, W))
        self.cost_entry.grid(column=1, row=2, columnspan=2,
                             padx=5, pady=5, sticky=(E, W))
        self.member_name_label.grid(
            column=3, row=2, padx=5, pady=5, sticky=(E, W))
        self.member_name_combobox.grid(
            column=4, row=2, columnspan=2, padx=(5, 30), pady=5, sticky=(E, W))
        self.number_label.grid(column=0, row=3, padx=(
            30, 5), pady=5, sticky=(E, W))
        self.number_combobox.grid(
            column=1, row=3, columnspan=2, padx=5, pady=5, sticky=(E, W))
        self.wallet_label.grid(column=3, row=3, padx=5, pady=5, sticky=(E, W))
        self.wallet_entry.grid(column=4, row=3, padx=(
            5, 30), pady=5, sticky=(E, W))
        self.wallet_pay_checkbutton.grid(
            column=5, row=3, padx=(5, 30), pady=5, sticky=(E, W))
        self.notice_entry.grid(column=0, row=4, columnspan=6, padx=(
            20, 20), pady=5, sticky=(E, W))
        self.add_button.grid(column=1, row=5, padx=5, pady=5, sticky=(E, W))
        self.shopcart_menubutton.grid(
            column=2, row=5, columnspan=2, padx=5, pady=5, sticky=(S, N))
        self.apply_button.grid(column=4, row=5, padx=5, pady=5, sticky=(E, W))
        for i in range(6):
            self.infomation_frame.columnconfigure(i, weight=1)
            self.infomation_frame.rowconfigure(i, weight=1)

        self.catagory_combobox.bind('<<ComboboxSelected>>',
                                    lambda e: self.catagory_combobox_matching())
        self.catagory_combobox.bind(
            '<FocusOut>', lambda e: self.catagory_combobox_matching())
        self.batch_combobox.bind('<<ComboboxSelected>>',
                                 lambda e: self.batch_combobox_matching())
        self.member_name_combobox.bind('<<ComboboxSelected>>',
                                       lambda e: self.member_matching('member'))
        self.number_combobox.bind('<<ComboboxSelected>>',
                                  lambda e: self.member_matching('number'))
        self.member_name_combobox.bind(
            '<1>', lambda e: self.check_out_validate('member'))
        self.number_combobox.bind(
            '<1>', lambda e: self.check_out_validate('number'))

        self.member_name_combobox.bind(
            '<BackSpace>', lambda e: self.member_entry_clear('member'))
        self.number_combobox.bind(
            '<BackSpace>', lambda e: self.member_entry_clear('number'))

        self.catagory_combobox.bind(
            '<1>', lambda e: self.check_out_validate('catagory'))

    def order_panel(self):
        self.order_array = self.db.order_data_load()

        def cancel_insert():
            order_panel.destroy()
            self.insert_panel_exist = False

        def from_order_insert():
            if order_table.selected_value() == []:
                return False
            for row in order_table.selected_value():
                self.catagory_combobox.delete(0, 'end')
                self.catagory_combobox.insert('end', row[3])
                self.catagory_combobox_matching()
                self.quantity_entry.delete(0, 'end')
                self.quantity_entry.insert('end', row[4])
                self.auto_sum()
                self.number_combobox.delete(0, 'end')
                self.number_combobox.insert('end', row[2])
                self.member_matching('number')
                self.current_order = [row[0], row[2]]
                if float(self.quantity_entry.get()) < float(row[4])-0.0001:
                    messagebox.showwarning(
                        title='警告', message='该批次货物数量无法满足订单要求，请自行处理批次组合.')
                    self.price_entry.delete(0,'end')
            cancel_insert()
        if self.insert_panel_exist == True:
            return False

        order_panel = ttk.Toplevel()
        pop_menu(order_panel)
        self.insert_panel_exist = True
        win_initialize(order_panel, 800, 462, '订单！')
        order_panel.resizable(0, 0)
        order_panel.protocol("WM_DELETE_WINDOW", cancel_insert)
        order_column_id = ['id', 'customer', 'number', 'catagory',
                           'quantity', 'booking_date', 'remarks']
        order_showname = ['订单号', '客户', '客户电话',
                          '订购种类', '订购数/(斤)', '订购日期', '备注']
        order_table = table_viewS(
            order_panel, columnid=order_column_id, showname=order_showname, data=self.order_array, readonly=1, columnwidth=100)
        order_table.reload()
        order_table.grid(column=0, row=0, sticky=(E, W, S, N))
        order_panel.columnconfigure(0, weight=1)
        order_panel.rowconfigure(0, weight=1)
        order_panel.bind('<Double-1>', lambda e: from_order_insert())

    def catagory_combobox_matching(self, catagory=False, batch=False):
        self.button_point = False
        for i in self.catagory_button_dict:
            self.catagory_button_dict[i].config(bootstyle='default')
        self.current = (self.db.catagory_batch_matching(
            self.catagory_combobox.get()))
        batch_list = []
        for row in self.current:
            batch_list.append(row[2])
        self.batch_combobox.config(values=batch_list)
        self.check_out_validate('catagory')
        try:
            self.batch_combobox.current(0)
        except:
            pass
        self.batch_combobox_matching()

    def auto_sum(self):
        if self.count_rate != False and re.compile('^[0-9]+\.?[0-9]*$').match(self.quantity_entry.get()) != None:
            self.price_entry.delete(0, 'end')
            self.price_entry.insert('end', str(
                format(float(self.count_rate)*float(self.quantity_entry.get()), '.2f')))
            self.check_out_validate('all')

    def batch_combobox_matching(self):
        if self.current == []:
            self.count_rate = False
            self.current_catagory_row = False
            self.price_entry.delete(0, 'end')
            self.quantity_entry.delete(0, 'end')
            self.cost_entry.delete(0, 'end')
            return False
        for row in self.current:
            if row[2] == self.batch_combobox.get():
                self.count_rate = row[5]
                self.current_catagory_row = row
                break
            else:
                self.count_rate = False
                self.current_catagory_row = False
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.cost_entry.delete(0, 'end')
        return True

    def button_matching(self, index):
        self.button_point = index
        for i in self.catagory_button_dict:
            self.catagory_button_dict[i].config(bootstyle='default')
        self.catagory_button_dict[index].config(bootstyle='success')
        self.current = (self.db.catagory_batch_matching(
            self.catagory_dict[self.button_point]))
        batch_list = []
        for row in self.current:
            batch_list.append(row[2])
        self.catagory_combobox.delete(0, 'end')
        self.catagory_combobox.insert(
            'end', self.catagory_dict[self.button_point])
        self.batch_combobox.config(values=batch_list)
        self.batch_combobox.current(0)
        self.check_out_validate('catagory')
        self.catagory_combobox_matching()

    def member_matching(self, mode):
        if mode == 'number':
            for row in self.member_list:
                if self.number_combobox.get() == row[0]:
                    self.current_member = row
                    self.member_name_combobox.delete(0, 'end')
                    self.member_name_combobox.insert('end', row[1])
                    self.wallet_entry.config(state='normal')
                    self.wallet_entry.delete(0, 'end')
                    self.wallet_entry.insert('end', row[2])
                    self.wallet_entry.config(state='disable')
                    break
                else:
                    self.current_member = False
                    self.wallet_entry.config(state='normal')
                    self.wallet_entry.delete(0, 'end')
                    self.wallet_entry.config(state='disable')
        elif mode == 'member':
            for row in self.member_list:
                if self.member_name_combobox.get() == row[1]:
                    self.current_member = row
                    self.number_combobox.delete(0, 'end')
                    self.number_combobox.insert('end', row[0])
                    self.wallet_entry.config(state='normal')
                    self.wallet_entry.delete(0, 'end')
                    self.wallet_entry.insert('end', row[2])
                    self.wallet_entry.config(state='disable')
                    break
                else:
                    self.current_member = False
                    self.wallet_entry.config(state='normal')
                    self.wallet_entry.delete(0, 'end')
                    self.wallet_entry.config(state='disable')

    def page_turn(self, mode):
        self.catagory_array = self.db.get_available_catagory()
        self.catagory_array.reverse()
        self.order_array = self.db.order_data_load()
        if len(self.catagory_array) >= 25:
            self.former_button.config(state='normal')
            self.next_button.config(state='normal')
        for widget in self.catagory_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()
        for index, item in enumerate(self.catagory_array):
            self.catagory_dict[index] = item
            self.catagory_button_dict[index] = ttk.Button(
                self.catagory_frame, text=self.catagory_dict[index],
                command=lambda arg=index: self.button_matching(arg))
        if mode == 0 and self.pagination-1 >= 0:
            self.pagination -= 1
        elif mode == 1 and self.pagination+1 <= len(self.catagory_array)//25:
            self.pagination += 1
        for i in range(self.pagination*25, (self.pagination+1)*25):
            if i >= len(self.catagory_array):
                ttk.Button(self.catagory_frame, text='    ', bootstyle='secondary').grid(
                    column=i % 5, row=(i % 25)//5, padx=1, pady=1, sticky=(W, S, E, N))
            else:
                self.catagory_button_dict[i].grid(
                    column=i % 5, row=(i % 25)//5, padx=1, pady=1, sticky=(W, S, E, N))
        for widget in self.catagory_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(width=1)
        self.catagory_combobox.config(values=self.catagory_array)
        self.member_list = self.db.member_load()
        member_list = []
        for row in self.member_list:
            member_list.append(row[1])
        self.member_name_combobox.config(values=member_list)
        number_list = []
        for row in self.member_list:
            number_list.append(row[0])
        self.number_combobox.config(values=number_list)
        return True

    def check_out_validate(self, key):
        if key == 'catagory' or key == 'all':
            self.catagory_combobox.config(bootstyle='default')
            if self.catagory_combobox.get() not in self.catagory_array:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.insert('end', '警告！输入库存中查无此种类的商品！')
                self.batch_combobox.config(values=[])
                self.batch_combobox.delete(0, 'end')
                self.notice_entry.config(state='readonly', bootstyle='warning')
                self.catagory_combobox.config(bootstyle='warning')
            else:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.config(state='readonly', bootstyle='default')
            temp_catagory_list = []
            for row in self.catagory_array:
                if self.catagory_combobox.get() in row:
                    temp_catagory_list.append(row)
            self.catagory_combobox.config(values=temp_catagory_list)
        if key == 'batch':
            # if self.current==False:
            #     return True
            # for row in self.current:
            #     if row[2] == self.batch_combobox.get():
            #         self.count_rate = row[5]
            #         self.current_catagory_row = row
            #         break
            #     else:
            #         self.count_rate = False
            #         self.current_catagory_row = False
            self.catagory_combobox_matching()
            self.quantity_entry.delete(0, 'end')
            self.price_entry.delete(0, 'end')
            self.cost_entry.delete(0, 'end')
        if key == 'quantity' or key == 'all':
            self.quantity_entry.config(bootstyle='default')
            if re.compile('^[0-9]+\.?[0-9]*$').match(self.quantity_entry.get()) == None:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.insert(
                    'end', '错误！商品数量格式错误！应为一大于零的数字切结算时只保留两位小数')
                self.notice_entry.config(state='readonly', bootstyle='danger')
                self.quantity_entry.config(bootstyle='danger')
                return True
            else:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.config(state='readonly', bootstyle='default')
                self.cost_entry.delete(0, 'end')
                if self.current_catagory_row != False:
                    self.cost_entry.delete(0, 'end')
                    self.cost_entry.insert('end', format(
                        float(self.quantity_entry.get())*float(self.current_catagory_row[3]), '.2f'))
                    self.check_out_validate('cost')
                    spare_quantity = self.current_catagory_row[4]
                    for row in self.shopcart_list:
                        if self.current_catagory_row[0] == row[0]+row[1]:
                            spare_quantity = format(
                                float(spare_quantity)-float(row[2]), '.2f')
                    if float(self.quantity_entry.get()) > float(spare_quantity):
                        self.quantity_entry.delete(0, 'end')
                        self.quantity_entry.delete(0, 'end')
                        self.quantity_entry.insert(
                            'end', str(spare_quantity))
                        self.quantity_entry.config(bootstyle='default')

        if key == 'price' or key == 'all':
            self.price_entry.config(bootstyle='default')
            if re.compile('^[0-9]+\.?[0-9]*$').match(self.price_entry.get()) == None:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.insert(
                    'end', '错误！售价格式错误！应为一大于零的数字切结算时只保留两位小数')
                self.notice_entry.config(state='readonly', bootstyle='danger')
                self.price_entry.config(bootstyle='danger')
                return True
            else:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.config(state='readonly', bootstyle='default')
        if key == 'cost' or key == 'all':
            self.cost_entry.config(bootstyle='default')
            if re.compile('^[0-9]+\.?[0-9]*$').match(self.cost_entry.get()) == None:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.insert(
                    'end', '错误！成本价格式错误！应为一大于零的数字切结算时只保留两位小数')
                self.notice_entry.config(state='readonly', bootstyle='danger')
                self.cost_entry.config(bootstyle='danger')
                return True
            else:
                self.notice_entry.config(state='normal')
                self.notice_entry.delete(0, 'end')
                self.notice_entry.config(state='readonly', bootstyle='default')
        if key == 'member' or key == 'all':
            temp_member_list = []
            for row in self.member_list:
                if self.member_name_combobox.get() in row[1]:
                    temp_member_list.append(row[1])
            self.member_name_combobox.config(values=temp_member_list)
            self.member_matching('member')

        if key == 'number' or key == 'all':
            temp_number_list = []
            for row in self.member_list:
                if self.number_combobox.get() in row[0]:
                    temp_number_list.append(row[0])
            self.number_combobox.config(values=temp_number_list)
            self.member_matching('number')

        return True

    def add_to_shop_cart(self):
        def shopcart_remove(key):
            for index, row in enumerate(self.shopcart_list):
                if self.shopcart_dict[key] == row:
                    self.shopcart_menu.delete(index)
                    break
            self.shopcart_list.remove(self.shopcart_dict[key])
            del self.shopcart_dict[key]
            self.notice_entry.config(state='normal')
            self.notice_entry.delete(0, 'end')
            self.notice_entry.insert(0, '从购物车中删除成功！')
            self.notice_entry.config(state='readonly', bootstyle='default')

        warning_string = '警告！'
        Error_string = '错误！'
        if self.catagory_combobox.get() not in self.catagory_array:
            warning_string += '未在库存中发现该商品！您可以继续进行结算，但系统不会在库存表中做出任何\n更改。\n'
        if self.batch_combobox != '' and self.current_catagory_row == False:
            warning_string += '未发现该批次该产品！您可以继续进行结算，但系统不会在库存表中做出任何更改。\n'
        if re.compile('^[0-9]+\.?[0-9]*$').match(self.quantity_entry.get()) == None:
            Error_string += '错误！交易数量格式错误，应为一个数字，在进行结算时将保留两位小数。\n'
        if re.compile('^[0-9]+\.?[0-9]*$').match(self.price_entry.get()) == None:
            Error_string += '错误！售价格式错误，应为一个数字，在进行结算时将保留两位小数。\n'
        if re.compile('^[0-9]+\.?[0-9]*$').match(self.cost_entry.get()) == None:
            Error_string += '错误！成本价格式错误，应为一个数字，在进行结算时将保留两位小数。若您不需要记\n录该项，请填入0.\n'

        if Error_string != '错误！' and warning_string != '警告！':
            confirm_panel = ttk.Toplevel()
            pop_menu(confirm_panel)
            confirm_panel.resizable(0, 0)
            win_initialize(confirm_panel, 600, 346, '错误列表')
            show_text = ttk.Text(confirm_panel, width=600, height=346)
            show_text.grid(column=0, row=1, sticky=(E, W, S, N))
            if warning_string != '警告！' and Error_string == '错误！':
                show_text.insert('end', warning_string+'成功插入到购物车中')
            elif warning_string != '警告！' and Error_string != '错误！':
                show_text.insert('end', warning_string)
            if Error_string != '错误！':
                show_text.insert('end', Error_string+'插入失败')
            show_text.config(state='disabled')
        if Error_string == '错误！':
            self.shopcart_list.append([
                self.catagory_combobox.get(),
                self.batch_combobox.get(),
                float(self.quantity_entry.get()),
                float(self.price_entry.get()),
                float(self.cost_entry.get())
            ])
            t = self.catagory_combobox.get()+self.batch_combobox.get() + \
                ' '+self.quantity_entry.get()+' '+self.price_entry.get()
            self.shopcart_dict[t] = [
                self.catagory_combobox.get(),
                self.batch_combobox.get(),
                float(self.quantity_entry.get()),
                float(self.price_entry.get()),
                float(self.cost_entry.get())
            ]
            self.shopcart_menu.add_command(
                label=t, command=lambda arg=t: shopcart_remove(arg))
            self.notice_entry.config(state='normal')
            self.notice_entry.delete(0, 'end')
            self.notice_entry.insert(0, '插入购物车成功！')
            self.notice_entry.config(state='readonly', bootstyle='default')

    def final_checkout(self):
        def apply_all():
            for row in self.shopcart_list:
                temp = []
                temp.append(int(time.mktime(time.localtime())))
                temp.append(row[3])
                temp.append(row[2])
                temp.append(row[4])
                temp.append(row[0])
                temp.append(row[1])
                if self.db.is_in_stock(row[0]+row[1]):
                    temp.append(self.db.get_stock_storage(row[0]+row[1]))
                    self.db.stock_minus(row[0]+row[1], float(row[2]))
                else:
                    temp.append('非库存')
                if re.compile('^[0-9]+\.?[0-9]*$').match(self.wallet_entry.get()) != None:
                    temp.append(self.member_name_combobox.get())
                elif float(self.price_entry.get())-0.00>0.00001:
                    temp.append('非会员')
                elif float(self.price_entry.get())-0.00<0.00001:
                    temp.append('报损')
                self.db.sell_history_insert(temp)
            if self.wallet_pay.get() == 1:
                if deducted == False and self.db.is_in_member(self.number_combobox.get()):
                    self.db.member_update(
                        self.number_combobox.get(), value=float(total_price))
                elif deducted != False:
                    self.db.member_update(
                        self.number_combobox.get(), zero=True)
            if self.number_combobox.get() == self.current_order[1]:
                self.db.order_state_update(self.current_order[0])

            self.shopcart_dict = {}
            self.shopcart_list = []
            self.shopcart_menu.delete(0, 'end')
            confirm_panel.destroy()
            self.catagory_combobox.delete(0, 'end')
            self.batch_combobox.delete(0, 'end')
            self.quantity_entry.delete(0, 'end')
            self.price_entry.delete(0, 'end')
            self.cost_entry.delete(0, 'end')
            self.member_name_combobox.delete(0, 'end')
            self.number_combobox.delete(0, 'end')
            self.wallet_entry.delete(0, 'end')
            for key in self.catagory_button_dict:
                self.catagory_button_dict[key].destroy()
            self.catagory_button_dict = {}
            self.catagory_dict = {}
            self.catagory_array = []
            self.page_turn(-1)
            self.current_order = [False, False]

        def cancel():
            confirm_panel.destroy()

        total_price = 0.0
        continue_wallet_pay = False
        deducted = False
        for row in self.shopcart_list:
            total_price += row[3]
        if self.wallet_pay.get() == 1:
            if self.db.is_in_member(self.number_combobox.get()):
                if re.compile('^[0-9]+\.?[0-9]*$').match(self.wallet_entry.get()) != None:
                    if float(self.wallet_entry.get()) <= total_price:
                        continue_wallet_pay = messagebox.askyesno(
                            title='会员余额不足', message='会员余额不足，是否继续使用会员余额进行结算？\n继续结算将会直接扣空余额，您应该使用其他支付方法补齐差价')
                        if continue_wallet_pay == 1:
                            deducted = total_price - \
                                float(self.wallet_entry.get())
                        else:
                            self.wallet_pay.set(value=0)
                else:
                    messagebox.showerror(
                        title='错误', message='错误的会员,请检查或使用其他支付方法。\n系统依赖电话号码查询会员，请核对电话号码。')
                    return False
            else:
                messagebox.showerror(
                    title='错误', message='错误的会员,请检查或使用其他支付方法。\n系统依赖电话号码查询会员，请核对电话号码。')
                return False
        confirm_panel = ttk.Toplevel()
        pop_menu(confirm_panel)
        confirm_panel.resizable(0, 0)
        win_initialize(confirm_panel, 900, 600, '商品列表')
        continue_button = ttk.Button(
            confirm_panel, text='确认结算', command=apply_all, bootstyle='success')
        cancel_button = ttk.Button(
            confirm_panel, text='取消结算', command=cancel, bootstyle='danger')
        show_text = ttk.Text(confirm_panel)
        show_text.grid(column=0, row=0, columnspan=3,
                       rowspan=3, sticky=(E, W, S, N))
        continue_button.grid(column=0, row=3, sticky=(E, W, S, N))
        cancel_button.grid(column=2, row=3, sticky=(E, W, S, N))
        show_text.insert('end', '\t\t'+'商品种类\t\t商品批次\t\t商品数量/斤\t\t商品价格\n')
        for row in self.shopcart_list:
            show_text.insert(
                'end', '\t\t'+row[0]+'\t\t'+row[1]+'\t\t'+str(row[2])+'\t\t'+str(row[3]))
            show_text.insert('end', '\n')
        show_text.insert('end', '总价为{}'.format(total_price))
        if self.wallet_pay.get() == 1:
            if deducted == False and self.db.is_in_member(self.number_combobox.get()):
                show_text.insert('end', '本次支付全部从客户余额中支出，支付后客户余额{}元'.format(
                    float(self.wallet_entry.get())-total_price))
            elif deducted != False:
                show_text.insert(
                    'end', '本次支付客户余额不足，余额清零后仍需通过其他途径支付{}元'.format(deducted))
        show_text.config(state='disabled')
        for i in range(3):
            confirm_panel.columnconfigure(i, weight=1)
            confirm_panel.rowconfigure(i, weight=1)
        confirm_panel.rowconfigure(3, weight=1)

    def member_entry_clear(self, mode):
        if mode == 'number':
            self.wallet_entry.config(state='normal')
            self.wallet_entry.delete(0, 'end')
            self.wallet_entry.config(state='disable')
            self.member_name_combobox.delete(0, 'end')
        if mode == 'member':
            self.wallet_entry.config(state='normal')
            self.wallet_entry.delete(0, 'end')
            self.wallet_entry.config(state='disable')
            self.number_combobox.delete(0, 'end')

class statistics_frame_init:
    def __init__(self,parent:ttk.Frame) -> None:
        self.parent=parent
        self.db=DB_statistics()
        self.frame_gui()

    def frame_gui(self):
        self.start_time_label=ttk.Label(self.parent,text='起始时间：',justify='right')
        self.start_time_entry=ttk.Entry(self.parent,width=25)
        self.end_time_label=ttk.Label(self.parent,text='终止时间：',justify='right')
        self.end_time_entry=ttk.Entry(self.parent,width=25)
        self.total_price_label=ttk.Label(self.parent,text='营业收入：')
        self.total_price_entry=ttk.Entry(self.parent,width=25)
        self.total_cost_label=ttk.Label(self.parent,text='总成本价：')
        self.total_cost_entry=ttk.Entry(self.parent,width=25)
        self.gross_profit_label=ttk.Label(self.parent,text='总毛利润：')
        self.gross_profit_entry=ttk.Entry(self.parent,width=25)
        self.profit_rate_label=ttk.Label(self.parent,text='总毛利率：')
        self.profit_rate_entry=ttk.Entry(self.parent,width=25)
        columnid=['rank','quantity','profit_rate','volume','most_pay']
        showname=['排行','商品销售量/斤','商品销售额/元','商品毛利率','消费额最高客户']
        self.statistic_table=table_view(self.parent,columnid=columnid,showname=showname,data=[[]],readonly=1)
        self.day_button=ttk.Button(self.parent,text='今日数据',command=lambda:self.auto_date_insert('day'))
        self.week_button=ttk.Button(self.parent,text='本周数据',command=lambda:self.auto_date_insert('week'))
        self.month_button=ttk.Button(self.parent,text='本月数据',command=lambda:self.auto_date_insert('month'))
        self.year_button=ttk.Button(self.parent,text='本年数据',command=lambda:self.auto_date_insert('year'))
        
        self.start_time_label.grid(column=0,row=0,padx=5,pady=5,sticky=(E,W,S,N))
        self.start_time_entry.grid(column=1,row=0,columnspan=2,padx=5,pady=5,sticky=(E,W,S,N))
        self.end_time_label.grid(column=4,row=0,padx=5,pady=5,sticky=(E,W,S,N))
        self.end_time_entry.grid(column=5,row=0,columnspan=2,padx=5,pady=5,sticky=(E,W,S,N))
        self.total_price_label.grid(column=0,row=1,padx=5,pady=5,sticky=(E,W,S,N))
        self.total_price_entry.grid(column=0,row=2,padx=5,pady=5,sticky=(E,W,S,N))
        self.total_cost_label.grid(column=2,row=1,padx=5,pady=5,sticky=(E,W,S,N))
        self.total_cost_entry.grid(column=2,row=2,padx=5,pady=5,sticky=(E,W,S,N))
        self.gross_profit_label.grid(column=4,row=1,padx=5,pady=5,sticky=(E,W,S,N))
        self.gross_profit_entry.grid(column=4,row=2,padx=5,pady=5,sticky=(E,W,S,N))
        self.profit_rate_label.grid(column=6,row=1,padx=5,pady=5,sticky=(E,W,S,N))
        self.profit_rate_entry.grid(column=6,row=2,padx=5,pady=5,sticky=(E,W,S,N))
        self.statistic_table.grid(column=0,row=3,columnspan=7,rowspan=4,padx=5,pady=5,sticky=(E,W,S,N))
        self.day_button.grid(column=0,row=7,padx=5,pady=5,sticky=(E,W,S,N))
        self.week_button.grid(column=2,row=7,padx=5,pady=5,sticky=(E,W,S,N))
        self.month_button.grid(column=4,row=7,padx=5,pady=5,sticky=(E,W,S,N))
        self.year_button.grid(column=6,row=7,padx=5,pady=5,sticky=(E,W,S,N))

        for i in range(7):
            self.parent.columnconfigure(i,weight=1)
            self.parent.rowconfigure(i,weight=1)
        self.parent.rowconfigure(7,weight=1)

        self.total_price_entry.config(state='readonly')
        self.total_cost_entry.config(state='readonly')
        self.gross_profit_entry.config(state='readonly')
        self.profit_rate_entry.config(state='readonly')

        self.start_time_entry.bind('<Double-1>',self.date_insert)
        self.end_time_entry.bind('<Double-1>',self.date_insert)
        self.start_time_entry.bind('<Return>',lambda e:self.other_date_insert())
        self.end_time_entry.bind('<Return>',lambda e:self.other_date_insert())

    def date_insert(self,event):
        t = str(Querybox.get_date(self.start_time_entry))
        event.widget.config(state='normal')
        event.widget.delete(0, 'end')
        t+=' 00:00:00'
        event.widget.insert('end', t)

    def today(self):
        start = time.strptime(time.strftime("%Y-%m-%d 00:00:00", time.localtime()), "%Y-%m-%d %H:%M:%S")
        start_stamp = int(time.mktime(start))
        end = time.strptime(time.strftime("%Y-%m-%d 23:59:59", time.localtime()), "%Y-%m-%d %H:%M:%S")
        end_stamp = int(time.mktime(end))
        return [start_stamp,end_stamp]

    def this_week(self):
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        monday = today - oneday * today.weekday()
        week_stamp = time_str_to_stamp("{}-{}-{}" .format (monday.year, monday.month, monday.day),mode=2)
        next_week_stamp = time_str_to_stamp("{}-{}-{}" .format (monday.year, monday.month, monday.day + 7),mode=2)
        return [week_stamp,next_week_stamp-1]
    
    def this_month(self):
        today = datetime.date.today()
        month_stamp = time_str_to_stamp("{}-{}-{}" .format (today.year, today.month, 1),mode=2)
        next_month_stamp = time_str_to_stamp("{}-{}-{}" .format (today.year, today.month + 1, 1),mode=2)
        return [month_stamp,next_month_stamp-1]
    
    def this_year(self):
        today = datetime.date.today()
        year_stamp = time_str_to_stamp("{}-{}-{}" .format (today.year, 1, 1),mode=2)
        next_year_stamp = time_str_to_stamp("{}-{}-{}" .format (today.year + 1, 1, 1),mode=2)
        return [year_stamp,next_year_stamp-1]
    
    def entry_unlock(self):
        self.total_price_entry.config(state='normal')
        self.total_cost_entry.config(state='normal')
        self.gross_profit_entry.config(state='normal')
        self.profit_rate_entry.config(state='normal')

    def entry_delete_content(self):
        self.total_price_entry.delete(0,'end')
        self.total_cost_entry.delete(0,'end')
        self.gross_profit_entry.delete(0,'end')
        self.profit_rate_entry.delete(0,'end')

    def update_all(self,start,end):
        price=self.db.get_turnover_sum(start,end)
        cost=self.db.get_cost_sum(start,end)
        gross_profit=self.db.gross_profit(start,end)
        gross_profit_rate=self.db.gross_profit_rate(start,end)
        self.total_price_entry.insert(0,price)
        self.total_cost_entry.insert(0,cost)
        self.gross_profit_entry.insert(0,gross_profit)
        self.profit_rate_entry.insert(0,gross_profit_rate)
        self.table_data_load(start,end)
    def entry_lock(self):
        self.total_price_entry.config(state='readonly')
        self.total_cost_entry.config(state='readonly')
        self.gross_profit_entry.config(state='readonly')
        self.profit_rate_entry.config(state='readonly')

    def auto_date_insert(self,mode):
        if mode not in ['day','week','month','year']:
            return False
        if mode =='day':
            self.start_time_entry.delete(0,'end')
            self.start_time_entry.insert('end',stamp_to_time_str(self.today()[0]))
            self.end_time_entry.delete(0,'end')
            self.end_time_entry.insert('end',stamp_to_time_str(self.today()[1]))
            self.entry_unlock()
            self.entry_delete_content()
            self.update_all(self.today()[0],self.today()[1])
            self.entry_lock()
        if mode=='week':
            self.start_time_entry.delete(0,'end')
            self.start_time_entry.insert('end',stamp_to_time_str(self.this_week()[0]))
            self.end_time_entry.delete(0,'end')
            self.end_time_entry.insert('end',stamp_to_time_str(self.this_week()[1]))
            self.entry_unlock()
            self.entry_delete_content()
            self.update_all(self.this_week()[0],self.this_week()[1])
            self.entry_lock()
        if mode=='month':
            self.start_time_entry.delete(0,'end')
            self.start_time_entry.insert('end',stamp_to_time_str(self.this_month()[0]))
            self.end_time_entry.delete(0,'end')
            self.end_time_entry.insert('end',stamp_to_time_str(self.this_month()[1]))
            self.entry_unlock()
            self.entry_delete_content()
            self.update_all(self.this_month()[0],self.this_month()[1])
            self.entry_lock()
        if mode =='year':
            self.start_time_entry.delete(0,'end')
            self.start_time_entry.insert('end',stamp_to_time_str(self.this_year()[0]))
            self.end_time_entry.delete(0,'end')
            self.end_time_entry.insert('end',stamp_to_time_str(self.this_year()[1]))
            self.entry_unlock()
            self.entry_delete_content()
            self.update_all(self.this_year()[0],self.this_year()[1])
            self.entry_lock()

    def other_date_insert(self):
        error=0
        def datetime_wash(signal=0):
            unwashed_date = signal
            washed_date = ''
            for i in unwashed_date:
                if i == '：':
                    washed_date = washed_date+':'
                    continue
                washed_date = washed_date+i
            return washed_date
        if verify_datetime(datetime_wash(self.start_time_entry.get()))==False:
            messagebox.showerror(title='时间格式错误',message='起始时间格式错误，时间应为形如 2222-11-22 00:00:00,且客观上可存在的时间')
            error=1
        if verify_datetime(datetime_wash(self.end_time_entry.get()))==False:
            messagebox.showerror(title='时间格式错误',message='终止格式错误，时间应为形如 2222-11-22 00:00:00,且客观上可存在的时间')
            error=1
        if error==1:
            return False
        self.entry_unlock()
        self.entry_delete_content()
        start=time_str_to_stamp(datetime_wash(self.start_time_entry.get()))
        end=time_str_to_stamp(datetime_wash(self.end_time_entry.get()))
        if start>= end:
            messagebox.showwarning(title='警告',message='起始时间晚于终止时间是反常的，这样做无法取得任何数据，请检查。')
        self.update_all(start,end)
        self.entry_lock()

    def table_data_load(self,start_time_stamp, end_time_stamp):
        price=self.db.get_catagory_rank('turnover','catagory',start_time_stamp, end_time_stamp)
        quantity=self.db.get_catagory_rank('volume','catagory',start_time_stamp, end_time_stamp)
        profit_rate=self.db.get_profit_rate_rank(start_time_stamp, end_time_stamp)
        customer=self.db.get_catagory_rank('turnover','member',start_time_stamp, end_time_stamp)
        rank_list=[]
        for i in range(len(price)):
            rank_list.append(i+1)
        temp=[]
        for i in range(len(rank_list)):
            temp_row=[]
            temp_row.append(rank_list[i])
            temp_row.append(quantity[i])
            temp_row.append(price[i])
            temp_row.append(profit_rate[i])
            if i<len(customer):
                temp_row.append(customer[i])
            else:
                temp_row.append('')
            temp.append(temp_row)
        self.statistic_table.reload(temp)
        