import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db_classes import *
from StableClass import *


class client_init():
    def __init__(self, parent: ttk.Window) -> None:
        self.parent = parent
        db_setting = DB_load_client_setting()
        win_info = db_setting.setting()
        general_style_set(win_info[1])
        win_initialize(self.parent, win_info[2], win_info[3], '水产品超市管理系统')
        try:
            self.parent.iconbitmap('fish.ico')
        except:
            pass

class general_style_set():
    def __init__(self, style) -> None:
        self.style = style
        ttk.Style(self.style)
        font_style = ttk.Style()
        font_style.configure('title.TLabel', font=('Helvetica', 14))
        label_font_style = ttk.Style()
        label_font_style.configure('notice.TLabel', font=('Helvetica', 14))
        TreeviewStyle = ttk.Style()
        TreeviewStyle.configure('Treeview', rowheight=40)
        No_Head_Notebook = ttk.Style()
        No_Head_Notebook.layout('TNotebook.Tab', [])
