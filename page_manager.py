from job_functions import *


class page_manager_init():
    def __init__(self, parent: ttk.Window) -> None:
        self.parent = parent
        self.setting_panel_exist=False
        self.tab_manager = ttk.Notebook(self.parent)
        # 结算框架
        self.checkout = ttk.Frame(self.tab_manager)
        self.tab_manager.add(self.checkout, text='　结算　')
        # 库存框架
        self.stock = ttk.Frame(self.tab_manager)
        self.tab_manager.add(self.stock, text='　库存　')
        # 会员框架
        self.member = ttk.Frame(self.tab_manager)
        self.tab_manager.add(self.member, text='　会员　')
        # 订单框架
        self.order = ttk.Frame(self.tab_manager)
        self.tab_manager.add(self.order, text='　订单　')
        # 交易历史框架
        self.history = ttk.Frame(self.tab_manager)
        self.tab_manager.add(self.history, text='交易记录')
        # 统计框架
        self.statistics = ttk.Frame(self.tab_manager)
        self.tab_manager.add(self.statistics, text='　统计　')

        def setting():
            def cancel_insert():
                self.setting_panel_exist=False
                setting_panel.destroy()
            if self.setting_panel_exist==True:
                return False
            self.setting_panel_exist=True
            setting_panel=ttk.Toplevel()
            pop_menu(setting_panel)
            setting_panel_ini(setting_panel)
            setting_panel.protocol("WM_DELETE_WINDOW", cancel_insert)

        button_dic = {
            'checkout': {'id': 'checkout', 'name': ' 结算 '},
            'stock': {'id': 'stock', 'name': ' 库存 '},
            'member': {'id': 'member', 'name': ' 会员 '},
            'order': {'id': 'order', 'name': ' 订单 '},
            'history': {'id': 'history', 'name': '交易记录'},
            'statistics': {'id': 'statistics', 'name': ' 统计 '},
        }

        def tap_switch(buton_name):
            if buton_name == button_dic['checkout']['id']:
                self.tab_manager.select(self.checkout)
                self.button_style_reset()
                self.checkout_button.config(bootstyle='success')
                self.checkout_instance.page_turn(-1)
            if buton_name == button_dic['stock']['id']:
                self.tab_manager.select(self.stock)
                self.button_style_reset()
                self.stock_button.config(bootstyle='success')
                self.stock_instance.flush_data()
            if buton_name == button_dic['member']['id']:
                self.tab_manager.select(self.member)
                self.button_style_reset()
                self.member_button.config(bootstyle='success')
                self.member_instance.flush_data()
            if buton_name == button_dic['order']['id']:
                self.tab_manager.select(self.order)
                self.button_style_reset()
                self.order_button.config(bootstyle='success')
                self.order_instance.flush_data()
            if buton_name == button_dic['history']['id']:
                self.tab_manager.select(self.history)
                self.button_style_reset()
                self.history_button.config(bootstyle='success')
                self.history_instance.flush_data()
            if buton_name == button_dic['statistics']['id']:
                self.tab_manager.select(self.statistics)
                self.button_style_reset()
                self.statistics_button.config(bootstyle='success')
        # 功能按钮
        self.checkout_button = ttk.Button(
            self.parent, text=button_dic['checkout']['name'], command=lambda: tap_switch(button_dic['checkout']['id']))
        self.stock_button = ttk.Button(
            self.parent, text=button_dic['stock']['name'], command=lambda: tap_switch(button_dic['stock']['id']))
        self.member_button = ttk.Button(
            self.parent, text=button_dic['member']['name'], command=lambda: tap_switch(button_dic['member']['id']))
        self.order_button = ttk.Button(
            self.parent, text=button_dic['order']['name'], command=lambda: tap_switch(button_dic['order']['id']))
        self.history_button = ttk.Button(
            self.parent, text=button_dic['history']['name'], command=lambda: tap_switch(button_dic['history']['id']))
        self.statistics_button = ttk.Button(
            self.parent, text=button_dic['statistics']['name'], command=lambda: tap_switch(button_dic['statistics']['id']))
        # 设置按钮
        self.setting_button = ttk.Button(
            self.parent, text='　设置　', command=setting)
        self.button_style_reset()
        self.checkout_button.grid(
            column=0, row=0, padx=5, pady=5, sticky=(W, S, N, E))
        self.stock_button.grid(column=0, row=1, padx=5,
                               pady=5, sticky=(W, S, N, E))
        self.member_button.grid(column=0, row=2, padx=5,
                                pady=5, sticky=(W, S, N, E))
        self.order_button.grid(column=0, row=3, padx=5,
                               pady=5, sticky=(W, S, N, E))
        self.history_button.grid(
            column=0, row=4, padx=5, pady=5, sticky=(W, S, N, E))
        self.statistics_button.grid(
            column=0, row=5, padx=5, pady=5, sticky=(W, S, N, E))

        self.setting_button.grid(
            column=5, row=6, padx=5, pady=5, sticky=(W, S, N, E))

        self.tab_manager.grid(column=1, row=0, columnspan=5,
                              rowspan=6, sticky=(W, S, N, E))

        for i in range(7):
            self.parent.rowconfigure(i, weight=1)
        # self.parent.columnconfigure(0,weight=1)
        for i in range(1, 6):
            self.parent.columnconfigure(i, weight=1)
        pop_menu(self.parent)
        self.checkout_instance=checkout_frame_init(self.checkout)
        self.stock_instance = stock_frame_init(self.stock)
        self.member_instance = member_frame_init(self.member)
        self.order_instance = order_frame_init(self.order)
        self.history_instance = history_frame_init(self.history)
        self.statistics_instance=statistics_frame_init(self.statistics)
        tap_switch(button_dic['checkout']['id'])
        self.parent.protocol("WM_DELETE_WINDOW", self.exit)

        # def debug(event):
        #     print(event.x,event.y)
        # self.parent.bind('<Motion>',debug)
    def button_style_reset(self):
        self.checkout_button.config(bootstyle='default')
        self.stock_button.config(bootstyle='default')
        self.member_button.config(bootstyle='default')
        self.order_button.config(bootstyle='default')
        self.history_button.config(bootstyle='default')
        self.statistics_button.config(bootstyle='default')
    
    def exit(self):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        c.execute("UPDATE settings SET winwidth={},winheight={}".format(int(self.parent.winfo_width()),int(self.parent.winfo_height())))
        conn.commit()
        conn.close()
        self.parent.destroy()