﻿using System;
using System.IO;
using System.Windows.Forms;
using ARCed.Helpers;

namespace ARCed.Plugins
{
	/// <summary>
	/// Static class that acts as the interface for storing and invoking plugins.
	/// It ensures that all plugins are correctly formatted and searches them for
	/// content before adding their entries.
	/// </summary>
	public static class Registry
	{
		#region Private Fields

		private static RegistryEntryCollection _entries;
		private static PluginCollection _plugins;

		#endregion

		#region Public Properties

		/// <summary>
		/// Gets a collection of all currently registered plugin content
		/// </summary>
		public static RegistryEntryCollection Entries 
		{
			get
			{
				if (_entries == null)
					_entries = new RegistryEntryCollection();
				return _entries;
			}
		}

		/// <summary>
		/// Gets a list of loaded plugins
		/// </summary>
		public static PluginCollection Plugins 
		{
			get
			{
				if (_plugins == null)
					_plugins = new PluginCollection();
				return _plugins;
			}
		}

		#endregion

		#region Public Methods

		/// <summary>
		/// Loads a a plugin from file. The assembly is searched for useable content and 
		/// registered with the Editor
		/// </summary>
		/// <param name="filename"></param>
		public static void Load(string filename)
		{
			string ext = Path.GetExtension(filename);
			if (File.Exists(filename) && (ext == ".exe" || ext == ".dll"))
			{
				Plugin plugin = new Plugin(filename, Editor.MainInstance);
				if (plugin.IsLoaded)
				{
					Plugins.Add(plugin);
					Entries.AddRange(plugin.GetEntries());
					return;
				}
			}
			MessageBox.Show(String.Format("Plugin \"{0}\" failed to load.", filename), 
				"Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning);
		}

		/// <summary>
		/// Loads all plugins from the default plugin folder
		/// </summary>
		/// <remarks>Acceptable formats are "*.exe" and "*.dll"</remarks>
		public static void LoadAll()
		{
			string[] filters = { "*.dll", "*.exe" };
			foreach (string filter in filters)
			{
				string[] files = Directory.GetFiles(PathHelper.PluginDirectory, filter);
				foreach (string filename in files)
					Load(filename);
			}
		}

		/// <summary>
		/// Unloads the given plugin and all associated registry entries
		/// </summary>
		/// <param name="plugin">Plugin to remove</param>
		public static void Unload(Plugin plugin)
		{
			foreach (RegistryEntry entry in plugin.GetEntries())
				Entries.Remove(entry);
			Plugins.Remove(plugin);
		}

		/// <summary>
		/// Unloads the given entry from the registry
		/// </summary>
		/// <param name="entry">The entry to remove</param>
		public static void Unload(RegistryEntry entry)
		{
			Entries.Remove(entry);
		}

		/// <summary>
		/// Unloads all registry entries and plugins
		/// </summary>
		public static void UnloadAll()
		{
			Entries.Clear();
			Plugins.Clear();
		}

		#endregion
	}
}
