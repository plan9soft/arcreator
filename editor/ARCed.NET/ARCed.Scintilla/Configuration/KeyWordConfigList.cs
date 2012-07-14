#region Using Directives

using System;
using System.Collections.ObjectModel;

#endregion Using Directives


namespace ARCed.Scintilla.Configuration
{
    public class KeyWordConfigList : KeyedCollection<int, KeyWordConfig>
    {
        #region Methods

        protected override int GetKeyForItem(KeyWordConfig item)
        {
            return item.List;
        }

        #endregion Methods
    }
}
