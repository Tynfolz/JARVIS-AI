; === AHK Скрипт для автоматического закрытия Adobe Creative Cloud ===
; Скрипт запускается, выполняет завершение процессов и закрывается

#NoTrayIcon           ; Не показывать иконку в трее
#Persistent           ; Оставляем процесс ненадолго активным
#SingleInstance Force ; Разрешаем только один экземпляр

; Выключаем лишние функции
SendMode Input
SetWorkingDir %A_ScriptDir%

; Запускаем функцию завершения
KillAdobeCC()

; Завершаем скрипт после выполнения
ExitApp

KillAdobeCC() {
    ; Список процессов Adobe для завершения
    processes := ["Creative Cloud.exe"
                , "CCXProcess.exe"
                , "AdobeIPCBroker.exe"
                , "Adobe Desktop Service.exe"
                , "CoreSync.exe"
                , "CCLibrary.exe"
                , "AGSService.exe"
                , "AGMService.exe"
                , "Adobe CEF Helper.exe"
                , "AdobeCollabSync.exe"
                , "AdobeExtensionsService.exe"
                , "CRWindowsClientService.exe"
                , "Adobe Update Service.exe"
                , "AdobeARM.exe"
                , "Adobe_Updater.exe"
                , "Creative Cloud Helper.exe"
                , "node.exe"]  ; CCXProcess часто запускает node
    
    ; Сначала пробуем мягкое завершение
    for index, processName in processes
    {
        Process, Close, %processName%
    }
    
    ; Небольшая пауза для мягкого завершения
    Sleep, 500
    
    ; Принудительное завершение оставшихся процессов через taskkill
    for index, processName in processes
    {
        Run, taskkill /f /im "%processName%" 2>nul, , Hide
    }
    
    ; Дополнительная очистка: завершаем все процессы с "Adobe" в имени
    Run, taskkill /f /im "Adobe*" /t 2>nul, , Hide
    Run, taskkill /f /im "Creative Cloud*" /t 2>nul, , Hide
}

; Автоматическое завершение скрипта через 2 секунды
; (на случай, если что-то пошло не так)
SetTimer, AutoExit, -2000

AutoExit:
    ExitApp