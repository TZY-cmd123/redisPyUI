import redis
import PySimpleGUI as sg


class LoginUI(object):
    def __init__(self):  # 在构造器中构造界面
        # sg.theme_previewer()  # 展示所有可用主题
        sg.theme('DarkAmber')
        self.login_layout = [[sg.Text('Welcome to RedisUI Demo'), sg.Text(size=(15, 1), key='-Welcome-')], # 登录界面
        [sg.Text("Input your Host",size=(14,1)),sg.InputText(default_text='127.0.0.1',key='-Host-')],
        [sg.Text("Input your Port",size=(14,1)),sg.InputText(default_text='6379',key='-Port-')],
        [sg.Text("Select your DB number",size=(18,1)),sg.Listbox(values=([i for i in range(17)]), key='-DB-', size=(15, 3))],
        [sg.Button("Connect"), sg.Button("Cancel")]]
        self.window = sg.Window('MyRedis', self.login_layout)
        self.login()

    def login(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            # 以上是从图形界面中读取的信息
            if event == 'Connect':
                host=values['-Host-']
                port=values['-Port-']
                db=values['-DB-']
        self.window.close()  # 关闭窗口


if __name__ == '__main__':
    LoginUI()
