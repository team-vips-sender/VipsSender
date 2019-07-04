import tkinter as Tk
import tkinter.ttk as Ttk
from Defines import STANDARD_RETURN
from Defines import EXTERNAL_FILE
import os

base = os.path.dirname(os.path.abspath(__file__))

#Tk.Frameクラスを継承
class MessageWindow(Tk.Frame):
    def __init__(self):
        pass

    def __create_widgets(self, message):
        self.master.geometry()

        #pack()：ウィジェットをウィンドウに配置する
        #padx：横幅　pady：縦幅
        self.pack(padx=5, pady=5)
        #resizable：サイズ変更の許可
        #横,縦の順番で、0は禁止、１は許可
        self.master.resizable(0, 0)
        self.master.title('Message')

        # ボタンのスタイルを変更
        style = Ttk.Style()
        style.configure('TButton', font=('Meiryo UI', 8))

        #フレームの作成
        text_frame = Ttk.Frame(self)
        text_frame.pack(fill='none', side='top')
        input_frame = Ttk.Frame(self)
        input_frame.pack(side='top')
        
        self.label_1 = Ttk.Label(text_frame, text=message, font=("Meiryo UI", 10))
        self.label_1.pack(side='top')
        
        #OKボタン 押されたらプライベート関数__on_closingを実行する
        self.Button_ok = Ttk.Button(input_frame, text='OK', command=self.__on_closing, width=7)
        self.Button_ok.pack(side='top')


    def __on_closing(self):
        self.master.destroy()

    def display(self, message):
        self.master = Tk.Tk()

        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

        # ウィジェット作成
        self.__create_widgets(message)
        # 前面に配置
        self.master.attributes("-topmost", True)
        # アイコンをVIPSのロゴに変更
        iconfile = base + '/vipstarcoin.ico'
        self.master.iconbitmap(default=iconfile)

        #閉じるボタンが押されたときの処理
        self.master.protocol("WM_DELETE_WINDOW", self.__on_closing)
        #GUIを表示
        self.mainloop()

        return


def display( message ):
    mw = MessageWindow()
    mw.display(message)
    
    return
