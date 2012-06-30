﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using ARCed.Controls;

namespace ARCed.Database.Troops
{
	public partial class BattleTestDialog : Form
	{
		public BattleTestDialog()
		{
			InitializeComponent();
			if (Project.BTActors == null)
				Project.BTActors = new List<dynamic>() { Project.Data.Actors[0] };
			numericUpDownActors.Value = Project.BTActors.Count;
		}

		private void numericUpDownActors_ValueChanged(object sender, EventArgs e)
		{
			int value = (int)numericUpDownActors.Value;
			if (value < tabControlActors.TabCount)
			{
				for (int i = tabControlActors.TabCount - 1; i >= value; i--)
				{
					tabControlActors.TabPages.RemoveAt(i);
					Project.BTActors.RemoveAt(i);
				}
			}
			else
			{
				tabControlActors.SuspendLayout();
				for (int i = tabControlActors.TabCount; i < value; i++)
				{
					TabPage page = new TabPage((i + 1).ToString());
					BattleTestActorPanel panel = new BattleTestActorPanel();
					page.Controls.Add(panel);
					panel.Dock = DockStyle.Fill;
					tabControlActors.TabPages.Add(page);
					Project.BTActors.Add(Project.Data.Actors[0]);
				}
				tabControlActors.ResumeLayout(true);
			}
		}
	}
}
