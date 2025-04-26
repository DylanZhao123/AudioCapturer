@echo off
REM 用你本地安装的 Python310 运行指定的 .py 脚本

REM 检查是否提供了参数（脚本路径）
IF "%~1"=="" (
    echo 请将 .py 文件拖到这个批处理文件上运行，或者用命令行提供文件路径。
    pause
    exit /b
)

REM 执行 Python 脚本
"C:\Users\Dylan Zhao\AppData\Local\Programs\Python\Python310\python.exe" %*
