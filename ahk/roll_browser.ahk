#SingleInstance force
Sleep, 300

IfWinExist, ahk_exe opera.exe
{
    WinGet, state, MinMax, ahk_exe opera.exe
    if (state = -1)
        WinActivate, ahk_exe opera.exe
    else
        WinMinimize, ahk_exe opera.exe
}
else
{
    Run, opera.exe
}

Sleep, 300
ExitApp