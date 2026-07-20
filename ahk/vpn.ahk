#NoEnv
#SingleInstance force
SendMode Input
SetWorkingDir %A_ScriptDir%

; Запускаем .bat файл (Run — асинхронно, скрипт не ждёт завершения)
Run, "C:\Users\tynfolz\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\Happ.lnk" 

Sleep 600  ; небольшая пауза, чтобы команда точно ушла (можно уменьшить/убрать)

; Запускаем .bat файл (Run — асинхронно, скрипт не ждёт завершения)
Run, "D:\jarvis\commands\steam\ahk\vpn_curtail.exe"

Sleep 300   ; небольшая пауза, чтобы команда точно ушла (можно уменьшить/убрать)
ExitApp