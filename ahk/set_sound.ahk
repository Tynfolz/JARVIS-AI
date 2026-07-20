#NoEnv
#SingleInstance force

; Проверяем, передан ли аргумент
if (A_Args.Length() < 1)
{
    ; Можно раскомментировать, если хочешь видеть ошибку
    ; MsgBox, Нужно передать громкость в %%`nПример: "%A_ScriptFullPath%" 65
    ExitApp
}

percent := A_Args[1] + 0   ; приводим к числу

; Защита от некорректных значений
if (percent < 0 || percent > 100)
    ExitApp

vol := percent / 100.0     ; nircmd требует значение от 0.0 до 1.0

; ←←← ИЗМЕНИ ЭТОТ ПУТЬ НА СВОЙ РЕАЛЬНЫЙ ←←←
nircmd_path := "D:\jarvis\nircmd-x64\nircmd.exe"   ; или "D:\Tools\nircmd.exe" и т.д.

; Запускаем команду тихо
RunWait, "%nircmd_path%" setappvolume "Spotify.exe" %vol%, , Hide

ExitApp