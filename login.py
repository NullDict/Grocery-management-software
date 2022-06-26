from db_classes import *
import re
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from StableClass import *
from stock_member_function import pop_menu

class Sign_in:
    def __init__(self, parent: ttk.Window):
        # 定义区
        def validate_username():
            if re.compile('^\w{1}[\w\d]{5,11}$').match(Entry_user.get()):
                Label_ShowValidate.config(text='           ')
                Label_ShowValidate2.config(
                    text='                                               ')
                Entry_user.config(bootstyle='default')
            else:
                if Entry_user.get() !='':
                    Label_ShowValidate.config(text=' 用户名错误！用户名应为:以字母开头 ')
                    Label_ShowValidate2.config(text='由数字和字母组成,长度在6~11位之间 ')
                    Entry_user.config(bootstyle='danger')
            return True

        def vadlidate_password():
            if re.compile('^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{7,15}$').match(Entry_Password.get()):
                Label_ShowValidate.config(text='           ')
                Label_ShowValidate2.config(
                    text='                                               ')
                Entry_Password.config(bootstyle='default')
            else:
                if Entry_Password.get()!='':
                    Label_ShowValidate.config(text='密码错误！密码必须:包括数字、')
                    Label_ShowValidate2.config(text='字母两种字符,长度在8-15位之间')
                    Entry_Password.config(bootstyle='danger')
            return True

        def db_verify(user, password):
            result = DB_login_verify(user, password).verify()
            if result[0] == 0:
                messagebox.showerror(title='登陆失败！', message='用户名不存在！')
                if result[1] == 1:
                    messagebox.showinfo(title='提示', message='或许您记错了用户名')
                    return False
                return False
            if result[0] == 1:
                if result[1] == 1:
                    return True
                else:
                    messagebox.showerror(
                        title='密码错误！', message='密码错误！如果您忘记密码请点击忘记密码选项')
                    return False

        def login_verification(*args):
            if re.compile('^\w{1}[\w\d]{5,11}$').match(Entry_user.get()):
                if re.compile('^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,15}$').match(Entry_Password.get()):
                    if db_verify(Entry_user.get(), Entry_Password.get()):
                        self.parent.deiconify()
                        login_window.destroy()

                else:
                    messagebox.showwarning(title='警告', message='请确认您的密码为合理格式')
            else:
                messagebox.showwarning(title='警告', message='请确认您的用户名为合理格式')

            return 0
        # 工作区
        self.parent = parent
        #win_initialize(self.parent, 500, 289, '登录')
        # login_window = ttk.Frame(self.parent, width=500, height=289)   #此处为使用frame作为解决方案的遗留，留作纪念
        # login_window.grid()
        login_window = ttk.Toplevel()
        pop_menu(login_window)
        win_initialize(login_window, 500, 289, '登录')
        login_window.resizable(0, 0)
        try:
            login_window.iconbitmap('fish.ico')
        except:
            pass
        self.parent.withdraw()
        font_style = ttk.Style()
        font_style.configure('title.TLabel', font=('Helvetica', 14))

        # 组件定义区
        Label_Title = ttk.Label(
            login_window, text='请输入用户名和密码', justify=CENTER, style='title.TLabel')
        Label_User = ttk.Label(login_window, text='用户名：', justify=RIGHT)
        Entry_user = ttk.Entry(
            login_window, width=20, validate='all', validatecommand=validate_username)
        Label_Password = ttk.Label(login_window, text='密码：', justify=RIGHT)
        Entry_Password = ttk.Entry(
            login_window, width=20, show='⭐', validate='all', validatecommand=vadlidate_password)
        Label_ShowValidate = ttk.Label(login_window, text='           ')
        Label_ShowValidate2 = ttk.Label(
            login_window, text='                                               ')
        Button_Login = ttk.Button(
            login_window, text='　登录　', command=login_verification)
        Entry_Password.bind('<Return>', login_verification)
        Button_ForgetPassword = ttk.Button(login_window, text='忘记密码')

        # 组件布局区
        Label_Title.grid(column=2, row=0, columnspan=3,
                         pady=5, sticky=(W, S, E, N))
        Label_User.grid(column=1, row=1, padx=20, pady=5, sticky=(W, S, E, N))
        Entry_user.grid(column=2, row=1, columnspan=2,padx=(0,120),
                        pady=5, sticky=(W, S, E, N))
        Label_Password.grid(column=1, row=2, padx=20,
                            pady=5, sticky=(W, S, E, N))
        Entry_Password.grid(column=2, row=2, columnspan=2,padx=(0,120),
                            pady=5, sticky=(W, S, E, N))
        Label_ShowValidate.grid(column=1, row=3, columnspan=4)
        Label_ShowValidate2.grid(column=1, row=4, columnspan=4)
        Button_Login.grid(column=1, row=5, padx=5, pady=5, sticky=(E))
        Button_ForgetPassword.grid(column=3, row=5, padx=5, pady=10)

        # 窗口权重分配
        login_window.columnconfigure(0, weight=1)
        login_window.columnconfigure(1, weight=1)
        login_window.columnconfigure(2, weight=1)
        login_window.columnconfigure(3, weight=1)
        #login_window.columnconfigure(4, weight=1)
        login_window.rowconfigure(0, weight=1)
        login_window.rowconfigure(1, weight=1)
        login_window.rowconfigure(2, weight=1)
        login_window.rowconfigure(3, weight=1)
        login_window.rowconfigure(4, weight=1)
        login_window.rowconfigure(5, weight=1)
# 用来处理不进行登录操作时的退出操作

        def exist_without_login():
            self.parent.destroy()
            pass
        login_window.protocol("WM_DELETE_WINDOW", exist_without_login)
        pass

