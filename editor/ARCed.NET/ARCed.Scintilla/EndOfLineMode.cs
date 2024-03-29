﻿#region Using Directives



#endregion Using Directives


namespace ARCed.Scintilla
{
    /// <summary>
    ///     Document's EndOfLine Mode
    /// </summary>
    public enum EndOfLineMode
    {
        /// <summary>
        ///     Carriage Return + Line Feed (Windows Style)
        /// </summary>
        Crlf = 0,

        /// <summary>
        ///     Carriage Return Only (Mac Style)
        /// </summary>
        CR = 1,

        /// <summary>
        ///     Line Feed Only (Unix Style)
        /// </summary>
        LF = 2,
    }
}
