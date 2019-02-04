import tkinter as Tk
import json
import ExternalFile
from Defines import STANDARD_RETURN

#Tk.Frameクラスを継承
class Confirm(Tk.Frame):
    def __init__(self):
        #tkinterのインスタンスでありメインウィンドウ
        self.master = Tk.Tk()
        #BookeanVar()はTrueかFalseの2択の特殊な変数の型
        #次回以降確認画面を出すかどうかのチェックボックス用
        self.IsConfirm = Tk.BooleanVar()
        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

    #tkinterではGUIの部品のことをウィジェットという
    #ウィジェットを作成するプライベート関数
    #パスワード入力画面を表示する
    def __create_widgets(self):

        #ウィンドウの幅
        width = 400
        #ウィンドウの高さ
        height = 150
        #x座標をスクリーンの長さの半分 - ウィンドウの幅の半分に設定
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        #y座標をスクリーンの長さの半分 - ウィンドウの高さの半分に設定
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width,height, x, y))

        #pack()：ウィジェットをウィンドウに配置する
        #padx：横幅　pady：縦幅jjj
        self.pack(padx=20, pady=20)
        #resizable：サイズ変更の許可
        #横,縦の順番で、0は禁止、１は許可
        self.master.resizable(0, 0)
        self.master.title('送金確認画面')

        self.label_1 = Tk.Label(self,text='送金します。よろしいですか？',font=8)
        #OKボタン　押されたらプライベート関数__pressed_okを実行する
        self.Button_ok = Tk.Button(self, text='OK', command=self.__pressed_ok,bd=3,font=4,width=5)
        #キャンセルボタン　押されたらプライベート関数__pressed_cancelを実行する
        self.Button_cancel = Tk.Button(self, text='キャンセル', command=self.__pressed_cancel,bd=3,font=4,width=10)
        #次回以降確認画面を出すかどうかのチェックボックス　onでTrue offでFalse
        self.CheckButton_isConfirm = Tk.Checkbutton(self, text=u'今後、このメッセージを表示しない', variable=self.IsConfirm)

        #grid()：テキストボックスをグリッド状に配置
        #上の４つのウィジェットをそれぞれ配置していく
        #ラベルは1行1列目　テキストボックスは2行1列目　OKボタンは2行2列目　チェックボックスは3行1列目
        self.label_1.grid(column=0,row=0)
        self.Button_ok.grid(column=0, row=1,padx=10,pady=10)
        self.Button_cancel.grid(column=1, row=1,padx=10,pady=10)
        self.CheckButton_isConfirm.grid(column=0, row=2)

    #OKボタンが押されたときに実行される
    #成功を返却して閉じる
    # 「今後、このメッセージを表示しない」にチェックしていれば記憶
    def __pressed_ok(self):
        if self.IsConfirm.get():
            self.save()
        self.master.destroy()
        self.result = True

    #キャンセルボタンが押されたときに実行される
    #失敗を返却して閉じる
    def __pressed_cancel(self):
        self.master.destroy()
        self.result =  False

    #次回以降確認しない情報を記憶する
    def save(self):
        self.external_file.save('isconfirmflag', 'False')

    def is_sending(self):
        #インスタンスを作成すると自動的にファイルが作られる
        self.external_file = ExternalFile.ExternalFile('VipsSender.property')
        # 次回以降確認しない情報が読み出せればTrueを返却して終了
        result = self.external_file.get('isconfirmflag')
        if result[0] == 0 and result[1] == 'False':
            return True
        else:
            #デフォルトは確認画面を出す
            self.external_file.save('isconfirmflag', 'True')

        # ウィジェット作成
        self.__create_widgets()
        #GUIを表示
        self.mainloop()

        return self.result