#NoEnv
#SingleInstance force

; Перебираем все видимые окна и восстанавливаем минимизированные
WinGet, id, List,,, Program Manager  ; получаем список всех верхнеуровневых окон

Loop, %id%
{
    this_id := id%A_Index%
    
    ; Пропускаем невидимые / невалидные / скрытые окна
    WinGet, Style, Style, ahk_id %this_id%
    if !(Style & 0x10000000)  ; WS_VISIBLE
        continue
    
    ; Пропускаем панель задач, рабочий стол и т.п.
    WinGetClass, class, ahk_id %this_id%
    if (class = "Shell_TrayWnd" || class = "Progman" || class = "WorkerW")
        continue
    
    ; Если окно минимизировано — разворачиваем
    WinGet, MinMax, MinMax, ahk_id %this_id%
    if (MinMax = -1)  ; -1 = минимизировано
    {
        WinRestore, ahk_id %this_id%
        ; Опционально: WinActivate, ahk_id %this_id%   ; если хочешь активировать последнее
    }
}

Sleep 100  ; маленькая пауза на обработку
ExitApp