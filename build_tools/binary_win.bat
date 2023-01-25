@REM Relies on working directory being the root of the project
pyinstaller.exe --clean        ^
    --workpath "./build/temp/" ^
    --distpath "./build/"      ^
    build_tools/binary.spec
