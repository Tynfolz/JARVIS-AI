#NoEnv
#SingleInstance force
SetWorkingDir %A_ScriptDir%

; Самый универсальный способ остановить музыку/видео
Send {Media_Stop}

; Альтернатива 1 (часто лучше работает в 2024–2026 годах)
; Send {vkB3sc127}   ; Media_Stop в скан-коде

; Альтернатива 2 (пауза + стоп в некоторых плеерах)
; Send {Media_Play_Pause}
; Sleep 50
; Send {Media_Stop}

Sleep 80   ; даём системе время обработать команду
ExitApp