; Скрипт для одноразового перезапуска Discord
; Запускается, перезапускает Discord и закрывается

#NoTrayIcon  ; Не показываем иконку в трее
#SingleInstance, Force  ; Заменяем предыдущий экземпляр

; Закрываем все процессы Discord
Process, Close, Discord.exe
Process, Close, DiscordPTB.exe
Process, Close, DiscordCanary.exe

; Ждем 2 секунды чтобы процессы точно закрылись
Sleep, 2000

; Запускаем Discord заново
Run, %LocalAppData%\Discord\Update.exe --processStart Discord.exe

; Небольшая пауза перед выходом
Sleep, 500

; Завершаем работу скрипта
ExitApp