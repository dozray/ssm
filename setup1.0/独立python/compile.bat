cd /d c:\
cd \
cd PyInstaller
echo "正在编译文件..."
python PyInstaller.py -a --clean -w --upx-dir=c:\PyInstaller  --icon=c:\cs\src\Airport.ico c:\cs\src\CardService.py

echo "编译完成，正在拷贝文件..."

xcopy CardService\dist\CardService %~dp0\pkg\CardService /e/r/y/f

pause