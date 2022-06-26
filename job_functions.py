from checkout_statistics_functions import *
from client_initialize import general_style_set





class setting_panel_ini:
    def __init__(self, parent: ttk.Toplevel) -> None:
        self.parent = parent
        self.style_var = ttk.IntVar(value=0)
        self.db = DB_setting()
        self.light_theme_list = ['cosmo', 'flatly', 'journal',  'lumen', 'minty',
                                 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
        self.dark_theme_list = [
            'solar', 'superhero', 'darkly', 'cyborg', 'vapor']
        win_initialize(self.parent, int(int(self.parent.winfo_screenwidth(
        ))*0.20), int(int(self.parent.winfo_screenheight())*0.20), '设置')
        self.parent.resizable(0, 0)
        self.theme_frame = ttk.LabelFrame(self.parent, text='设置主题')
        self.user_frame = ttk.LabelFrame(self.parent, text='设置用户')
        self.style_type_checkbutton = ttk.Checkbutton(
            self.theme_frame, text='亮色调', variable=self.style_var, offvalue=0, onvalue=1, command=self.style_transform, bootstyle="round-toggle")
        self.style_combobox = ttk.Combobox(self.theme_frame, state='readonly')
        self.style_combobox.bind(
            '<<ComboboxSelected>>', lambda e: self.style_modify())
        self.style_transform()
        self.style_type_checkbutton.grid()
        self.style_combobox.grid()
        self.theme_frame.grid(column=0, row=0, sticky=(E, W, S, N))
        self.user_combobox = ttk.Combobox(
            self.user_frame, values=self.db.user_info_load())
        self.user_combobox.current(0)
        self.delete_user_button = ttk.Button(
            self.user_frame, text='删除用户', command=lambda: self.delete_user())
        self.new_user_button = ttk.Button(
            self.user_frame, text='新建用户', command=lambda: self.new_user())
        self.modify_key_button = ttk.Button(
            self.user_frame, text='修改密码 ', command=lambda: self.modify_key())
        self.user_combobox.grid(
            column=0, row=0, columnspan=3, sticky=(E, W, S, N))
        self.delete_user_button.grid(
            column=0, row=1, padx=2, pady=2, sticky=(E, W, S, N))
        self.new_user_button.grid(
            column=1, row=1, padx=2, pady=2, sticky=(E, W, S, N))
        self.modify_key_button.grid(
            column=2, row=1, padx=2, pady=2, sticky=(E, W, S, N))
        self.user_frame.grid(column=0, row=1, sticky=(E, W, S, N))
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=1)
        pop_menu(self.parent)

    def style_transform(self):
        if self.style_var.get() == 0:
            self.style_type_checkbutton.config(text='亮色调')
            self.style_combobox.config(values=self.light_theme_list)
            self.style_combobox.current(0)
        elif self.style_var.get() == 1:
            self.style_type_checkbutton.config(text='暗色调')
            self.style_combobox.config(values=self.dark_theme_list)
            self.style_combobox.current(0)

    def style_modify(self):
        try:
            general_style_set(self.style_combobox.get())
            self.db.theme_update(self.style_combobox.get())
            messagebox.showwarning(
                parent=self.parent, title='警告', message='修改主题可能会导致当次会话中部分布局错误，重启客户端后会恢复正常，请尽快重启客户端。')
        except Exception as e:
            return e

    def delete_user(self):
        if self.user_combobox.get() in self.db.user_info_load():
            if len(self.db.user_info_load()) > 1:
                self.db.delete_user(self.user_combobox.get())
                self.user_combobox.config(values=self.db.user_info_load())
                self.user_combobox.delete(0, 'end')
            else:
                messagebox.showerror(
                    parent=self.parent, title='错误', message='您不能删除最后一个用户，这会导致无法登录')
        else:
            messagebox.showerror(parent=self.parent,
                                 title='错误', message='查无此用户，请检查。')

    def new_user(self):
        if self.user_combobox.get() != 'abcd1234':
            if self.user_combobox.get() not in self.db.user_info_load():
                if re.compile('^\w{1}[\w\d]{5,11}$').match(self.user_combobox.get()):
                    t = Querybox.get_string(
                        parent=self.parent, prompt='请输入密码', title='请输入密码')
                    if re.compile('^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,15}$').match(t):
                        t = [self.user_combobox.get(), t]
                        self.db.new_user(t)
                        self.user_combobox.config(
                            values=self.db.user_info_load())
                        self.user_combobox.delete(0, 'end')
                    else:
                        messagebox.showerror(
                            parent=self.parent, title='错误', message='密码应为由字母和数字组成的8到15位字符串。')
                else:
                    messagebox.showerror(
                        parent=self.parent, title='错误', message='用户名应为由字母和数字组成的6到11位字符串，且必须以字母开头。')
            else:
                messagebox.showerror(parent=self.parent,
                                     title='错误', message='已存在此用户。')
        else:
            t = Querybox.get_string(
                parent=self.parent, prompt='请输入密码', title='请输入密码')
            if re.compile('^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,15}$').match(t):
                self.db.default_user_revie(t)
                self.user_combobox.config(values=self.db.user_info_load())
                self.user_combobox.delete(0, 'end')

    def modify_key(self):
        if self.user_combobox.get() in self.db.user_info_load():
            t = Querybox.get_string(
                parent=self.parent, prompt='请输入密码', title='请输入密码')
            if re.compile('^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,15}$').match(t):
                self.db.update_user(self.user_combobox.get(), t)
                self.user_combobox.config(values=self.db.user_info_load())
                self.user_combobox.delete(0, 'end')
            else:
                messagebox.showerror(
                    parent=self.parent, title='错误', message='密码应为由字母和数字组成的8到15位字符串。')

        else:
            messagebox.showerror(parent=self.parent,
                                 title='错误', message='该用户不存在。')
