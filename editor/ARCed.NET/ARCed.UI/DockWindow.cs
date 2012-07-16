#region Using Directives

using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

#endregion

namespace ARCed.UI
{
	[ToolboxItem(false)]
	public partial class DockWindow : Panel, INestedPanesContainer, ISplitterDragSource
	{
        private readonly DockPanel _mDockPanel;
        private readonly DockState _mDockState;
        private readonly SplitterControl _mSplitter;
        private readonly NestedPaneCollection _mNestedPanes;

		internal DockWindow(DockPanel dockPanel, DockState dockState)
		{
			this._mNestedPanes = new NestedPaneCollection(this);
			this._mDockPanel = dockPanel;
			this._mDockState = dockState;
			Visible = false;

			SuspendLayout();

			if (DockState == DockState.DockLeft || DockState == DockState.DockRight ||
				DockState == DockState.DockTop || DockState == DockState.DockBottom)
			{
				this._mSplitter = new SplitterControl();
				Controls.Add(this._mSplitter);
			}

			if (DockState == DockState.DockLeft)
			{
				Dock = DockStyle.Left;
				this._mSplitter.Dock = DockStyle.Right;
			}
			else if (DockState == DockState.DockRight)
			{
				Dock = DockStyle.Right;
				this._mSplitter.Dock = DockStyle.Left;
			}
			else if (DockState == DockState.DockTop)
			{
				Dock = DockStyle.Top;
				this._mSplitter.Dock = DockStyle.Bottom;
			}
			else if (DockState == DockState.DockBottom)
			{
				Dock = DockStyle.Bottom;
				this._mSplitter.Dock = DockStyle.Top;
			}
			else if (DockState == DockState.Document)
			{
				Dock = DockStyle.Fill;
			}

			ResumeLayout();
		}

		public VisibleNestedPaneCollection VisibleNestedPanes
		{
			get	{	return NestedPanes.VisibleNestedPanes;	}
		}

		public NestedPaneCollection NestedPanes
		{
			get	{	return this._mNestedPanes;	}
		}

		public DockPanel DockPanel
		{
			get	{	return this._mDockPanel;	}
		}

		public DockState DockState
		{
			get	{	return this._mDockState;	}
		}

		public bool IsFloat
		{
			get	{	return DockState == DockState.Float;	}
		}

		internal DockPane DefaultPane
		{
			get	{	return VisibleNestedPanes.Count == 0 ? null : VisibleNestedPanes[0];	}
		}

		public virtual Rectangle DisplayingRectangle
		{
			get
			{
				Rectangle rect = ClientRectangle;
				// if DockWindow is document, exclude the border
				if (DockState == DockState.Document)
				{
					rect.X += 1;
					rect.Y += 1;
					rect.Width -= 2;
					rect.Height -= 2;
				}
				// exclude the splitter
				else if (DockState == DockState.DockLeft)
					rect.Width -= Measures.SplitterSize;
				else if (DockState == DockState.DockRight)
				{
					rect.X += Measures.SplitterSize;
					rect.Width -= Measures.SplitterSize;
				}
				else if (DockState == DockState.DockTop)
					rect.Height -= Measures.SplitterSize;
				else if (DockState == DockState.DockBottom)
				{
					rect.Y += Measures.SplitterSize;
					rect.Height -= Measures.SplitterSize;
				}

				return rect;
			}
		}

		protected override void OnPaint(PaintEventArgs e)
		{
			// if DockWindow is document, draw the border
            if (DockState == DockState.Document)
                e.Graphics.DrawRectangle(SystemPens.ControlDark, ClientRectangle.X, ClientRectangle.Y, ClientRectangle.Width - 1, ClientRectangle.Height - 1);

			base.OnPaint(e);
		}

		protected override void OnLayout(LayoutEventArgs levent)
		{
			VisibleNestedPanes.Refresh();
			if (VisibleNestedPanes.Count == 0)
			{
                if (Visible)
                    Visible = false;
			}
			else if (!Visible)
			{
				Visible = true;
				VisibleNestedPanes.Refresh();
			}

			base.OnLayout (levent);
		}

        #region ISplitterDragSource Members

        void ISplitterDragSource.BeginDrag(Rectangle rectSplitter)
        {
        }

        void ISplitterDragSource.EndDrag()
        {
        }

        bool ISplitterDragSource.IsVertical
        {
            get { return (DockState == DockState.DockLeft || DockState == DockState.DockRight); }
        }

        Rectangle ISplitterDragSource.DragLimitBounds
        {
            get
            {
                Rectangle rectLimit = DockPanel.DockArea;
                Point location;
                if ((ModifierKeys & Keys.Shift) == 0)
                    location = Location;
                else
                    location = DockPanel.DockArea.Location;

                if (((ISplitterDragSource)this).IsVertical)
                {
                    rectLimit.X += MeasurePane.MinSize;
                    rectLimit.Width -= 2 * MeasurePane.MinSize;
                    rectLimit.Y = location.Y;
                    if ((ModifierKeys & Keys.Shift) == 0)
                        rectLimit.Height = Height;
                }
                else
                {
                    rectLimit.Y += MeasurePane.MinSize;
                    rectLimit.Height -= 2 * MeasurePane.MinSize;
                    rectLimit.X = location.X;
                    if ((ModifierKeys & Keys.Shift) == 0)
                        rectLimit.Width = Width;
                }

                return DockPanel.RectangleToScreen(rectLimit);
            }
        }

        void ISplitterDragSource.MoveSplitter(int offset)
        {
            if ((ModifierKeys & Keys.Shift) != 0)
                SendToBack();

            Rectangle rectDockArea = DockPanel.DockArea;
            if (DockState == DockState.DockLeft && rectDockArea.Width > 0)
            {
                if (DockPanel.DockLeftPortion > 1)
                    DockPanel.DockLeftPortion = Width + offset;
                else
                    DockPanel.DockLeftPortion += (offset) / (double)rectDockArea.Width;
            }
            else if (DockState == DockState.DockRight && rectDockArea.Width > 0)
            {
                if (DockPanel.DockRightPortion > 1)
                    DockPanel.DockRightPortion = Width - offset;
                else
                    DockPanel.DockRightPortion -= (offset) / (double)rectDockArea.Width;
            }
            else if (DockState == DockState.DockBottom && rectDockArea.Height > 0)
            {
                if (DockPanel.DockBottomPortion > 1)
                    DockPanel.DockBottomPortion = Height - offset;
                else
                    DockPanel.DockBottomPortion -= (offset) / (double)rectDockArea.Height;
            }
            else if (DockState == DockState.DockTop && rectDockArea.Height > 0)
            {
                if (DockPanel.DockTopPortion > 1)
                    DockPanel.DockTopPortion = Height + offset;
                else
                    DockPanel.DockTopPortion += (offset) / (double)rectDockArea.Height;
            }
        }

        #region IDragSource Members

        Control IDragSource.DragControl
        {
            get { return this; }
        }

        #endregion
        #endregion
    }
}
