import Crypt
import tkinter as Tk
import ExternalFile
from Defines import STANDARD_RETURN
from Defines import EXTERNAL_FILE

#Tk.Frameクラスを継承
class Password(Tk.Frame):
    def __init__(self):
        #tkinterのインスタンスでありメインウィンドウ
        self.master = Tk.Tk()
        #BookeanVar()はTrueかFalseの2択の特殊な変数の型
        #パスワードを記憶するかどうかのチェックボックス用
        self.IsRememberPassword = Tk.BooleanVar()
        #Python3ではJavaと違って継承元のコンストラクタを暗黙的に呼び出さないので、明示的に呼び出す必要がある
        super().__init__(self.master)

    #tkinterではGUIの部品のことをウィジェットという
    #ウィジェットを作成するプライベート関数
    #パスワード入力画面を表示する
    def __create_widgets(self):

        #ウィンドウの幅
        width = 400
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
        self.master.title('パスワード入力画面')

        self.label_1 = Tk.Label(self,text='ウォレットのロックを解除するパスワードを入力してください。')
        #Enty：1行入力のテキストボックス 第1引数は配置するFrameオブジェクト　show='*'で伏字になる
        self.Entry_password = Tk.Entry(self, show='*',width= 30,font=8,relief='sunken',bd=3)
        #OKボタン　押されたらプライベート関数__pressed_okを実行する
        self.Button_ok = Tk.Button(self, text='OK', command=self.__pressed_ok,font=8,bd=3)
        #パスワードを記憶するかどうかのチェックボックス　onでTrue offでFalse
        self.CheckButton_RememberPassword = Tk.Checkbutton(self, text=u'パスワードを記憶', variable=self.IsRememberPassword)

        #grid()：テキストボックスをグリッド状に配置
        #上の４つのウィジェットをそれぞれ配置していく
        #ラベルは1行1列目　テキストボックスは2行1列目　OKボタンは2行2列目　チェックボックスは3行1列目
        self.label_1.grid(column=0,row=0)
        self.Entry_password.grid(column=0, row=1,pady=10)
        self.Button_ok.grid(column=1, row=1,padx=10)
        self.CheckButton_RememberPassword.grid(column=0, row=2)

    # 閉じるボタンが押されたら失敗を返却
    def __on_closing(self):
        self.master.destroy()
        self.result = STANDARD_RETURN.NOT_OK

    #OKボタンが押されたときに実行される
    #テキストボックスに入力されたパスワードを変数に保存して閉じる
    def __pressed_ok(self):
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

        self.external_file = ExternalFile.ExternalFile(EXTERNAL_FILE.PATH)
        self.external_file.save('password', crypted_str)
        self.external_file.save('secret_key', key)

    #is_force_inputがFalseかつ記憶済のパスワードがあれば、記憶済のパスワードを返す
    #それ以外はパスワード入力画面表示し、入力されたパスワードを返す
    #入力されたパスワードが正しいかどうかはここではチェックしない
    def get_password(self, is_force_input):
        password = ''
        # パスワード入力を強制しない場合は記憶済パスワードを探す
        if is_force_input == False:
            # 記憶した暗号化済みパスワードと秘密鍵を読み出し、複合して返す
            self.external_file = ExternalFile.ExternalFile(EXTERNAL_FILE.PATH)
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

