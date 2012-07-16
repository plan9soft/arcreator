#region Using Directives

using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Windows.Forms;

#endregion

namespace ARCed.UI
{
	public abstract class AutoHideStripBase : Control
	{
        [SuppressMessage("Microsoft.Design", "CA1034:NestedTypesShouldNotBeVisible")]
        protected class Tab : IDisposable
        {
            private readonly IDockContent m_content;

            protected internal Tab(IDockContent content)
            {
                m_content = content;
            }

            ~Tab()
            {
                Dispose(false);
            }

            public IDockContent Content
            {
                get { return m_content; }
            }

            public void Dispose()
            {
                Dispose(true);
                GC.SuppressFinalize(this);
            }

            protected virtual void Dispose(bool disposing)
            {
            }
        }

        [SuppressMessage("Microsoft.Design", "CA1034:NestedTypesShouldNotBeVisible")]
        protected sealed class TabCollection : IEnumerable<Tab>
        {
            #region IEnumerable Members
            IEnumerator<Tab> IEnumerable<Tab>.GetEnumerator()
            {
                for (int i = 0; i < Count; i++)
                    yield return this[i];
            }

            IEnumerator IEnumerable.GetEnumerator()
            {
                for (int i = 0; i < Count; i++)
                    yield return this[i];
            }
            #endregion

            internal TabCollection(DockPane pane)
            {
                m_dockPane = pane;
            }

            private readonly DockPane m_dockPane;
            public DockPane DockPane
            {
                get { return m_dockPane; }
            }

            public DockPanel DockPanel
            {
                get { return DockPane.DockPanel; }
            }

            public int Count
            {
                get { return DockPane.DisplayingContents.Count; }
            }

            public Tab this[int index]
            {
                get
                {
                    IDockContent content = DockPane.DisplayingContents[index];
                    if (content == null)
                        throw (new ArgumentOutOfRangeException("index"));
                    if (content.DockHandler.AutoHideTab == null)
                        content.DockHandler.AutoHideTab = (DockPanel.AutoHideStripControl.CreateTab(content));
                    return content.DockHandler.AutoHideTab as Tab;
                }
            }

            public bool Contains(Tab tab)
            {
                return (IndexOf(tab) != -1);
            }

            public bool Contains(IDockContent content)
            {
                return (IndexOf(content) != -1);
            }

            public int IndexOf(Tab tab)
            {
                if (tab == null)
                    return -1;

                return IndexOf(tab.Content);
            }

            public int IndexOf(IDockContent content)
            {
                return DockPane.DisplayingContents.IndexOf(content);
            }
        }

        [SuppressMessage("Microsoft.Design", "CA1034:NestedTypesShouldNotBeVisible")]
        protected class Pane : IDisposable
        {
            private readonly DockPane m_dockPane;

            protected internal Pane(DockPane dockPane)
            {
                m_dockPane = dockPane;
            }

            ~Pane()
            {
                Dispose(false);
            }

            public DockPane DockPane
            {
                get { return m_dockPane; }
            }

            public TabCollection AutoHideTabs
            {
                get
                {
                    if (DockPane.AutoHideTabs == null)
                        DockPane.AutoHideTabs = new TabCollection(DockPane);
                    return DockPane.AutoHideTabs as TabCollection;
                }
            }

            public void Dispose()
            {
                Dispose(true);
                GC.SuppressFinalize(this);
            }

            protected virtual void Dispose(bool disposing)
            {
            }
        }

        [SuppressMessage("Microsoft.Design", "CA1034:NestedTypesShouldNotBeVisible")]
        protected sealed class PaneCollection : IEnumerable<Pane>
        {
            private class AutoHideState
            {
                private readonly DockState _mDockState;
                private bool _mSelected;

                public AutoHideState(DockState dockState)
                {
                    this._mDockState = dockState;
                }

                public DockState DockState
                {
                    get { return this._mDockState; }
                }

                public bool Selected
                {
                    get { return this._mSelected; }
                    set { this._mSelected = value; }
                }
            }

            private class AutoHideStateCollection
            {
                private readonly AutoHideState[] _mStates;

                public AutoHideStateCollection()
                {
                    this._mStates = new[]	{	
												new AutoHideState(DockState.DockTopAutoHide),
												new AutoHideState(DockState.DockBottomAutoHide),
												new AutoHideState(DockState.DockLeftAutoHide),
												new AutoHideState(DockState.DockRightAutoHide)
											};
                }

                public AutoHideState this[DockState dockState]
                {
                    get
                    {
                        for (int i = 0; i < this._mStates.Length; i++)
                        {
                            if (this._mStates[i].DockState == dockState)
                                return this._mStates[i];
                        }
                        throw new ArgumentOutOfRangeException("dockState");
                    }
                }

                public bool ContainsPane(DockPane pane)
                {
                    if (pane.IsHidden)
                        return false;

                    for (int i = 0; i < this._mStates.Length; i++)
                    {
                        if (this._mStates[i].DockState == pane.DockState && this._mStates[i].Selected)
                            return true;
                    }
                    return false;
                }
            }

            internal PaneCollection(DockPanel panel, DockState dockState)
            {
                this._mDockPanel = panel;
                this._mStates = new AutoHideStateCollection();
                States[DockState.DockTopAutoHide].Selected = (dockState == DockState.DockTopAutoHide);
                States[DockState.DockBottomAutoHide].Selected = (dockState == DockState.DockBottomAutoHide);
                States[DockState.DockLeftAutoHide].Selected = (dockState == DockState.DockLeftAutoHide);
                States[DockState.DockRightAutoHide].Selected = (dockState == DockState.DockRightAutoHide);
            }

            private readonly DockPanel _mDockPanel;
            public DockPanel DockPanel
            {
                get { return this._mDockPanel; }
            }

            private readonly AutoHideStateCollection _mStates;
            private AutoHideStateCollection States
            {
                get { return this._mStates; }
            }

            public int Count
            {
                get
                {
                    int count = 0;
                    foreach (DockPane pane in DockPanel.Panes)
                    {
                        if (States.ContainsPane(pane))
                            count++;
                    }

                    return count;
                }
            }

            public Pane this[int index]
            {
                get
                {
                    int count = 0;
                    foreach (DockPane pane in DockPanel.Panes)
                    {
                        if (!States.ContainsPane(pane))
                            continue;

                        if (count == index)
                        {
                            if (pane.AutoHidePane == null)
                                pane.AutoHidePane = DockPanel.AutoHideStripControl.CreatePane(pane);
                            return pane.AutoHidePane as Pane;
                        }

                        count++;
                    }
                    throw new ArgumentOutOfRangeException("index");
                }
            }

            public bool Contains(Pane pane)
            {
                return (IndexOf(pane) != -1);
            }

            public int IndexOf(Pane pane)
            {
                if (pane == null)
                    return -1;

                int index = 0;
                foreach (DockPane dockPane in DockPanel.Panes)
                {
                    if (!States.ContainsPane(pane.DockPane))
                        continue;

                    if (pane == dockPane.AutoHidePane)
                        return index;

                    index++;
                }
                return -1;
            }

            #region IEnumerable Members

            IEnumerator<Pane> IEnumerable<Pane>.GetEnumerator()
            {
                for (int i = 0; i < Count; i++)
                    yield return this[i];
            }

            IEnumerator IEnumerable.GetEnumerator()
            {
                for (int i = 0; i < Count; i++)
                    yield return this[i];
            }

            #endregion
        }

		protected AutoHideStripBase(DockPanel panel)
		{
			this._mDockPanel = panel;
			this._mPanesTop = new PaneCollection(panel, DockState.DockTopAutoHide);
			this._mPanesBottom = new PaneCollection(panel, DockState.DockBottomAutoHide);
			this._mPanesLeft = new PaneCollection(panel, DockState.DockLeftAutoHide);
			this._mPanesRight = new PaneCollection(panel, DockState.DockRightAutoHide);

			SetStyle(ControlStyles.OptimizedDoubleBuffer, true);
			SetStyle(ControlStyles.Selectable, false);
		}

        private readonly DockPanel _mDockPanel;
		protected DockPanel DockPanel
		{
			get	{	return this._mDockPanel;	}
		}

        private readonly PaneCollection _mPanesTop;
		protected PaneCollection PanesTop
		{
			get	{	return this._mPanesTop;	}
		}

        private readonly PaneCollection _mPanesBottom;
		protected PaneCollection PanesBottom
		{
			get	{	return this._mPanesBottom;	}
		}

        private readonly PaneCollection _mPanesLeft;
		protected PaneCollection PanesLeft
		{
			get	{	return this._mPanesLeft;	}
		}

        private readonly PaneCollection _mPanesRight;
		protected PaneCollection PanesRight
		{
			get	{	return this._mPanesRight;	}
		}

		protected PaneCollection GetPanes(DockState dockState)
		{
			if (dockState == DockState.DockTopAutoHide)
				return PanesTop;
			else if (dockState == DockState.DockBottomAutoHide)
				return PanesBottom;
			else if (dockState == DockState.DockLeftAutoHide)
				return PanesLeft;
			else if (dockState == DockState.DockRightAutoHide)
				return PanesRight;
			else
				throw new ArgumentOutOfRangeException("dockState");
		}

        internal int GetNumberOfPanes(DockState dockState)
        {
            return GetPanes(dockState).Count;
        }

		protected Rectangle RectangleTopLeft
		{
			get
			{	
				int height = MeasureHeight();
				return PanesTop.Count > 0 && PanesLeft.Count > 0 ? new Rectangle(0, 0, height, height) : Rectangle.Empty;
			}
		}

		protected Rectangle RectangleTopRight
		{
			get
			{
				int height = MeasureHeight();
				return PanesTop.Count > 0 && PanesRight.Count > 0 ? new Rectangle(Width - height, 0, height, height) : Rectangle.Empty;
			}
		}

		protected Rectangle RectangleBottomLeft
		{
			get
			{
				int height = MeasureHeight();
				return PanesBottom.Count > 0 && PanesLeft.Count > 0 ? new Rectangle(0, Height - height, height, height) : Rectangle.Empty;
			}
		}

		protected Rectangle RectangleBottomRight
		{
			get
			{
				int height = MeasureHeight();
				return PanesBottom.Count > 0 && PanesRight.Count > 0 ? new Rectangle(Width - height, Height - height, height, height) : Rectangle.Empty;
			}
		}

		protected internal Rectangle GetTabStripRectangle(DockState dockState)
		{
			int height = MeasureHeight();
			if (dockState == DockState.DockTopAutoHide && PanesTop.Count > 0)
				return new Rectangle(RectangleTopLeft.Width, 0, Width - RectangleTopLeft.Width - RectangleTopRight.Width, height);
			else if (dockState == DockState.DockBottomAutoHide && PanesBottom.Count > 0)
				return new Rectangle(RectangleBottomLeft.Width, Height - height, Width - RectangleBottomLeft.Width - RectangleBottomRight.Width, height);
			else if (dockState == DockState.DockLeftAutoHide && PanesLeft.Count > 0)
				return new Rectangle(0, RectangleTopLeft.Width, height, Height - RectangleTopLeft.Height - RectangleBottomLeft.Height);
			else if (dockState == DockState.DockRightAutoHide && PanesRight.Count > 0)
				return new Rectangle(Width - height, RectangleTopRight.Width, height, Height - RectangleTopRight.Height - RectangleBottomRight.Height);
			else
				return Rectangle.Empty;
		}

		private GraphicsPath m_displayingArea;
		private GraphicsPath DisplayingArea
		{
			get
			{
				if (m_displayingArea == null)
					m_displayingArea = new GraphicsPath();

				return m_displayingArea;
			}
		}

		private void SetRegion()
		{
			DisplayingArea.Reset();
			DisplayingArea.AddRectangle(RectangleTopLeft);
			DisplayingArea.AddRectangle(RectangleTopRight);
			DisplayingArea.AddRectangle(RectangleBottomLeft);
			DisplayingArea.AddRectangle(RectangleBottomRight);
			DisplayingArea.AddRectangle(GetTabStripRectangle(DockState.DockTopAutoHide));
			DisplayingArea.AddRectangle(GetTabStripRectangle(DockState.DockBottomAutoHide));
			DisplayingArea.AddRectangle(GetTabStripRectangle(DockState.DockLeftAutoHide));
			DisplayingArea.AddRectangle(GetTabStripRectangle(DockState.DockRightAutoHide));
			Region = new Region(DisplayingArea);
		}

		protected override void OnMouseDown(MouseEventArgs e)
		{
			base.OnMouseDown(e);

			if (e.Button != MouseButtons.Left)
				return;

			IDockContent content = HitTest();
			if (content == null)
				return;

			content.DockHandler.Activate();
		}

		protected override void OnMouseHover(EventArgs e)
		{
			base.OnMouseHover(e);

			IDockContent content = HitTest();
			if (content != null && DockPanel.ActiveAutoHideContent != content)
				DockPanel.ActiveAutoHideContent = content;

			// requires further tracking of mouse hover behavior,
            ResetMouseEventArgs();
		}

		protected override void OnLayout(LayoutEventArgs levent)
		{
			RefreshChanges();
			base.OnLayout (levent);
		}

		internal void RefreshChanges()
		{
            if (IsDisposed)
                return;

			SetRegion();
			OnRefreshChanges();
		}

		protected virtual void OnRefreshChanges()
		{
		}

		protected internal abstract int MeasureHeight();

		private IDockContent HitTest()
		{
			Point ptMouse = PointToClient(MousePosition);
			return HitTest(ptMouse);
		}

        protected virtual Tab CreateTab(IDockContent content)
        {
            return new Tab(content);
        }

        protected virtual Pane CreatePane(DockPane dockPane)
        {
            return new Pane(dockPane);
        }

		protected abstract IDockContent HitTest(Point point);
	}
}
