import PySimpleGUI as sg # 这个包堪称懦夫救星
layout = [[sg.Text('懦夫救星桌面')],
                 [sg.InputText()],
                [sg.Checkbox('121')],
                 [sg.Submit(), sg.Cancel()]]
#以上是图形界面

window = sg.Window('Window Title', layout)
event, values = window.read()
#以上是从图形界面中读取的信息

window.close()

text_input = values
sg.popup('You entered', text_input)#弹出的内容