#NoEnv
#SingleInstance force

; Запускаем .bat файл (Run — асинхронно, скрипт не ждёт завершения)
Run, "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Calculator.lnk"

Sleep 300   ; небольшая пауза, чтобы команда точно ушла (можно уменьшить/убрать)
ExitApp
