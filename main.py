import tkinter as tk
import autopy, os, sys, time, threading, platform
import const, favicon

#Variavel global para indicar o stop da thread
stop = False

#Funcao para dar o start no mouse
def btn_start_click(lbl_run):
    global stop
    stop = False
    #start na thread apenas se a label running estiver setado
    if lbl_run['text'] == '':
        t = threading.Thread(target=start_move, args=(lbl_run, ))
        t.start()

#Funcao para dar o stop no mouse
def btn_stop_click(lbl_run):
    global stop
    stop = True
    lbl_run['text'] = ''

#Funcao para iniciar o mouse
def start_move(lbl_run):
    global stop
    lbl_run['text'] = const.LBL_RUNNING
    while True:
        if stop:
            break
        time.sleep(2)
        if stop:
            break
        x = window.winfo_x() + 80
        y = window.winfo_y() + 35
        autopy.mouse.smooth_move(x,y)
        autopy.mouse.click()
        if stop:
            break
        time.sleep(2)
        if stop:
            break
        x = window.winfo_x() + 180
        y = window.winfo_y() + 35
        autopy.mouse.smooth_move(x,y)
        autopy.mouse.click()

#Funcao para criar e exibir o popup
def popup(title, msg):
    x_win_pos = window.winfo_x()
    y_win_pos = window.winfo_y()
    about = tk.Toplevel(window)
    about.title(title)
    about.geometry('+%d+%d' % (x_win_pos+20, y_win_pos+40))
    about.resizable(0, 0)
    about.attributes('-topmost', True)
    frame = tk.Frame(about)
    frame.grid()
    msg_body_1 = tk.Label(frame, text=msg, font=('Arial', 8))
    msg_body_1.grid(row=0, column=0, padx=50, pady=5, sticky=tk.N)
    ok_btn = tk.Button(frame, text=const.BTN_TEXT_OK, command=about.destroy, width=10)
    ok_btn.grid(row=1, column=0, padx=50, pady=5)
    ok_btn.focus()

#Funcao para sair da aplicacao
def quit_app():
    global stop
    stop = True
    sys.exit()

#Funcao para criar e configurar o menu    
def config_menu(win):
    #criar o menu
    menu = tk.Menu(win)

    #criar o menu File
    file_item = tk.Menu(menu, tearoff=0)
    file_item.add_command(label=const.MENU_EXIT, command=quit_app)
    menu.add_cascade(label=const.MENU_FILE, menu=file_item)

    #criar o menu Help
    about_item = tk.Menu(menu, tearoff=0)
    about_item.add_command(label=const.MENU_ABOUT, command=lambda:popup(const.POPUP_ABOUT_TITLE, const.POPUP_ABOUT_MSG))
    menu.add_cascade(label=const.MENU_HELP, menu=about_item)
    return menu

#Funcao principal para montar todos os componentes do programa na tela
def config_components(win):
    
    #label Frame para os comandos
    labelframe = tk.LabelFrame(win, text=const.LF_COMMANDS)
    labelframe.pack(fill=tk.BOTH, expand=tk.YES)
    labelframe.grid_rowconfigure(0, weight=0)
    labelframe.grid_columnconfigure(0, weight=1)

    #botao para iniciar o mouse
    btn_start = tk.Button(labelframe, text=const.BTN_TEXT_START, height=1, command= lambda:btn_start_click(lbl_run))
    btn_start.grid(column=0, row=0, padx=12, pady=5, sticky=tk.NSEW)
    
    #botao para parar o mouse
    btn_start = tk.Button(labelframe, text=const.BTN_TEXT_STOP, height=1, command= lambda:btn_stop_click(lbl_run))
    btn_start.grid(column=0, row=1, padx=12, pady=5, sticky=tk.NSEW)

    #label para indicar a execucao do mouse
    lbl_run = tk.Label(win, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    lbl_run.pack(side=tk.BOTTOM, fill=tk.X)

#configurar e executar a janela principal
window = tk.Tk()
window.title(const.MAIN_APP_NAME)
window.geometry(const.MAIN_APP_SIZE)
#nao permitir redimensionar a janela
window.resizable(0, 0)
window.config(menu=config_menu(window))
#janela da aplicacao sempre na frente em relacao aos outros programas
window.attributes('-topmost', True)
#adicionar o favicon apenas no Windows
if 'Windows' == platform.system():
    window.wm_iconbitmap(default=favicon.favicon)
#sobreescrever o atl+F4 e o X do windows e sempre passar pelo metodo quit_app
#com isso garante que sera fechado a thread caso esteja ativa
window.protocol("WM_DELETE_WINDOW", quit_app)
os.remove(favicon.favicon)
config_components(window)
window.mainloop()