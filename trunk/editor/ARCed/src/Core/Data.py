'''
Created on Jan 18, 2011

'''
import os
import sys

import ConfigParser

import wx

import Kernel
from Kernel import Manager as KM

def NewProject(mainwindow):
    dlg = KM.get_component("NewProjectDialog").object(mainwindow)
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        mode, name, path = dlg.getdata()
        Kernel.Global.Mode = mode
        Kernel.Global.Title = name
        KM.raise_event("EventMode")
        projectcreator = KM.get_component(*Kernel.Global.ProjectCreators[mode]).object()
        projectcreator.Create(path, name)
        Kernel.Global.CurrentProjectDir = path
        Kernel.Global.ProjectOpen = True
    dlg.Destroy()

def OpenProject(mainwindow, filehistory, path=""):
    if Kernel.Global.ProjectOpen:
        message = "Do you want to save the currently open project?"
        caption = "There is already an open project"
        dlg = wx.MessageDialog(mainwindow, message, caption, style=wx.YES_NO |
                               wx.YES_DEFAULT)
        result = dlg.ShowModal()
        if result == wx.YES:
            SaveProject(mainwindow)
    if not path == "":
        Kernel.Global.CurrentProjectDir = path
        config = ConfigParser.ConfigParser()
        config.read(os.path.normpath(path))
        Kernel.Global.Title = config.get("Project", "title")
        Kernel.Global.Mode = config.get("Project", "type")
        Kernel.Global.config = config
        KM.raise_event("EventMode")
        path = os.path.dirname(path)
        Kernel.Global.CurrentProjectDir = path
        Kernel.Global.ProjectOpen = True
        loader = KM.get_component("ProjectLoader",
                                  str(Kernel.Global.Mode)).object()
        loader.Load(os.path.normpath(path), mainwindow)
    else:
        wildcard = "ARC Project File (*.arcproj)|*.arcproj"
        defaultpath = (os.path.join(wx.StandardPaths.Get().GetDocumentsDir(),
                                    "ARC"))
        dlg = wx.FileDialog(mainwindow, message="Choose a file",
            defaultDir=defaultpath,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            config = ConfigParser.ConfigParser()
            config.read(os.path.normpath(dlg.GetPath()))
            filehistory.AddFileToHistory(dlg.GetPath())
            Kernel.Global.Title = config.get("Project", "title")
            Kernel.Global.Mode = config.get("Project", "type")
            Kernel.Global.config = config
            KM.raise_event("EventMode")
            path = dlg.GetDirectory()
            Kernel.Global.CurrentProjectDir = path
            Kernel.Global.ProjectOpen = True
            dlg.Destroy()
            loader = KM.get_component("ProjectLoader",
                                      str(Kernel.Global.Mode)).object()

            loader.Load(os.path.normpath(path), mainwindow)

def SaveProject(mainwindow):
    saver = KM.get_component("ProjectSaver", Kernel.Global.Mode).object()
    saver.Save(Kernel.Global.CurrentProjectDir)

def SaveProjectAS(mainwindow, filehistory):
    wildcard = "ARC Project File (*.arcproj)|*.arcproj|"
    defaultpath = (os.path.join(wx.StandardPaths.Get().GetDocumentsDir(),
                                "ARC"))
    dlg = wx.DirDialog(mainwindow, "Choose a Location:",
                       defaultPath=defaultpath,
                       style=wx.DD_DEFAULT_STYLE
                       | wx.DD_NEW_DIR_BUTTON)
    if dlg.ShowModal() == wx.ID_OK:
        location = dlg.GetPath()
        filehistory.AddFileToHistory(os.path.join(location, "Project.arcproj"))
        saver = KM.get_component("ProjectCreator", Kernel.Global.Mode).object()
        saver.Create(location, Kernel.Global.Title, saveas=True)

class ARCProjectCreator(object):
    
    def __init__(self):
        self.project = None
        
    def Create(self, path, title, saveas=False):
        config = ConfigParser.ConfigParser()
        config.add_section("Project")
        config.set("Project", "title", title)
        config.set("Project", "type", "ARC")
        filename = os.path.join(path, "Project.arcproj")
        f = open(filename, 'w')
        config.write(f)
        f.close()
        Kernel.Global.Project = self.project
        saver = ARCProjectSaver()
        saver.Save(path)
        if not saveas:
            KM.raise_event("EventRefreshProject")
            
class ARCProjectSaver(object):
    def __init__(self):
        self.project = Kernel.Global.Project

    def Save(self, path):
        dirpath = os.path.join(path, "Data")
        if not os.path.exists(dirpath) and not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        #TODO Finish after data struture is decided


    def dump_data(self, data, filename):
        f = open(filename, 'wb')
        cPickle.dump(data, f, protocol= -1)
        f.close()