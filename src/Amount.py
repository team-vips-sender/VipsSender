import tkinter as Tk
import Logger
from Defines import STANDARD_RETURN

#Tk.Frameクラスを継承
class Amount(Tk.Frame):
    def __init__(self):
        #tkinterのインスタンスでありメインウィンドウ
        self.master = Tk.Tk()
        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

    # 閉じるボタンが押されたら失敗を返却
    def __on_closing(self):
        self.master.destroy()
        self.result = STANDARD_RETURN.NOT_OK

    #OKボタンが押されたときに実行される
    #テキストボックスに入力されたパスワードを変数に保存して閉じる
    def __pressed_ok(self):
        self.Amount = self.Entry_amount.get()
        self.master.destroy()

    def __create_widgets(self):

        #ウィンドウの幅
        width = 350
        #ウィンドウの高さ
        height = 130
        #x座標をスクリーンの長さの半分 - ウィンドウの幅の半分に設定
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        #y座標をスクリーンの長さの半分 - ウィンドウの高さの半分に設定
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width,height, x, y))

        #pack()：ウィジェットをウィンドウに配置する
        #padx：横幅　pady：縦幅
        self.pack(padx=20, pady=20)
        #resizable：サイズ変更の許可
        #横,縦の順番で、0は禁止、１は許可
        self.master.resizable(0, 0)
        self.master.title('送金額入力画面')

        self.label_1 = Tk.Label(self,text=u'送金額を入力してください。')
        #Enty：1行入力のテキストボックス 第1引数は配置するFrameオブジェクト
        self.Entry_amount = Tk.Entry(self, width= 20,font=8,relief='sunken',bd=3,justify='right')
        self.label_2 = Tk.Label(self,text=u'VIPS',font=4)
        #OKボタン　押されたらプライベート関数__pressed_okを実行する
        self.Button_ok = Tk.Button(self, text='OK', command=self.__pressed_ok,font=8,bd=3)

        #grid()：テキストボックスをグリッド状に配置
        #上の４つのウィジェットをそれぞれ配置していく
        #ラベル1は1行1列目　テキストボックスは2行1列目　ラベル2は2行2列目　OKボタンは2行3列目
        self.label_1.grid(column=0,row=0)
        self.Entry_amount.grid(column=0, row=1,pady=10)
        self.label_2.grid(column=1, row=1)
        self.Button_ok.grid(column=2, row=1,padx=10)

    def input(self):
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
