import sqlite3

# 如果数据库不存在，恢复数据库


def db_initialize():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings(
            id          INT     PRIMARY KEY,
            theme       VARCHAR(20),
            winwidth    INT,
            winheight   INT
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS login(
            id      VARCHAR(20) PRIMARY KEY     NOT NULL,
            key     VARCHAR(20) NOT NULL,
            hide    INT DEFAULT 0
    )''')
    t = c.execute("SELECT * FROM settings")
    temp = []
    for row in t:
        temp.append(row)
    if len(temp) == 0:
        c.execute("INSERT INTO settings VALUES(1, 'lumen', 1600,768)")
    t = c.execute("SELECT * FROM login")
    temp = []
    for row in t:
        temp.append(row)
    if len(temp) == 0:
        c.execute("INSERT INTO login VALUES('abcd1234', 'abcd1234', 0)")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS member(
            number  VARCHAR(20) PRIMARY KEY NOT NULL,
            name    VARCHAR(20)  NOT NULL,
            wallet  VARCHAR(20)         NOT NULL,
            points  VARCHAR(20)   DEFAULT  0,
            reg_date    INTEGER      DEFAULT (datetime('now','localtime')),
            spare1  VARCHAR(20)  DEFAULT NULL,
            spare2  VARCHAR(20)  DEFAULT NULL
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS stock(
            id              VARCHAR(20)  PRIMARY KEY NOT NULL,
            catagory        VARCHAR(20)  NOT NULL,
            batch           VARCHAR(20)  NOT NULL,
            price           VARCHAR(20)  NOT NULL,
            quantity        VARCHAR(20)  NOT NULL,
            selling_price   VARCHAR(20)  NOT NULL,
            date            INTEGER      DEFAULT (datetime('now', 'localtime')),
            expire          INTEGER      DEFAULT (datetime('now', 'localtime','+1 day')),
            storage         VARCHAR(20)  NOT NULL
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders(
            id              VARCHAR(20)  PRIMARY KEY NOT NULL,
            customer        VARCHAR(20)  NOT NULL,
            number          VARCHAR(20)  NOT NULL,
            catagory        VARCHAR(20)  NOT NULL,
            quantity        VARCHAR(20)  NOT NULL,
            booking_date    INT          DEFAULT (datetime('now', 'localtime')),
            remarks         TEXT,
            state           INT
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS purchase_history(
            id              VARCHAR(20)  PRIMARY KEY NOT NULL,
            catagory        VARCHAR(20)  NOT NULL,
            batch           VARCHAR(20)  NOT NULL,
            price           VARCHAR(20)  NOT NULL,
            quantity        VARCHAR(20)  NOT NULL,
            selling_price   VARCHAR(20)  NOT NULL,
            expire          INTEGER      DEFAULT (datetime('now', 'localtime','+1 day')),
            storage         VARCHAR(20)  NOT NULL
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sell_history(
                id              INTEGER      NOT NULL,
                turnover        VARCHAR(20)  NOT NULL,
                volume          VARCHAR(20)  NOT NULL,
                cost            VARCHAR(20)  NOT NULL,
                catagory        VARCHAR(20)  NOT NULL,
                batch           VARCHAR(20)  NOT NULL,
                storage         VARCHAR(20)  NOT NULL,
                member          VARCHAR(20)  NOT NULL
            )''')
    conn.commit()
    conn.close()


db_initialize()


class DB_load_client_setting:
    def __init__(self) -> None:
        self.login_settings = []
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        temp = c.execute('''SELECT * FROM settings;''')
        for row in temp:
            self.login_settings = row
        conn.commit()
        conn.close()
        pass

    def setting(self):
        return self.login_settings


class DB_setting:
    def __init__(self) -> None:
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()

        conn.commit()
        conn.close()

    def theme_update(self, theme):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        try:
            t = c.execute(
                '''UPDATE settings SET theme = '{}';'''.format(theme))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        conn.commit()
        conn.close()
        return True

    def user_info_load(self):
        temp = []
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        user_data = c.execute('''SELECT id FROM login WHERE hide!=1;''')
        for row in user_data:
            temp.append(row[0])
        conn.commit()
        conn.close()
        return temp

    def delete_user(self, id):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        if id != 'abcd1234':
            try:
                c.execute('''DELETE FROM login WHERE id='{}';'''.format(id))
            except Exception as e:
                conn.commit()
                conn.close()
                return e
        else:
            try:
                c.execute(
                    '''UPDATE login SET hide=1,key="***" WHERE id="abcd1234";'''.format(id))
            except Exception as e:
                conn.commit()
                conn.close()
                return e
        conn.commit()
        conn.close()
        return True

    def update_user(self, id, key):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        try:
            c.execute(
                '''UPDATE login SET key="{}" WHERE id ="{}"'''.format(key, id))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        conn.commit()
        conn.close()
        return True

    def new_user(self, row):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        try:
            c.execute(
                '''INSERT INTO login (id,key) VALUES ("{}","{}")'''.format(row[0], row[1]))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        conn.commit()
        conn.close()
        return True

    def default_user_revie(self, key):
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        try:
            c.execute(
                '''UPDATE login SET key="{}",hide=0 WHERE id ="abcd1234"'''.format(key))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        conn.commit()
        conn.close()
        return True


class DB_login_verify:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.result = [0, 0]
        conn = sqlite3.connect('settings.db')
        c = conn.cursor()
        login_data = c.execute('''SELECT id,key FROM login;''')
        for row in login_data:
            if row[0] == self.username:
                self.result[0] = 1
            if row[1] == self.password:
                self.result[1] = 1
        conn.close()

    def verify(self):
        verify_result = self.result
        self.result = [0, 0]
        return verify_result


class DB_checkout:
    def __init__(self) -> None:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        conn.commit()
        conn.close()
        pass

    def sell_history_insert(self, data):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO sell_history
            (id,turnover,volume,cost,catagory,batch,storage,member)
            VALUES
            ("{date}","{turnover}","{volume}","{cost}","{catagory}","{batch}","{storage}","{member}")
            '''.format(date=data[0], turnover=data[1], volume=data[2], cost=data[3], catagory=data[4], batch=data[5], storage=data[6], member=data[7]))
        except Exception as e:
            return e
        conn.commit()
        conn.close()
        return True

    def get_available_catagory(self):
        conn = sqlite3.connect('data.db')
        catagory_list = []
        c = conn.cursor()
        t = c.execute("SELECT catagory FROM stock")
        for row in t:
            catagory_list.append(row[0])
        catagory_list = list(set(catagory_list))
        catagory_list.sort()
        conn.commit()
        conn.close()
        return catagory_list

    def catagory_batch_matching(self, catagory):
        conn = sqlite3.connect('data.db')
        batch_list = []
        c = conn.cursor()
        t = c.execute(
            "SELECT id,catagory,batch,price,quantity,selling_price,storage,(strftime('%s',expire)-strftime('%s',datetime('now','localtime'))) FROM stock WHERE catagory='{}' ORDER BY strftime('%s',expire)-strftime('%s',datetime('now','localtime'))".format(catagory))
        for row in t:
            row = list(row)
            row[3] = str(format(float(row[3])/float(row[4]), '.2f'))
            row[-1] = str(format(float(row[-1])/86400, '.2f'))
            batch_list.append(row)
        conn.commit()
        conn.close()
        return batch_list

    def order_data_load(self):
        conn = sqlite3.connect('data.db')
        order_list = []
        c = conn.cursor()
        t = c.execute(
            '''SELECT 
            id,customer,number,catagory,quantity,booking_date,remarks,state
            FROM orders WHERE state = 1 ORDER BY booking_date ASC''')
        for row in t:
            order_list.append(list(row))
        conn.commit()
        conn.close()
        return order_list

    def member_load(self):
        member_data_array = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT number,name,wallet,points,reg_date,date(reg_date) FROM member;''')
        for row in t:
            temp = list(row)
            temp.pop(4)
            member_data_array.append(temp)
        conn.commit()
        conn.close()
        temp = member_data_array
        member_data_array = []
        return temp

    def get_stock_storage(self, key):
        conn = sqlite3.connect('data.db')
        storage = False
        c = conn.cursor()
        t = c.execute("SELECT storage FROM stock WHERE id ='{}'".format(key))
        for row in t:
            storage = row[0]
        conn.commit()
        conn.close()
        return storage

    def is_in_stock(self, key):
        temp = []
        conn = sqlite3.connect('data.db')
        catagory_list = []
        c = conn.cursor()
        t = c.execute("SELECT id FROM stock WHERE id ='{}'".format(key))
        for row in t:
            temp.append(row[0])
        conn.commit()
        conn.close()
        if len(temp) == 0:
            return False
        else:
            return True

    def stock_minus(self, key, value):
        old_quantity = False
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute("SELECT quantity FROM stock WHERE id ='{}'".format(key))
        for row in t:
            old_quantity = float(row[0])
        if old_quantity == False:
            return False
        new_quantity = format(old_quantity-float(value), '.2f')
        if float(new_quantity)-0.0 >= 0.001:
            try:
                t = c.execute("UPDATE stock SET quantity='{quantity}' WHERE id='{id}'".format(
                    quantity=str(new_quantity), id=key))
            except Exception as e:
                conn.commit()
                conn.close()
                return e
        else:
            try:
                t = c.execute("DELETE FROM stock WHERE id='{id}'".format(
                    quantity=str(new_quantity), id=key))
            except Exception as e:
                conn.commit()
                conn.close()
                return e
        conn.commit()
        conn.close()
        return True

    def is_in_member(self, key):
        temp = []
        conn = sqlite3.connect('data.db')
        catagory_list = []
        c = conn.cursor()
        t = c.execute(
            "SELECT number FROM member WHERE number ='{}'".format(key))
        for row in t:
            temp.append(row[0])
        conn.commit()
        conn.close()
        if len(temp) == 0:
            return False
        else:
            return True

    def member_update(self, key, value=0, zero=False):
        old_wallet = False
        old_points = False
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            "SELECT wallet,points FROM member WHERE number ='{}'".format(key))
        for row in t:
            old_wallet = float(row[0])
            old_points = int(row[1])
        if old_wallet == False:
            return False
        if zero == False:
            new_wallet = format(old_wallet-float(value), '.2f')
            new_points = old_points+int(value)
        elif zero == True:
            new_wallet = 0.00
            new_points = old_points+int(old_wallet)
        try:
            t = c.execute("UPDATE member SET wallet='{wallet}',points='{points}' WHERE number='{number}'".format(
                wallet=new_wallet, points=new_points, number=key))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        conn.commit()
        conn.close()
        return True

    def order_state_update(self, key, mode=0):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute(
                '''UPDATE orders SET state={modeN} WHERE id="{keyN}";'''.format(keyN=key, modeN=mode))
            conn.commit()
        except Exception as error:
            conn.commit()
            conn.close()
            return error
        conn.commit()
        conn.close()
        return True


class DB_member:
    def __init__(self) -> None:
        self.member_data_array = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        conn.commit()
        conn.close()
        pass

    def data_load(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT number,name,wallet,points,reg_date,date(reg_date) FROM member;''')
        for row in t:
            temp = list(row)
            temp.pop(4)
            self.member_data_array.append(temp)
        conn.commit()
        conn.close()
        temp = self.member_data_array
        self.member_data_array = []
        return temp

    def data_insert(self, data):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('SELECT name FROM member;')
        for row in t:
            if data[0] == row[0]:
                return '错误！同一电话号码只能注册一名会员'
        try:
            c.execute(
                'INSERT INTO member (number,name,wallet,points,reg_date) VALUES ("{number}","{name}","{wallet}","{points}","{reg_date}")'.format(
                    number=data[0], name=data[1], wallet=data[2], points=data[3], reg_date=data[4]))
            conn.commit()
        except Exception as e:
            return repr(e)
        conn.close()
        return True

    def data_delete(self, key_list):
        error_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        for i in key_list:
            try:
                c.execute("DELETE FROM member WHERE number='{}'".format(i))
                conn.commit()
            except Exception as del_error:
                error_list.append([i, repr(del_error)])
        conn.close()
        if error_list != []:
            return error_list
        return True

    def date_update(self, data_list):
        error_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        for row in data_list:
            try:
                c.execute(
                    "UPDATE member SET name='{}',wallet='{}',points='{}',reg_date='{}' WHERE number='{}'".format(
                        row[1], row[2], row[3], row[4], row[0]))
                conn.commit()
            except Exception as error:
                error_list.append([row[0], repr(error)])
        conn.close()
        if error_list == []:
            return True
        else:
            return error_list


class DB_stock:
    def __init__(self) -> None:
        self.stock_data_array = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        conn.commit()
        conn.close()
        pass

    def data_load(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT 
            id,catagory,batch,price,quantity,selling_price,date,(strftime('%s',expire)-strftime('%s',datetime('now','localtime'))),storage 
            FROM stock;''')
        for row in t:
            self.stock_data_array.append(list(row))
        conn.commit()
        conn.close()
        temp = self.stock_data_array
        self.stock_data_array = []
        return temp

    def batch_check(self, catagory):
        if catagory == '':
            return []
        temp = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT batch FROM stock WHERE catagory='{}';'''.format(catagory))
        for row in t:
            temp.append(row[0])
        conn.commit()
        conn.close()
        return temp

    def storage_check(self):
        temp = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT storage FROM stock;''')
        for row in t:
            temp.append(row[0])
        temp = list(set(temp))
        temp.sort()
        conn.commit()
        conn.close()
        return temp

    def stock_data_insert(self, data):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('SELECT id FROM stock;')
        for row in t:
            if data[0] == row[0]:
                return '错误，已有同一种类同一批次货物存在'
        try:
            c.execute(
                '''INSERT INTO stock 
                (id,catagory,batch,price,quantity,selling_price,date,expire,storage) 
                VALUES 
                ("{id}","{catagory}","{batch}","{price}","{quantity}","{selling_price}","{date}",
                datetime("{date}","+{hour} hour","+{day} day","+{month} month", "+{year} year"),"{storage}");'''.format(
                    id=data[0], catagory=data[1], batch=data[2], price=data[3],
                    quantity=data[4], selling_price=data[5], date=data[6],
                    hour=data[7][0], day=data[7][1], month=data[7][2], year=data[7][3], storage=data[8]
                ))
            c.execute(
                '''INSERT INTO purchase_history 
                (id,catagory,batch,price,quantity,selling_price,expire,storage) 
                VALUES 
                ("{id}","{catagory}","{batch}","{price}","{quantity}","{selling_price}",
                datetime("{date}","+{hour} hour","+{day} day","+{month} month", "+{year} year"),"{storage}");'''.format(
                    id=data[0]+'<<'+data[6], catagory=data[1], batch=data[2], price=data[3],
                    quantity=data[4], selling_price=data[5], date=data[6],
                    hour=data[7][0], day=data[7][1], month=data[7][2], year=data[7][3],
                    storage=data[8]
                ))
            conn.commit()
        except Exception as e:
            return repr(e)
        conn.close()
        return True

    def stock_data_delete(self, key_list):
        error_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        for i in key_list:
            try:
                c.execute("DELETE FROM stock WHERE id='{}'".format(i))
                conn.commit()
            except Exception as del_error:
                error_list.append([i, repr(del_error)])
        conn.close()
        if error_list != []:
            return error_list
        return True

    def stock_date_update(self, data_list):
        error_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        for row in data_list:
            try:
                c.execute(
                    '''UPDATE stock SET 
                    price="{price}",
                    quantity="{quantity}",
                    selling_price="{selling_price}",
                    date="{date}",
                    expire=datetime("now","localtime","+{hour} hour","+{day} day","+{month} month", "+{year} year"),
                    storage="{storage}"
                    WHERE id="{id}"
                '''.format(id=row[0], price=row[3],
                           quantity=row[4], selling_price=row[5], date=row[6],
                           hour=row[7][0], day=row[7][1], month=row[7][2], year=row[7][3], storage=row[8]
                           ))
                conn.commit()
            except Exception as error:
                error_list.append([row[0], repr(error)])
        conn.close()
        if error_list == []:
            return True
        else:
            return error_list

    def report_loss(self, data):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            t = c.execute(
                "DELETE FROM stock WHERE id='{id}'".format(id=data[3]+data[4]))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        try:
            c.execute('''INSERT INTO sell_history
            (id,turnover,volume,cost,catagory,batch,storage,member)
            VALUES
            ("{date}","{turnover}","{volume}","{cost}","{catagory}","{batch}","{storage}","{member}")
            '''.format(date=data[0], turnover=0, volume=data[1], cost=data[2], catagory=data[3], batch=data[4], storage=data[5], member='报损'))
        except Exception as e:
            conn.commit()
            conn.close()
            return e
        conn.commit()
        conn.close()
        return True


class DB_history:
    def __init__(self) -> None:
        self.purchase_history_data_array = []
        self.sell_history_data_array = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        conn.commit()
        conn.close()
        pass

    def purchase_data_load(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT 
            id,catagory,batch,price,quantity,selling_price,expire,storage 
            FROM purchase_history;''')
        for row in t:
            self.purchase_history_data_array.append(list(row))
        conn.commit()
        conn.close()
        temp = self.purchase_history_data_array
        self.purchase_history_data_array = []
        return temp

    def sell_data_load(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT 
            id,turnover,volume,cost,catagory,batch,storage,member
            FROM sell_history ORDER BY id DESC''')
        for row in t:
            self.sell_history_data_array.append(list(row))
        conn.commit()
        conn.close()
        temp = self.sell_history_data_array
        self.sell_history_data_array = []
        return temp


class DB_order:
    def __init__(self) -> None:
        self.order_data_array = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        conn.commit()
        conn.close()

    def order_data_load(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute(
            '''SELECT 
            id,customer,number,catagory,quantity,booking_date,remarks,state
            FROM orders WHERE state = 1 ORDER BY booking_date ASC''')
        for row in t:
            self.order_data_array.append(list(row))
        t = c.execute(
            '''SELECT 
            id,customer,number,catagory,quantity,booking_date,remarks,state
            FROM orders WHERE state != 1 ORDER BY state DESC,booking_date DESC''')
        for row in t:
            self.order_data_array.append(list(row))
        conn.commit()
        conn.close()
        temp = self.order_data_array
        self.order_data_array = []
        return temp

    def order_data_insert(self, data):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO orders
            (id,customer,number,catagory,quantity,booking_date,remarks,state)
            VALUES
            ("{id}","{customer}","{number}","{catagory}","{quantity}","{booking_date}","{remarks}",{state})
            '''.format(id=data[0], customer=data[1], number=data[2],
                       catagory=data[3], quantity=data[4], booking_date=data[5],
                       remarks=data[6], state=data[7]))
        except Exception as e:
            return e
        conn.commit()
        conn.close()
        return True

    def order_data_update(self, row):
        error_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute(
                '''UPDATE orders SET 
                customer="{customer}",number="{number}",
                catagory="{catagory}",quantity="{quantity}",
                booking_date="{booking_date}",
                remarks="{remarks}",state={state}
                WHERE id="{id}";'''.format(
                    id=row[0], customer=row[1], number=row[2],
                    catagory=row[3], quantity=row[4], booking_date=row[5],
                    remarks=row[6], state=row[7]))
            conn.commit()
        except Exception as error:
            return str(error)
        conn.close()
        return True

    def order_data_delete(self, key_list):
        error_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        for i in key_list:
            try:
                c.execute("DELETE FROM orders WHERE id='{}'".format(i))
                conn.commit()
            except Exception as del_error:
                error_list.append([i, repr(del_error)])
        conn.close()
        if error_list != []:
            return error_list
        return True

    def check_member(self):
        member_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('''SELECT name FROM member''')
        for row in t:
            member_list.append(row[0])
        conn.commit()
        conn.close()
        member_list = list(set(member_list))
        return member_list

    def check_number(self):
        number_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('''SELECT number FROM member''')
        for row in t:
            number_list.append(row[0])
        conn.commit()
        conn.close()
        return number_list

    def check_catagory(self):
        catagory_list = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('''SELECT catagory FROM purchase_history''')
        for row in t:
            catagory_list.append(row[0])
        conn.commit()
        conn.close()
        catagory_list = list(set(catagory_list))
        return catagory_list

    def auto_matching(self, mode, key):
        result = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        if mode == 'member':
            t = c.execute(
                "SELECT number FROM member WHERE name='{Key}'".format(Key=key))
            for row in t:
                result.append(row[0])
        elif mode == 'number':
            t = c.execute(
                "SELECT name FROM member WHERE number='{Key}'".format(Key=key))
            for row in t:
                result.append(row[0])
        conn.commit()
        conn.close()
        if len(result) != 1:
            return []
        else:
            return result

    def expired_order_state_update(self, mode):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute(
                '''UPDATE orders SET state={} WHERE booking_date < date('now','localtime') and state =1;'''.format(mode))
            conn.commit()
        except Exception as error:
            return str(error)
        conn.close()
        return True

    def order_expired_delete(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            c.execute(
                "DELETE FROM orders WHERE booking_date < date('now','localtime') and state =1;")
            conn.commit()
        except Exception as del_error:
            return del_error
        conn.close()
        return True

    def order_state_update(self, key_list, mode):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        error_list = []
        for i in key_list:
            try:
                c.execute(
                    '''UPDATE orders SET state={modeN} WHERE id="{key}";'''.format(key=i, modeN=mode))
                conn.commit()
            except Exception as error:
                error_list.append(repr(error))
        conn.commit()
        conn.close()
        if error_list == []:
            return True
        else:
            return error_list


class DB_statistics:
    def __init__(self) -> None:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        conn.commit()
        conn.close()

    def get_turnover_sum(self, start_time_stamp, end_time_stamp):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('''
        select sum(turnover) FROM sell_history WHERE id BETWEEN {} and {}
        '''.format(start_time_stamp, end_time_stamp))
        for row in t:
            conn.commit()
            conn.close()
            if row[0] == None:
                return 0.00
            return float(row[0])

    def get_cost_sum(self, start_time_stamp, end_time_stamp):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        t = c.execute('''
        select sum(cost) FROM sell_history WHERE id BETWEEN {} and {}
        '''.format(start_time_stamp, end_time_stamp))
        for row in t:
            conn.commit()
            conn.close()
            if row[0] == None:
                return 0.00
            return float(row[0])

    def gross_profit(self, start_time_stamp, end_time_stamp):
        income = self.get_turnover_sum(start_time_stamp, end_time_stamp)
        cost = self.get_cost_sum(start_time_stamp, end_time_stamp)
        return income-cost

    def gross_profit_rate(self, start_time_stamp, end_time_stamp):
        income = self.get_turnover_sum(start_time_stamp, end_time_stamp)
        cost = self.get_cost_sum(start_time_stamp, end_time_stamp)
        if income-0.00 <= 0.001:
            return '0%'
        return str(float(format((income-cost)/income, '.4f'))*100)+'%'

    def get_catagory_rank(self, column_name, group_by_column, start_time_stamp, end_time_stamp):
        temp = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("select {},sum({}) from sell_history WHERE id BETWEEN {} and {} group by {}  order by sum({}) desc" .format(
            group_by_column,  column_name, start_time_stamp, end_time_stamp, group_by_column, column_name))
        result = c.fetchall()
        conn.close()
        for row in result:
            temp.append(row[0]+':'+str(row[1]))
        return temp

    def get_profit_rate_rank(self, start_time_stamp, end_time_stamp):
        temp = []
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("select catagory,(sum(turnover)-sum(cost))/sum(turnover) from sell_history WHERE id BETWEEN {} and {} group by catagory order by (sum(turnover)-sum(cost))/sum(turnover) desc".format(start_time_stamp, end_time_stamp))
        result = c.fetchall()
        conn.close()
        for row in result:
            temp_row = row[0]
            if row[1] != None:
                temp_row += ':'+"{:.2%}" .format(row[1])
            else:
                temp_row += ':无利润'
            temp.append(temp_row)
        return temp
