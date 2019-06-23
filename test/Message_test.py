import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\src'))
import Message

Message.display('1 byte charactor test')
Message.display('２バイト文字テスト')
Message.display(
'''
マルチラインテスト

VIPSTARCOIN (VIPS) は5ちゃんねるニュー速VIP板発祥の仮想通貨です。

国産仮想通貨として多目的に利用されること、
ひいては寄付への利用で世界に貢献することを目指して開発が進んでいます。

強いコミュニティの力で運営し、盛り上げていきます。
'''
)


