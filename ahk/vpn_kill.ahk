#NoEnv
#SingleInstance Force
SetWorkingDir %A_ScriptDir%
SetBatchLines -1

; ────────────────────────────────────────────────
; Скрипт запускается → сразу убивает Happ → и завершает сам себя
; ────────────────────────────────────────────────

; 1. Даём окну/процессу немного времени "успокоиться", если оно только-только запустилось
Sleep 400

; 2. Пытаемся закрыть окно по-разному
WinClose, ahk_exe Happ.exe     ,, 2
WinClose, Happ ahk_class AutoHotkeyGUI
Sleep 300

; 3. Закрываем основной процесс "мягко"
Process, Close, Happ.exe
Process, Close, Happ-x64.exe   ; на случай если 64-битная версия называется иначе
Sleep 400

; 4. Жёсткое убийство (включая дочерние процессы)
Run, %ComSpec% /c "taskkill /F /IM Happ.exe     /T >nul 2>&1",, Hide
Run, %ComSpec% /c "taskkill /F /IM Happ*        /T >nul 2>&1",, Hide
Run, %ComSpec% /c "taskkill /F /IM xray.exe     /T >nul 2>&1",, Hide   ; ядро, которое часто остаётся
Run, %ComSpec% /c "taskkill /F /IM xray*        /T >nul 2>&1",, Hide

Sleep 300

; 5. (опционально) сообщение, что всё сделано — можно закомментировать
; MsgBox, 64, Готово, Happ и связанные процессы закрыты., 2

; 6. Скрипт завершает сам себя
ExitApp
