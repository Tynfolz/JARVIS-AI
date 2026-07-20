#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%

файл := "message.txt"

; Пробуем самые распространённые варианты по порядку
FileEncoding, UTF-8
FileRead, текст, %файл%

if (ErrorLevel || StrLen(текст) < 200) {
    ; если не получилось — пробуем без указания кодировки
    FileEncoding, CP1251
    FileRead, текст, %файл%
}

if ErrorLevel {
    MsgBox, Не удалось прочитать файл`n%файл%`n`nПроверьте, существует ли файл и есть ли в нём текст.
    ExitApp
}

Clipboard := текст
ClipWait, 3

if ErrorLevel {
    MsgBox, Не удалось поместить текст в буфер обмена
    ExitApp
}


ExitApp

Убрать:
    ToolTip
return