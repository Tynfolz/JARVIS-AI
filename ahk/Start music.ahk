#NoEnv
#SingleInstance force

; Отправляем WM_APPCOMMAND с кодом Play/Pause напрямую в Spotify
PostMessage, 0x319, 0, 0xE0000,, ahk_exe Spotify.exe

Sleep 120   ; даём время обработать
ExitApp