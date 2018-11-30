// cs example of "def open_cpe_agent():" in python module winAuto.py

using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

class OpenTray {

    int hWnd = 0;
    private const int SW_HIDE = 0;
    private const int SW_SHOW = 5;
    private const int SW_SHOWNORMAL = 1;

    [DllImport("User32")]
    private static extern int ShowWindow(int hwnd, int nCmdShow);

    //[DllImport("User32")]
    //public static extern int SetForegroundWindow(int hwnd);

    public static void Main(string[] args) {
        Program p = new Program();
        p.Show_hWnd();
    }
    void Show_hWnd() {
        Process[] processRunning = Process.GetProcesses();
        foreach(Process pr in processRunning) {
            if(pr.ProcessName == "Check Point Endpoint Security") {
                hWnd = pr.MainWindowHandle.ToInt32();
                ShowWindow(hWnd, SW_SHOW);
                ShowWindow(hWnd, SW_SHOWNORMAL);
                //SetForegroundWindow(hWnd);
            }
        }
    }
}