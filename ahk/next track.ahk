#NoEnv
#SingleInstance force

; Следующий трек в Spotify (даже в фоне)
PostMessage, 0x319, 0, 0xB0000,, ahk_exe Spotify.exe

Sleep 120   ; небольшая пауза для обработки команды
ExitApp