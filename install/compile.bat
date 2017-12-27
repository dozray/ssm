cd /d c:\
cd \
cd PyInstaller
rem define the PyInstaller home
cd /d c:\PyInstaller
@SET src="%~dp0\..\src"

echo "正在编译文件..."
echo "python PyInstaller.py -a -w --clean --upx-dir=c:\PyInstaller  -i c:\cs\src\Airport.ico %src%\CardService.py"

python PyInstaller.py -a -w --clean %src%\CardService.py

echo "编译完成，正在拷贝文件..."

rem copy file to dest.
xcopy CardService\dist\CardService %~dp0\pkg\CardService /e/r/y/f

pause