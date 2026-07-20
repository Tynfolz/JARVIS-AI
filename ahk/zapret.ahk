#NoEnv
#SingleInstance force

; Запускаем .bat файл (Run — асинхронно, скрипт не ждёт завершения)
Run, "C:\Users\tynfolz\Documents\diskordfix"

Sleep 300   ; небольшая пауза, чтобы команда точно ушла (можно уменьшить/убрать)
ExitApp
