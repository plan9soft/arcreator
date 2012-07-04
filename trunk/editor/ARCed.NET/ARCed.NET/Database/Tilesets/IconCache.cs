﻿using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using ARCed.Helpers;
using Microsoft.Xna.Framework.Graphics;

namespace ARCed.Database.Tilesets
{
	public static class IconCache
	{
		#region Constants

		/// <summary>
		/// Bit value indicating down direction is impassable.
		/// </summary>
		private const int DOWN = 0x01;
		/// <summary>
		/// Bit value indicating left direction is impassable.
		/// </summary>
		private const int LEFT = 0x02;
		/// <summary>
		/// Bit value indicating right direction is impassable.
		/// </summary>
		private const int RIGHT = 0x04;
		/// <summary>
		/// Bit value indicating up direction is impassable.
		/// </summary>
		private const int UP = 0x08;
		/// <summary>
		/// Bit value indicating all directions are impassable.
		/// </summary>
		private const int ALL = 0x01 | 0x02 | 0x04 | 0x08;
		/// <summary>
		/// Bit value indicating a bush flag.
		/// </summary>
		private const int BUSH = 0x40;
		/// <summary>
		/// Bit value indicating a counter flag.
		/// </summary>
		private const int COUNTER = 0x80;

		#endregion

		#region Private Fields

		private static Dictionary<string, Texture2D> _cache =
			new Dictionary<string, Texture2D>();
		public static GraphicsDevice GraphicsDevice { get; set; }

		#endregion

		#region Private Methods

		private static Bitmap GetBitmap(string key)
		{
			string name = String.Format("ARCed.Resources.TilesetIcons.{0}.png", key);
			using (Stream stream = SystemHelper.ARCedAssembly.GetManifestResourceStream(name))
				return new Bitmap(stream);
		}

		private static Texture2D CacheTexture(string key)
		{
			if (_cache.ContainsKey(key))
				return _cache[key];
			_cache[key] = GetBitmap(key).ToTexture(GraphicsDevice);
			return _cache[key];
		}

		#endregion

		#region Public Methods

		/// <summary>
		/// Caches and returns an icon used for Passage.
		/// </summary>
		/// <param name="passage">Passage value</param>
		/// <returns>Cached texture</returns>
		public static Texture2D Passage(int passage)
		{
			passage &= ~BUSH;
			passage &= ~COUNTER;
			string key = (passage == 0) ? "PassageCircle" : "PassageX";
			return CacheTexture(key);
		}

		/// <summary>
		/// Caches and returns an icon used for Priority.
		/// </summary>
		/// <param name="passage">Priority value</param>
		/// <returns>Cached texture</returns>
		public static Texture2D Priority(int priority)
		{
			string key = String.Format("Priority{0}", priority);
			return CacheTexture(key);
		}

		/// <summary>
		/// Caches and returns an icon used for Counter flags.
		/// </summary>
		/// <param name="passage">Passage value</param>
		/// <returns>Cached texture</returns>
		public static Texture2D Counter(int passage)
		{
			string key = ((passage & COUNTER) == COUNTER) ? "Counter" : "Priority0";
			return CacheTexture(key);
		}

		/// <summary>
		/// Caches and returns an icon used for Bush flags.
		/// </summary>
		/// <param name="passage">Passage value</param>
		/// <returns>Cached texture</returns>
		public static Texture2D Bush(int passage)
		{
			string key = ((passage & BUSH) == BUSH) ? "Bush" : "Priority0";
			return CacheTexture(key);
		}

		/// <summary>
		/// Caches and returns an icon used for Terrain Tags.
		/// </summary>
		/// <param name="passage">Terrain tag value</param>
		/// <returns>Cached texture</returns>
		public static Texture2D Terrain(int terrain)
		{
			string key = String.Format("Terrain{0}", terrain);
			return CacheTexture(key);
		}

		/// <summary>
		/// Caches and returns an icon used for Passage 4-Dir.
		/// </summary>
		/// <param name="passage">Passage value</param>
		/// <returns>Cached texture</returns>
		public static Texture2D Passage4Dir(int passage)
		{
			passage &= ~BUSH;
			passage &= ~COUNTER;
			string key = String.Format("Passage{0}", passage);
			if (_cache.ContainsKey(key))
				return _cache[key];
			if (passage == 0)
				return CacheTexture("PassageAll");
			if ((passage & ALL) == ALL)
				return CacheTexture("PassageNone");
			{
				Bitmap b = GetBitmap("PassageNone");
				using (Graphics g = Graphics.FromImage(b))
				{
					if ((passage & DOWN) != DOWN)
						g.DrawImage(GetBitmap("PassageDown"), PointF.Empty);
					if ((passage & LEFT) != LEFT)
						g.DrawImage(GetBitmap("PassageLeft"), PointF.Empty);
					if ((passage & RIGHT) != RIGHT)
						g.DrawImage(GetBitmap("PassageRight"), PointF.Empty);
					if ((passage & UP) != UP)
						g.DrawImage(GetBitmap("PassageUp"), PointF.Empty);
				}
				_cache[key] = b.ToTexture(GraphicsDevice);
				return _cache[key];
			}
		}

		#endregion
	}
}