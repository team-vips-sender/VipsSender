set SOURCE_DIR=..\src

rmdir /s /q dist
pyinstaller --clean --noconsole --icon=%SOURCE_DIR%\resources\vipstarcoin.ico --add-data="%SOURCE_DIR%\resources\vipstarcoin.ico;resources" %SOURCE_DIR%\VipsSender.py

pause
