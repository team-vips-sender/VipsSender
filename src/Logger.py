#引数のメッセージをログに記録
#日付、時間を付ける
from datetime import datetime as dt
import Resource

def Logging(log_msg):

    log_content = dt.now().strftime('%Y/%m/%d %H:%M:%S,') + log_msg

    with open(Resource.resource_path('error.log'), mode='a', encoding="utf-8") as f:
        f.write(log_content + '\n')
