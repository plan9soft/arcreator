#region Using Directives

using System;
using System.Diagnostics.CodeAnalysis;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;

#endregion

namespace ARCed.Core.Win32
{
    /// <summary>
    /// Static class containing methods that utilize P/Invoke or other unmanaged libraries
    /// </summary>
    public static class NativeMethods
    {
		[DllImport("User32.dll", CharSet=CharSet.Auto)]
        [return: MarshalAs(UnmanagedType.Bool)]
		public static extern bool DragDetect(IntPtr hWnd, Point pt);

        [DllImport("User32.dll", CharSet=CharSet.Auto)]
        public static extern IntPtr GetFocus();

        [DllImport("User32.dll", CharSet=CharSet.Auto)]
        public static extern IntPtr SetFocus(IntPtr hWnd);

        [DllImport("User32.dll", CharSet=CharSet.Auto)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool PostMessage(IntPtr hWnd, int Msg, uint wParam, uint lParam);

        [DllImport("User32.dll", CharSet=CharSet.Auto)]
        public static extern uint SendMessage(IntPtr hWnd, int Msg, uint wParam, uint lParam);

        [DllImport("User32.dll", CharSet=CharSet.Auto)]
        public static extern int ShowWindow(IntPtr hWnd, short cmdShow);

        [DllImport("User32.dll", CharSet=CharSet.Auto)]
        public static extern int SetWindowPos(IntPtr hWnd, IntPtr hWndAfter, int X, int Y, int Width, int Height, FlagsSetWindowPos flags);

		[DllImport("user32.dll", CharSet = CharSet.Auto)]
		public static extern int GetWindowLong(IntPtr hWnd, int Index);

		[DllImport("user32.dll", CharSet = CharSet.Auto)]
		public static extern int SetWindowLong(IntPtr hWnd, int Index, int Value);

		[DllImport("user32.dll", CharSet=CharSet.Auto)]
		public static extern int ShowScrollBar(IntPtr hWnd, int wBar, int bShow);

		[DllImport("user32.dll", CharSet=CharSet.Auto)]
        //*********************************
        // FxCop bug, suppress the message
        //*********************************
        [SuppressMessage("Microsoft.Portability", "CA1901:PInvokeDeclarationsShouldBePortable", MessageId = "0")]
		public static extern IntPtr WindowFromPoint(Point point);

        [DllImport("Kernel32.dll", CharSet = CharSet.Auto)]
        public static extern int GetCurrentThreadId();

        public delegate IntPtr HookProc(int code, IntPtr wParam, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern IntPtr SetWindowsHookEx(HookType code, HookProc func, IntPtr hInstance, int threadID);

        [DllImport("user32.dll")]
        public static extern int UnhookWindowsHookEx(IntPtr hhook);

        [DllImport("user32.dll")]
        public static extern IntPtr CallNextHookEx(IntPtr hhook, int code, IntPtr wParam, IntPtr lParam);

        public const int WM_SETREDRAW = 11;

        [DllImport("User32.dll")]
        public static extern int SendMessage(IntPtr hWnd, Int32 wMsg, bool wParam, Int32 lParam);

        [DllImport("Gdi32.dll")]
        public static extern IntPtr AddFontMemResourceEx(IntPtr pbFont, uint cbFont, IntPtr pdv,
            [In] ref uint pcFonts);

        [DllImport("Gdi32.dll")]
        public static extern int AddFontResourceEx(string lpszFilename, uint fl, IntPtr pdv);

        /// <summary>
        /// Writes a configuration value to an .ini file
        /// </summary>
        /// <param name="section">The section name</param>
        /// <param name="key">The key name</param>
        /// <param name="val">The value to write</param>
        /// <param name="filePath">The path to the file</param>
        /// <returns>Error code</returns>
        [DllImport("Kernel32.dll")]
        public static extern long WritePrivateProfileString(string section,
            string key, string val, string filePath);

        /// <summary>
        /// Reads a configuration value to an .ini file
        /// </summary>
        /// <param name="section">The section name</param>
        /// <param name="key">The key name</param>
        /// <param name="def">Default string if value cannot be found</param>
        /// <param name="retVal">The buffer to write the value to</param>
        /// <param name="size">The maximum buffer size</param>
        /// <param name="filePath">The path to the file</param>
        /// <returns>Error code</returns>
        [DllImport("Kernel32.dll")]
        public static extern int GetPrivateProfileString(string section,
                 string key, string def, StringBuilder retVal, int size, string filePath);

        /// <summary>
        /// Creates a cursor object and returns it
        /// </summary>
        /// <param name="str">The name of the resouce file</param>
        /// <returns>A handle to a cursor object</returns>
        [DllImport("User32.dll", CharSet = CharSet.Ansi, BestFitMapping = false, ThrowOnUnmappableChar = true)]
        public static extern IntPtr LoadCursorFromFile(String str);

        /// <summary>
        /// Sets the foreground window
        /// </summary>
        /// <param name="hWnd">A handle to a window</param>
        /// <returns>Flag if error occurred</returns>
        [DllImport("User32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);

        /// <summary>
        /// Changes the icon of an attached console
        /// </summary>
        /// <param name="hIcon">A handle to an icon</param>
        /// <returns>Flag if error occurred</returns>
        [DllImport("Kernel32.dll")]
        public static extern bool SetConsoleIcon(IntPtr hIcon);

        /// <summary>
        /// Obtains the short path form of a specified input path
        /// </summary>
        /// <param name="lpszLongPath">Points to a null-terminated path string. The function 
        /// obtains the short form of this path</param>
        /// <param name="lpszShortPath">Points to a buffer to receive the null-terminated 
        /// short form of the path specified by lpszLongPath</param>
        /// <param name="cchBuffer">The size of the buffer that lpszShortPath points to</param>
        /// <returns>Value is the length, in characters, of the string copied to lpszShortPath</returns>
        [DllImport("Kernel32.dll")]
        public static extern uint GetShortPathName(string lpszLongPath,
            [Out] StringBuilder lpszShortPath, uint cchBuffer);

        /// <summary>
        /// Allocates a new console for the calling process
        /// </summary>
        /// <returns>Non-zero if successful, zero otherwise</returns>
        [DllImport("Kernel32.dll", EntryPoint = "AllocConsole")]
        public static extern int AllocConsole();
	}
}