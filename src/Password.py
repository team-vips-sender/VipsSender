import Crypt
import tkinter as Tk
import tkinter.ttk as Ttk
import ExternalFile
from Defines import STANDARD_RETURN
from Defines import EXTERNAL_FILE
import OsDepend

#Tk.Frameクラスを継承
class Password(Tk.Frame):
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
        self.master.title('パスワード入力画面')

        # ボタンのスタイルを変更
        style = Ttk.Style()
        style.configure('TButton', font=('Meiryo UI', 8))

        #フレームの作成
        text_frame = Ttk.Frame(self)
        text_frame.grid(column=0, row=0, sticky='w')
        input_frame = Ttk.Frame(self)
        input_frame.grid(column=0, row=1, sticky='we')
        remember_frame = Ttk.Frame(self)
        remember_frame.grid(column=0, row=2, sticky='w')
        
        self.label_1 = Ttk.Label(text_frame, text='ウォレットのロックを解除するパスワードを入力してください。', font=("Meiryo UI", 11))
        self.label_1.pack(side='left', anchor='w')
        
        #Enty：1行入力のテキストボックス 第1引数は配置するFrameオブジェクト　show='*'で伏字になる
        self.Entry_password = Ttk.Entry(input_frame, show='*', font=("Meiryo UI", 8))
        self.Entry_password.pack(side='left', padx=5, expand=1, fill='x')
        self.Entry_password.focus_set()
        self.Entry_password.bind('<Return>', self.__pressed_ok)
        
        #OKボタン　押されたらプライベート関数__pressed_okを実行する
        self.Button_ok = Ttk.Button(input_frame, text='OK', command=self.__pressed_ok, width=7)
        self.Button_ok.pack(side='left')

        #パスワードを記憶するかどうかのチェックボックス　onでTrue offでFalse
        self.CheckButton_RememberPassword = Ttk.Checkbutton(remember_frame, text=u'パスワードを記憶', variable=self.IsRememberPassword)
        self.CheckButton_RememberPassword.pack(side='left')

    # 閉じるボタンが押されたら失敗を返却
    def __on_closing(self):
        self.master.destroy()
        self.result = STANDARD_RETURN.NOT_OK

    #OKボタンが押されたときに実行される
    #テキストボックスに入力されたパスワードを変数に保存して閉じる
    def __pressed_ok(self, event=None):
        self.Password = self.Entry_password.get()
        self.master.destroy()
        self.result = STANDARD_RETURN.OK

    #パスワードを記憶する
    def save(self,password):
        # 平文のパスワードを暗号化
        encrypt_result = Crypt.Encrypt(password)
        # 暗号化したパスワード
        crypted_str = encrypt_result[0]
        # 秘密鍵
        key = encrypt_result[1]
        # それぞれテキストで保存できるように16進文字列に変換しておく
        crypted_str = crypted_str.hex()
        key = key.hex()

        ret, user_path = OsDepend.get_user_path()
        if ret == STANDARD_RETURN.OK:
            self.external_file = ExternalFile.ExternalFile(user_path + EXTERNAL_FILE.PATH)
            self.external_file.save('password', crypted_str)
            self.external_file.save('secret_key', key)

    #is_force_inputがFalseかつ記憶済のパスワードがあれば、記憶済のパスワードを返す
    #それ以外はパスワード入力画面表示し、入力されたパスワードを返す
    #入力されたパスワードが正しいかどうかはここではチェックしない
    def get_password(self, is_force_input):
        password = ''
        # パスワード入力を強制しない場合は記憶済パスワードを探す
        if is_force_input == False:
            ret, user_path = OsDepend.get_user_path()
            if ret != STANDARD_RETURN.OK:
                return STANDARD_RETURN.NOT_OK, ''

            # 記憶した暗号化済みパスワードと秘密鍵を読み出し、複合して返す
            self.external_file = ExternalFile.ExternalFile(user_path + EXTERNAL_FILE.PATH)
            result_pass = self.external_file.get('password')
            result_key = self.external_file.get('secret_key')
            if result_pass[0] == 0 and result_key[0] == 0:
                crypted_str = result_pass[1]
                key = result_key[1]
                # 16進文字列に変換して保存しているので元のバイナリに戻す
                crypted_str = bytes.fromhex(crypted_str)
                key = bytes.fromhex(key)
                decrypt_result = Crypt.Decrypt(crypted_str, key)
                return STANDARD_RETURN.OK,decrypt_result
            # 読み出しできなければパスワード入力させる
            else:
                pass
        #tkinterのインスタンスでありメインウィンドウ
        self.master = Tk.Tk()
        #BookeanVar()はTrueかFalseの2択の特殊な変数の型
        #パスワードを記憶するかどうかのチェックボックス用
        self.IsRememberPassword = Tk.BooleanVar()
        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

        # ウィジェット作成
        self.__create_widgets()
        #閉じるボタンが押されたときの処理
        self.master.protocol("WM_DELETE_WINDOW", self.__on_closing)
        #GUIを表示
        self.mainloop()
        #入力されたパスワードを変数に保存
        if self.result == STANDARD_RETURN.OK:
            password = self.Password

            # 記憶するにチェックしてＯＫが押されていれば記憶
            if self.IsRememberPassword.get() :
                self.save(password)

        return self.result,password

