/*
   Optional Windows bootstrapper source.
   Build with MinGW on Windows or x86_64-w64-mingw32-gcc:
   x86_64-w64-mingw32-gcc -municode -mwindows true_vision_launcher.c -o TrueVisionLauncher.exe

   This intentionally launches the reproducible Python companion instead of
   pretending to contain PSN, HID, or driver logic itself.
*/
#define UNICODE
#define _UNICODE
#include <windows.h>
#include <shellapi.h>

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR command_line, int show) {
    (void)instance; (void)previous; (void)command_line; (void)show;
    HINSTANCE result = ShellExecuteW(NULL, L"open", L"py", L"main.py", NULL, SW_SHOWNORMAL);
    if ((INT_PTR)result <= 32) {
        MessageBoxW(NULL, L"TRUE VISION could not start. Install Python 3.11+ or run the packaged build.", L"TRUE VISION", MB_ICONERROR);
        return 1;
    }
    return 0;
}
