#SingleInstance Force
#Requires AutoHotkey v1.1+
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

; Укажите имя процесса (например: notepad.exe, chrome.exe)
ProcessName = powershell.exe

; Находим и сворачиваем все окна процесса
WinGet, Windows, List, ahk_exe %ProcessName%
Loop, %Windows%
{
    WinMinimize, % "ahk_id " Windows%A_Index%
}

ExitApp