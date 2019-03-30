import tkinter as Tk
import tkinter.ttk as Ttk
import Logger
from Defines import STANDARD_RETURN

#Tk.Frameクラスを継承
class Amount(Tk.Frame):
    def __init__(self):
        pass

    # 閉じるボタンが押されたら失敗を返却
    def __on_closing(self):
        self.master.destroy()
        self.result = STANDARD_RETURN.NOT_OK

    #OKボタンが押されたときに実行される
    #テキストボックスに入力されたパスワードを変数に保存して閉じる
    def __pressed_ok(self, event=None):
        self.Amount = self.Entry_amount.get()
        self.master.destroy()

    def __create_widgets(self):
        self.master.geometry()

        #pack()：ウィジェットをウィンドウに配置する
        #padx：横幅　pady：縦幅
        self.pack(padx=5, pady=5)
        #resizable：サイズ変更の許可
        #横,縦の順番で、0は禁止、１は許可
        self.master.resizable(0, 0)
        self.master.title('送金額入力画面')

        # ボタンのスタイルを変更
        style = Ttk.Style()
        style.configure('TButton', font=('Meiryo UI', 8))

        #フレームの作成
        text_frame = Ttk.Frame(self)
        text_frame.grid(column=0, row=0, sticky='w')
        input_frame = Ttk.Frame(self)
        input_frame.grid(column=0, row=1, sticky='w')

        self.label_1 = Tk.Label(text_frame, text=u'送金額を入力してください。', font=("Meiryo UI", 11))
        self.label_1.pack(side='left', anchor='w')

        #Enty：1行入力のテキストボックス 第1引数は配置するFrameオブジェクト
        self.Entry_amount = Tk.Entry(input_frame, justify='right', font=("Meiryo UI", 8))
        self.Entry_amount.pack(side='left', padx=5, expand=1, fill='x')
        self.Entry_amount.focus_set()
        self.Entry_amount.bind('<Return>', self.__pressed_ok)

        self.label_2 = Tk.Label(input_frame, text=u'VIPS', width=5, font=("Meiryo UI", 8), anchor="w")
        self.label_2.pack(side='left')

        #OKボタン　押されたらプライベート関数__pressed_okを実行する
        self.Button_ok = Tk.Button(input_frame, text='OK', command=self.__pressed_ok, width=7)
        self.Button_ok.pack(side='left')

    def input(self):
        #tkinterのインスタンスでありメインウィンドウ
        self.master = Tk.Tk()
        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

        self.result = STANDARD_RETURN.OK
        # ウィジェット作成
        self.__create_widgets()
        #閉じるボタンが押されたときの処理
        self.master.protocol("WM_DELETE_WINDOW", self.__on_closing)
        #GUIを表示
        self.mainloop()
        #閉じられていたらFalseを返す
        if self.result == STANDARD_RETURN.NOT_OK:
            return self.result,0
        #入力された金額を変数に保存
        amount = self.Amount
        #数値以外と0以下と18桁以上はFalseを返す
        try:
            if float(amount) <= 0 or len(str(amount)) > 18:
                self.result = STANDARD_RETURN.NOT_OK
                Logger.Logging("message:{0}".format("input value of amount is invalid."))
                return self.result,0
        except ValueError:
            self.result = STANDARD_RETURN.NOT_OK
            Logger.Logging("message:{0}".format("input value of amount is invalid."))
            return self.result,0
        else:
            return self.result,amount
