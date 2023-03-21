cd %~dp0\..\
echo Building .exe from %cd%

pyinstaller.exe --clean        ^
    --workpath "./build/temp/" ^
    --distpath "./build/"      ^
    build_tools/pyinstaller/binary.spec ^
&& rmdir /s /q %cd%\build\temp
