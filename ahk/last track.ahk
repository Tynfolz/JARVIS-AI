#NoEnv
#SingleInstance force

; Предыдущий трек в Spotify (даже в фоне)
PostMessage, 0x319, 0, 0xC0000,, ahk_exe Spotify.exe

Sleep 120   ; даём время на обработку
ExitApp