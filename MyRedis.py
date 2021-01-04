import redis
import PySimpleGUI as sg


class RedisOp(object):
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        self.redis_pool = redis.ConnectionPool(host=host, port=int(port), db=int(db), decode_responses=True) # 这里使用线程池，方便后期维护
    def change_db(self):
        pass # 更换数据库，目前还不知道咋操作

    def get_all_key(self):
        self.r = redis.Redis(connection_pool=self.redis_pool)
        return self.r.keys()


class OperationUI(object):  # 登录成功进入操作界面
    def __init__(self, host, port, db):
        self.__redis_operation = RedisOp(host=host, port=port, db=db)  # 天然的单例模式
        self.operation_layout = [
            [
                sg.Text("Host:" + host + "    Port:" + port + "    Current DB:"),
                sg.InputCombo(values=([i for i in range(17)]), default_value=(db,), key='-SelectDB-', size=(15, 1))
            ],
            [
                sg.Listbox(values=(self.__redis_operation.get_all_key()), key='-SelectKey-', default_values=(0,), size=(48, 15))
            ],
            [sg.Button("Add", size=(15, 1)), sg.Button("Delete", size=(15, 1)),
             sg.Button("Cancel", size=(15, 1))
             ]]
        self.window = sg.Window('MyRedis', self.operation_layout)
        self.operation()

    def operation(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return
            if event == 'Add':
                sg.popup('V1.0\nThank you for using our product')  # 弹出的内容
                # 以上是从图形界面中读取的信息
            if event == 'Delete':
                host = values['-Host-']
                port = values['-Port-']
                db = values['-DB-']
                break
        self.window.close()


class LoginUI(object):
    def __init__(self):  # 在构造器中构造界面
        # sg.theme_previewer()  # 展示所有可用主题
        self.login_layout = [[sg.Text('Welcome to RedisUI Demo'), sg.Text(size=(15, 1), key='-Welcome-')],  # 登录界面
                             [sg.Text("Input your Host", size=(14, 1)),
                              sg.InputText(default_text='127.0.0.1', key='-Host-')],
                             [sg.Text("Input your Port", size=(14, 1)),
                              sg.InputText(default_text='6379', key='-Port-')],
                             [sg.Text("Select your DB number", size=(18, 1)),
                              sg.Listbox(values=([i for i in range(17)]), default_values=(0,), key='-DB-',
                                         size=(15, 3))],
                             [sg.Button("Connect", size=(15, 1)), sg.Button("Cancel", size=(15, 1)),
                              sg.Button("About", size=(15, 1))]]
        self.window = sg.Window('MyRedis', self.login_layout)
        self.login()

    def login(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return
            if event == 'About':
                sg.popup('V1.0\nThank you for using our product')  # 弹出的内容
            if event == 'Connect':
                host = values['-Host-']
                port = values['-Port-']
                db = values['-DB-']
                break
        self.window.close()
        OperationUI(host=host, port=port, db=db[0])


if __name__ == '__main__':
    LoginUI()
