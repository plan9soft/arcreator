#region Using Directives

using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;

#endregion


namespace ARCed.Scintilla
{
    [TypeConverter(typeof(ExpandableObjectConverter))]
    public class Indicator : ScintillaHelperBase
    {
        #region Fields

        private int _number;

        #endregion Fields


        #region Methods

        public override bool Equals(object obj)
        {
            if (!IsSameHelperFamily(obj))
                return false;

            return ((Indicator)obj).Number == this.Number;
        }


        private Color GetDefaultColor()
        {
            if (this._number == 0)
                return Color.FromArgb(0, 127, 0);
            else if (this._number == 1)
                return Color.FromArgb(0, 0, 255);
            else if (this._number == 2)
                return Color.FromArgb(255, 0, 0);
            else
                return Color.FromArgb(0, 0, 0);
        }


        private IndicatorStyle GetDefaultStyle()
        {
            if (this._number == 0)
                return IndicatorStyle.Squiggle;
            else if (this._number == 1)
                return IndicatorStyle.TT;
            else
                return IndicatorStyle.Plain;
        }


        public override int GetHashCode()
        {
            return base.GetHashCode();
        }


        public void Reset()
        {
            this.ResetColor();
            this.ResetIsDrawnUnder();
            this.ResetStyle();
        }


        public void ResetColor()
        {
            this.Color = this.GetDefaultColor();
        }


        public void ResetIsDrawnUnder()
        {
            this.IsDrawnUnder = false;
        }


        public void ResetStyle()
        {
            this.Style = this.GetDefaultStyle();
        }


        public Range Search()
        {
            return this.Search(Scintilla.GetRange());
        }


        public Range Search(Range searchRange)
        {
            int foundStart = NativeScintilla.IndicatorEnd(this._number, searchRange.Start);
            int foundEnd = NativeScintilla.IndicatorEnd(this._number, foundStart);
            if (foundStart < 0 || foundStart > searchRange.End || foundStart == foundEnd)
                return null;


            return new Range(foundStart, foundEnd, Scintilla);
        }


        public Range Search(Range searchRange, Range startingAfterRange)
        {
            int start = startingAfterRange.End;
            if (start > NativeScintilla.GetTextLength())
                return null;

            int foundStart = NativeScintilla.IndicatorEnd(this._number, start);
            int foundEnd = NativeScintilla.IndicatorEnd(this._number, foundStart);
            if (foundStart < 0 || foundStart > searchRange.End || foundStart == foundEnd)
                return null;
            
            return new Range(foundStart, foundEnd, Scintilla);
        }


        public List<Range> SearchAll()
        {
            return this.SearchAll(Scintilla.GetRange());
        }


        public List<Range> SearchAll(Range searchRange)
        {
            Range foundRange = Scintilla.GetRange(-1, -1);

            var ret = new List<Range>();
            do
            {
                foundRange = this.Search(searchRange, foundRange);
                if (foundRange != null)
                    ret.Add(foundRange);
            }
            while (foundRange != null);
            return ret;
        }


        internal bool ShouldSerialize()
        {
            return this.ShouldSerializeColor() ||
                this.ShouldSerializeIsDrawnUnder() ||
                this.ShouldSerializeStyle();
        }


        private bool ShouldSerializeColor()
        {
            return this.Color != this.GetDefaultColor();
        }


        private bool ShouldSerializeIsDrawnUnder()
        {
            return this.IsDrawnUnder;
        }


        private bool ShouldSerializeStyle()
        {
            return this.Style != this.GetDefaultStyle();
        }


        public override string ToString()
        {
            return "Indicator" + this._number;
        }

        #endregion Methods


        #region Properties

        public Color Color
        {
            get
            {
                if (Scintilla.ColorBag.ContainsKey(this + ".Color"))
                    return Scintilla.ColorBag[this + ".Color"];

                return Utilities.RgbToColor(NativeScintilla.IndicGetFore(this._number));
            }
            set
            {
                Scintilla.ColorBag[this + ".Color"] = value;
                NativeScintilla.IndicSetFore(this._number, Utilities.ColorToRgb(value));
            }
        }


        public bool IsDrawnUnder
        {
            get
            {
                return NativeScintilla.IndicGetUnder(this._number);
            }
            set
            {
                NativeScintilla.IndicSetUnder(this._number, value);
            }
        }


        public int Number
        {
            get
            {
                return this._number;
            }
            set
            {
                this._number = value;
            }
        }


        public IndicatorStyle Style
        {
            get
            {
                return (IndicatorStyle)NativeScintilla.IndicGetStyle(this._number);
            }
            set
            {
                NativeScintilla.IndicSetStyle(this._number, (int)value);
            }
        }

        #endregion Properties


        #region Constructors

        internal Indicator(int number, Scintilla scintilla) : base(scintilla)
        {
            this._number = number;
        }

        #endregion Constructors
    }
}
