import PySimpleGUI as sg  # 这个包堪称懦夫救星

# sg.theme_previewer()  # 展示所有可用主题
sg.theme('DarkAmber')  # Keep things interesting for your users
layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15, 1), key='textKey')],
          [sg.Text('懦夫救星桌面')],
          [sg.Multiline("Multiline",key='MultType')],
          [sg.Listbox(values=(1,2,3,4,5,8,"ListBox"), key='Listbox',size=(15,5))],
          [sg.Radio("Radio", key='Radio', size=(15, 5),group_id=1)],
          [sg.Radio("Radio", key='Radio1', size=(15, 5), group_id=1)],  # 不同的Radio用相同的group_id代表
          [sg.Spin(values=(1,2,3,4,5,8,"Spin"),size=(15,1))],
          [sg.RealtimeButton(button_text="实时按钮",key="RealtimeButton")],  #点击时会返回当前所有的状态
          [sg.ProgressBar(10)], #进度条,应该暂时用不到
          [sg.InputCombo(values=('InputCombo1','InputCombo2','InputCombo'),size=(15,1))],
          [sg.InputText(key='inputKey')],  # 通过设置key方便之后访问
          [sg.Checkbox(text='我是选择按钮', key='checkKey')],
          [sg.Button("Commit"), sg.Button("Cancel"), sg.Button('Show')]]  # Button 中的标识符可在之后的event中用到
# 以上是图形界面
window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Cancel':
        break
    # 以上是从图形界面中读取的信息
    if event=='RealtimeButton':
        print(event, values)
    if event == 'Show':
        window['textKey'].update(values['inputKey'])  # 需要改变界面的组件时我们会使用这个update
    text_input = values['inputKey']
    check_input = values["checkKey"]
    if event == 'Commit':
        sg.popup('You entered', text_input + str(check_input))  # 弹出的内容

window.close()  # 关闭窗口

# 常用组件
# Text
# InputText
# Multiline
# InputCombo
# Listbox
# Radio
# Checkbox
# Spin
# Output
# SimpleButton
# RealtimeButton
# ReadFormButton
# ProgressBar
# Image
# Slider
# Column
