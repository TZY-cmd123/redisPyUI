import redis
import PySimpleGUI as sg


class RedisOp(object):  # 逻辑底层操作
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        self.redis_pool = redis.ConnectionPool(host=host, port=int(port), db=int(db), decode_responses=True)  #
        # 这里使用线程池，方便后期维护
        self.r = redis.Redis(connection_pool=self.redis_pool)

    def change_db(self):
        pass  # 更换数据库，目前还不知道咋操作

    def get_all_key(self):  # 获得所有的键
        return self.r.keys()

    def get_type_key(self, key):  # 获得键的对应的值的类型
        return str(self.r.type(key))

    def get_ttl_key(self, key):  # 获得过期时间
        if self.r.ttl(key) is None:
            return '∞'
        return str(self.r.ttl(key))

    def get_value_key(self, key):  # 获得对应的值
        temp_type = self.get_type_key(key)
        if temp_type == "string":
            return str(self.r.get(key))
        elif temp_type == 'set':
            return str(self.r.smembers(key))
        elif temp_type == 'list':
            return str(self.r.lrange(key, 0, -1))
        elif temp_type == 'hash':
            return str(self.r.hgetall(key))

    def del_key(self, key):  # 根据键删除对应的键值对
        self.r.expire(key, 0)  # 直接把过期时间设为0秒

    def get_show_key(self):
        show_list = []
        for i in self.get_all_key():
            show_list.append([i, self.get_type_key(i), self.get_ttl_key(i), self.get_value_key(i)])
        return show_list


class DetailUI(object):  # 新增或者检查
    def __init__(self, redisOp, key=""):
        self.__redis_operation = redisOp  # 天然的单例模式


class OperationUI(object):  # 登录成功进入操作界面
    def __init__(self, host, port, db):
        self.__redis_operation = RedisOp(host=host, port=port, db=db)  # 天然的单例模式
        self.detective_connect()
        self.show_list = self.__redis_operation.get_show_key()
        self.operation_layout = [
            [
                sg.Text("Host:" + host + "    Port:" + port + "    Current DB:"),
                sg.InputCombo(values=([i for i in range(17)]), default_value=(db,), key='-SelectDB-', size=(15, 1))
            ],
            [sg.Table(headings=['Key', 'Type', 'Time to live', 'Value'],
                      values=self.show_list, key='-SelectKey-', size=(25, 10), def_col_width=10,
                      auto_size_columns=False)
             ],
            [
                sg.Button("Check", size=(10, 1)), sg.Button("Add", size=(10, 1)),
                sg.Button("Delete", size=(10, 1)), sg.Button("Cancel", size=(10, 1))
            ]
        ]
        self.window = sg.Window('MyRedis', self.operation_layout)
        self.operation()

    def detective_connect(self):  # 检查链接成功与否
        try:
            self.__redis_operation.r.ping()
        except redis.exceptions.ConnectionError:  # 链接失败
            LoginUI(text="Error Connection")
            return

    def operation(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return
            if event == 'Check':
                if values['-SelectKey-']:
                    key = self.show_list[values['-SelectKey-'][0]][0]
                    self.window.close()
                    DetailUI(self.__redis_operation, key)
            if event == 'Add':
                self.window.close()
                DetailUI(self.__redis_operation)
            if event == 'Delete':
                if values['-SelectKey-']:
                    key = self.show_list[values['-SelectKey-'][0]][0]
                    self.__redis_operation.del_key(key)
                    self.window.close()
                    OperationUI(host=self.__redis_operation.host, port=self.__redis_operation.port,
                                db=self.__redis_operation.db)


# 登录界面,已完成
class LoginUI(object):
    def __init__(self, text=""):  # 在构造器中构造界面
        # sg.theme_previewer()  # 展示所有可用主题
        self.login_layout = [[sg.Text('Welcome to RedisUI Demo'), sg.Text(size=(15, 1), key='-Welcome-'),
                              sg.Text(text, text_color="RED")],  # 登录界面
                             [sg.Text("Input your Host", size=(14, 1)),
                              sg.InputText(default_text='127.0.0.1', key='-Host-')],
                             [sg.Text("Input your Port", size=(14, 1)),
                              sg.InputText(default_text='6379', key='-Port-')],
                             [sg.Text("Select your DB number", size=(18, 1)),
                              sg.Listbox(values=([i for i in range(17)]), default_values=(0,), key='-DB-',
                                         size=(15, 4))],
                             [sg.Button("Connect", size=(15, 1)), sg.Button("Cancel", size=(15, 1)),
                              sg.Button("About", size=(15, 1))]]
        self.window = sg.Window('MyRedis', self.login_layout)
        self.login()

    def login(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return
            elif event == 'About':
                sg.popup('V1.0\nThank you for using our product')  # 弹出的内容
            elif event == 'Connect':
                host = values['-Host-']
                port = values['-Port-']
                db = values['-DB-']
                break
        self.window.close()
        OperationUI(host=host, port=port, db=db[0])


if __name__ == '__main__':
    LoginUI()
