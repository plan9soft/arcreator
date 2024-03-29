import os
import wx

import Kernel

from PyitectConsumes import Script

# --------------------------------------------------------------------------------------
# Manager
# --------------------------------------------------------------------------------------


class ScriptEditorManager(object):

    @staticmethod
    def EnsureScriptDirectory():
        """Ensures the project's script directory exists"""
        projDir = Kernel.GlobalObjects["CurrentProjectDir"]
        dir = os.path.join(projDir, 'Data', 'Scripts')
        if not os.path.exists(dir) or not os.path.isdir(dir):
            Kernel.Protect(os.makedirs, True)(dir)

    # ----------------------------------------------------------------------------------
    @staticmethod
    def LoadScripts():
        """Loads all scripts and stores them in memory

        Arguments:
        dir -- The directory where the scripts are located

        Returns:
        None

        """
        from fnmatch import fnmatch

        ScriptEditorManager.EnsureScriptDirectory()
        projDir = Kernel.GlobalObjects["CurrentProjectDir"]
        dir = os.path.join(projDir, 'Data', 'Scripts')
        # TODO: Include internal scripts as read-only entries?
        paths = []
        for file in os.listdir(dir):
            if fnmatch(file, '*.rb'):
                paths.append(os.path.join(dir, file))
        scripts = [Script(i, path, False) for i, path in enumerate(sorted(paths))]
        if 'Scripts' in Kernel.GlobalObjects:
            Kernel.GlobalObjects['Scripts'] =  scripts
        else:
            Kernel.GlobalObjects.request_new_key('Scripts', 'CORE', scripts)

    # ----------------------------------------------------------------------------------
    @staticmethod
    def SaveScripts():
        """Iterates over each script and saves the it to disk

        Arguments:
        None

        Returns:
        Bool value if all scripts were saved successfully

        """
        if 'Scripts' not in Kernel.GlobalObjects:
            return False
        result = True
        scripts = Kernel.GlobalObjects['Scripts']
        ScriptEditorManager.EnsureScriptDirectory()
        for i, script in enumerate(scripts):
            if not script.SaveScript(i):
                result = False
                Kernel.Log('Failed to save script \"%s\".' % script.GetName(), '[Script Editor]', True, False)
        return result

    # ----------------------------------------------------------------------------------
    @staticmethod
    def GetScriptStatistics(whitespace=True):
        """Returns statistics of the combined scripts

        Arguments:
        whitespace -- True or False if whitespace will be included in count

        Returns:
        A four element tuple whose values are as follows:
            (Number of Scripts, Total Lines, Total Words, Total Characters)

        """
        if 'Scripts' not in Kernel.GlobalObjects:
            return (0, 0, 0, 0)
        else:
            scripts = Kernel.GlobalObjects['Scripts']
            count = total_lines = total_words = total_characters = 0
            for script in scripts:
                count += 1
                lines = script.GetLines()
                if not whitespace:
                    lines = []
                    for line in script.GetLines():
                        stripped = line.strip()
                        if stripped == '' or stripped.startswith('#'):
                            continue
                        lines.append(line)
                else:
                    lines = script.GetLines()
                total_lines += len(lines)
                for line in lines:
                    total_characters += len(line)
                    total_words += len(line.split())
            return (count, total_lines, total_words, total_characters)

    # ----------------------------------------------------------------------------------
    @staticmethod
    def GetUserSettings():
        """
        Returns the settings defined in the configuration

        Returns:
        A list of format strings for the respective styles
        """
        styles = ScriptEditorManager.GetStyles()
        cfg = Kernel.Config.getUnified()['ScriptEditor']
        settings = [cfg[styles[1]] for style in styles]
        return settings

    # ----------------------------------------------------------------------------------
    @staticmethod
    def GetDefaultSettings():
        """
        Returns the internal default settings

        Returns:
        A list of format strings for the respective styles
        """
        # Get the default font faces for font families
        mono = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        roman = wx.Font(10, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)

        # TODO: Remove
        mono.SetFaceName('Consolas')

        faces = {
            'mono': mono.GetFaceName(),
            'roman': roman.GetFaceName(),
            'size': 10,
            'size2': 8
        }
        settings = [
            "face:%(mono)s,size:%(size)d" % faces,  # Default
            "back:#C0C0C0,face:%(mono)s,size:%(size2)d" % faces,  # Line Numbers
            "face:%(mono)s" % faces,  # Control Character
            "fore:#FFFFFF,back:#0000FF,bold",  # Brace Light
            "fore:#000000,back:#FF0000,bold",  # Brace Bad
            "fore:#008000,face:%(mono)s,size:%(size)d" % faces,  # Comment Block
            "fore:#008000,face:%(mono)s,size:%(size)d" % faces,  # Comment
            "fore:#800000,face:%(mono)s,size:%(size)d" % faces,  # Numbers
            "fore:#800080,italic,face:%(roman)s,size:%(size)d" % faces,  # Double-Quoted Strings
            "fore:#C80080,italic,face:%(roman)s,size:%(size)d" % faces,  # Single-Quoted Strings
            "fore:#0000FF,bold,size:%(size)d" % faces,  # Keywords
            "fore:#000000,bold,size:%(size)d" % faces,  # Class Name
            "fore:#000000,bold,size:%(size)d" % faces,  # Module Name
            "fore:#000000,bold,size:%(size)d" % faces,  # Method Name
            "fore:#2B91AF,bold,size:%(size)d" % faces,  # Operators
            "fore:#000000,face:%(mono)s,size:%(size)d" % faces,  # Normal
            "fore:#000000,face:%(mono)s,size:%(size)d" % faces,  # Global Variable
            "fore:#000000,face:%(mono)s,size:%(size)d" % faces,  # Instance Variable
            "fore:#000000,face:%(mono)s,size:%(size)d" % faces,  # Class Variable
            "fore:#9370DB,face:%(mono)s,size:%(size)d" % faces,  # Regular Expressions
            "fore:#000000,face:%(mono)s,size:%(size)d" % faces,  # Symbol
            "fore:#808080,face:%(mono)s,size:%(size)d" % faces,  # Backticks
            "fore:#000000,face:%(mono)s,size:%(size)d" % faces,  # Data Section
            "fore:#FF0000,face:%(mono)s,bold,size:%(size)d" % faces  # Error
        ]
        return settings

    # ----------------------------------------------------------------------------------
    @staticmethod
    def GetStyles():
        """
        Returns a list of styles for the Scintilla control

        Returns:
        A list of 2 element tuples, the first element is the constant for the setting,
        and the second element is the string name of the key in the configuration
        """
        import wx.stc as stc
        styles = [
            (stc.STC_STYLE_DEFAULT, 'global_default'),
            (stc.STC_STYLE_LINENUMBER, 'line_number'),
            (stc.STC_STYLE_CONTROLCHAR, 'control_char'),
            (stc.STC_STYLE_BRACELIGHT, 'brace_light'),
            (stc.STC_STYLE_BRACEBAD, 'brace_bad'),
            (stc.STC_ST_COMMENT, 'comment_block'),
            (stc.STC_RB_COMMENTLINE, 'comment_line'),
            (stc.STC_RB_NUMBER, 'numbers'),
            (stc.STC_RB_STRING, 'double_quote_string'),
            (stc.STC_RB_CHARACTER, 'single_quote_string'),
            (stc.STC_RB_WORD, 'keywords'),
            (stc.STC_RB_CLASSNAME, 'class_name'),
            (stc.STC_RB_MODULE_NAME, 'module_name'),
            (stc.STC_RB_DEFNAME, 'method_name'),
            (stc.STC_RB_OPERATOR, 'operators'),
            (stc.STC_RB_IDENTIFIER, 'normal_text'),
            (stc.STC_RB_GLOBAL, 'global_variables'),
            (stc.STC_RB_INSTANCE_VAR, 'instance_variables'),
            (stc.STC_RB_CLASS_VAR, 'class_variables'),
            (stc.STC_RB_REGEX, 'regex'),
            (stc.STC_RB_SYMBOL, 'symbols'),
            (stc.STC_RB_BACKTICKS, 'backticks'),
            (stc.STC_RB_DATASECTION, 'data_sections'),
            (stc.STC_RB_ERROR, 'errors')
        ]
        return styles

    # ----------------------------------------------------------------------------------
    @staticmethod
    def ApplyUserSettings(scriptcontrol):
        """
        Applies user-defined settings to the control

        Arguments:
        scriptcontrol -- A wx.stc.StyledTextCtrl instance

        Returns:
        None
        """
        default = ScriptEditorManager.GetDefaultSettings()
        styles = ScriptEditorManager.GetStyles()
        cfg = Kernel.Config.getUnified()['ScriptEditor']
        for i in range(len(styles)):
            style = styles[i]
            try:
                setting = cfg[style[1]]
                scriptcontrol.StyleSetSpec(style[0], setting)
            except:
                scriptcontrol.StyleSetSpec(style[0], default[i])
                Kernel.Log(str.format('Style setting \"{}\" is malformed/missing and the default value will be used', styles[i][1]), '[Script Editor]', True, False)
        scriptcontrol.SetTabWidth(int(cfg['tab_width']))
        scriptcontrol.SetEdgeColumn(int(cfg['edge_column']))
        scriptcontrol.SetCaretLineVisible(cfg['show_caret'])
        scriptcontrol.SetCaretForeground(ScriptEditorManager.ParseColor(cfg['caret_fore']))
        scriptcontrol.SetCaretLineBack(ScriptEditorManager.ParseColor(cfg['caret_back']))
        scriptcontrol.SetCaretLineBackAlpha(int(cfg['caret_alpha']))
        scriptcontrol.SetIndentationGuides(cfg['indent_guides'])

    # ----------------------------------------------------------------------------------
    @staticmethod
    def ParseColor(string):
        """Parses the color string and returns the wx.Colour instance"""
        if string.startswith('#'):
            string = string[1:]
        if len(string) < 6:
            string = string.zfill(6)
        return wx.Colour(int(string[:2], 16), int(string[2:4], 16), int(string[4:6], 16))

    # ----------------------------------------------------------------------------------
    @staticmethod
    def ApplyDefaultSettings(scriptcontrol):
        """
        Applies default settings to the control

        Arguments:
        scriptcontrol -- A wx.stc.StyledTextCtrl instance

        Returns:
        None
        """
        CARET_ALPHA = 255
        default = ScriptEditorManager.GetDefaultSettings()
        styles = ScriptEditorManager.GetStyles()
        cfg = Kernel.Config.getUnified()['ScriptEditor']
        for i in range(len(default)):
            scriptcontrol.StyleSetSpec(styles[i][0], default[i])
            cfg.set(styles[i][1], default[i])
        scriptcontrol.SetTabWidth(2)
        scriptcontrol.SetCaretLineVisible(True)
        scriptcontrol.SetCaretLineBack(wx.Colour(0, 0, 0))
        scriptcontrol.SetCaretForeground(wx.Colour(40, 40, 40))
        scriptcontrol.SetCaretLineBackAlpha(CARET_ALPHA)
        scriptcontrol.SetIndentationGuides(40)
        scriptcontrol.SetEdgeColumn(80)
