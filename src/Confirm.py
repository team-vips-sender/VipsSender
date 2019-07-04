import tkinter as Tk
import tkinter.ttk as Ttk
import ExternalFile
from Defines import STANDARD_RETURN
from Defines import EXTERNAL_FILE
import OsDepend
import os

base = os.path.dirname(os.path.abspath(__file__))

#Tk.Frameクラスを継承
class Confirm(Tk.Frame):
    def __init__(self):
        pass

    #tkinterではGUIの部品のことをウィジェットという
    #ウィジェットを作成するプライベート関数
    #パスワード入力画面を表示する
    def __create_widgets(self):
        self.master.geometry()

        #pack()：ウィジェットをウィンドウに配置する
        #padx：横幅　pady：縦幅
        self.pack(padx=5, pady=5)
        #resizable：サイズ変更の許可
        #横,縦の順番で、0は禁止、１は許可
        self.master.resizable(0, 0)
        self.master.title('送金確認画面')

        # ボタンのスタイルを変更
        style = Ttk.Style()
        style.configure('TButton', font=('Meiryo UI', 8))

        #フレームの作成
        main_frame = Ttk.Frame(self)
        main_frame.grid(column=0, row=0, sticky='w')
        redisplay_frame = Ttk.Frame(self)
        redisplay_frame.grid(column=0, row=1, sticky='w')

        self.label_1 = Ttk.Label(main_frame, text='送金します。よろしいですか？', font=("Meiryo UI", 11), width=25)
        self.label_1.pack(side='left', anchor='n')
        
        #OKボタン　押されたらプライベート関数__pressed_okを実行する
        self.Button_ok = Ttk.Button(main_frame, text='OK', command=self.__pressed_ok, width=7)
        self.Button_ok.pack(side='top')
        self.Button_ok.bind('<Return>', self.__pressed_ok)

        #キャンセルボタン　押されたらプライベート関数__pressed_cancelを実行する
        self.Button_cancel = Ttk.Button(main_frame, text='キャンセル', command=self.__pressed_cancel, width=7)
        self.Button_cancel.pack(side='top')

        #次回以降確認画面を出すかどうかのチェックボックス　onでTrue offでFalse
        self.CheckButton_isConfirm = Ttk.Checkbutton(redisplay_frame, text='今後、このメッセージを表示しない', variable=self.IsConfirm)
        self.CheckButton_isConfirm.pack(side='left')

    # 閉じるボタンが押されたら失敗を返却
    def __on_closing(self):
        self.master.destroy()
        self.result = STANDARD_RETURN.NOT_OK

    #OKボタンが押されたときに実行される
    #成功を返却して閉じる
    # 「今後、このメッセージを表示しない」にチェックしていれば記憶
    def __pressed_ok(self,event=None):
        if self.IsConfirm.get():
            self.save()
        self.master.destroy()
        self.result = STANDARD_RETURN.OK

    #キャンセルボタンが押されたときに実行される
    #失敗を返却して閉じる
    def __pressed_cancel(self):
        self.master.destroy()
        self.result = STANDARD_RETURN.NOT_OK

    #次回以降確認しない情報を記憶する
    def save(self):
        self.external_file.save('isconfirmflag', 'False')

    def is_sending(self):
        ret, user_path = OsDepend.get_user_path()
        if ret != STANDARD_RETURN.OK:
            return STANDARD_RETURN.NOT_OK

        #インスタンスを作成すると自動的にファイルが作られる
        self.external_file = ExternalFile.ExternalFile(user_path + EXTERNAL_FILE.PATH)
        # 次回以降確認しない情報が読み出せればTrueを返却して終了
        result = self.external_file.get('isconfirmflag')
        if result[0] == 0 and result[1] == 'False':
            return STANDARD_RETURN.OK
        else:
            #デフォルトは確認画面を出す
            self.external_file.save('isconfirmflag', 'True')

        #tkinterのインスタンスでありメインウィンドウ
        self.master = Tk.Tk()
        #BookeanVar()はTrueかFalseの2択の特殊な変数の型
        #次回以降確認画面を出すかどうかのチェックボックス用
        self.IsConfirm = Tk.BooleanVar()
        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

        # ウィジェット作成
        self.__create_widgets()
        # 前面に配置
        self.master.attributes("-topmost", True)
        # アイコンをVIPSのロゴに変更
        iconfile = base + '/vipstarcoin.ico'
        self.master.iconbitmap(default=iconfile)
        self.Button_ok.focus_set()
        #閉じるボタンが押されたときの処理
        self.master.protocol("WM_DELETE_WINDOW", self.__on_closing)
        #GUIを表示
        self.mainloop()

        return self.result