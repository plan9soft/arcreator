'''
Created on Jan 17, 2011

'''

import os
import sys
import copy

import wx

try:
    from agw import aui
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    
import  wx.lib.scrolledpanel as scrolled
    


# this is for if we need to use pygame ever
#===============================================================================
# #do stuff to use pygame with out a window
# os.environ["SDL_VIDEODRIVER"] = "dummy"
# if 1:
#    #some platforms might need to init the display for some parts of pygame.
#    import pygame
#    pygame.init()
#    screen = pygame.display.set_mode((1, 1))
#===============================================================================

import Kernel
from Kernel import Manager as KM

class MainToolbar(object):
    def __init__(self, toolbar, mainwindow):
        self.toolbar = toolbar
        self.mainwindow = mainwindow

        self.toolbar.SetToolBitmapSize(wx.Size(16, 16))

        #get bitmaps
        newbmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16))
        openbmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16))
        savebmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16, 16))
        undobmp = wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, (16, 16))
        redobmp = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, (16, 16))
        copybmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, (16, 16))
        cutbmp = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, (16, 16))
        pastebmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (16, 16))
        #set up ids
        self.newid = wx.NewId()
        self.openid = wx.NewId()
        self.saveid = wx.NewId()
        self.redoid = wx.NewId()
        self.undoid = wx.NewId()
        self.copyid = wx.NewId()
        self.cutid = wx.NewId()
        self.pasteid = wx.NewId()
        #add the tools
        self.toolbar.AddSimpleTool(self.newid, "New", newbmp,
                                   "Create a new project")
        self.toolbar.AddSimpleTool(self.openid, "Open", openbmp,
                                   "Open a ARC Project")
        self.toolbar.AddSimpleTool(self.saveid, "Save", savebmp,
                                   "Save the current Project")
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(self.undoid, "Undo", undobmp,
                                   "Undo last action")
        self.toolbar.AddSimpleTool(self.redoid, "Redo", redobmp,
                                   "Redo last action")
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(self.cutid, "Cut", cutbmp,
                           "Cut selection and copy to the clipboard")
        self.toolbar.AddSimpleTool(self.copyid, "Copy", copybmp,
                           "Copy selection to the clipboard")
        self.toolbar.AddSimpleTool(self.pasteid, "Paste", pastebmp,
                           "Paste data from the clipboard")
        self.toolbar.Realize()

        self.toolbar.Bind(wx.EVT_TOOL, self.OnNew, id=self.newid)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnOpen, id=self.openid)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnSave, id=self.saveid)
        self.toolbar.Bind(wx.EVT_UPDATE_UI, self.uiupdate, id=self.saveid)

        self.toolbar.Bind(wx.EVT_TOOL, self.OnUndo, id=self.undoid)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnRedo, id=self.redoid)

        self.toolbar.Bind(wx.EVT_TOOL, self.OnCut, id=self.cutid)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnCopy, id=self.copyid)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnPaste, id=self.pasteid)

    def OnNew(self, event):
        newproject = KM.get_component("NewProjectHandler").object
        newproject(self.mainwindow)
        Kernel.GlobalObjects.get_value("FileHistory").Save(Kernel.GlobalObjects.get_value("programconfig"))

    def OnOpen(self, event):
        openproject = KM.get_component("OpenProjectHandler").object
        openproject(self.mainwindow, Kernel.GlobalObjects.get_value("FileHistory"))
        Kernel.GlobalObjects.get_value("FileHistory").Save(Kernel.GlobalObjects.get_value("programconfig"))

    def OnSave(self, event):
        saveproject = KM.get_component("SaveProjectHandler").object
        saveproject()
        Kernel.GlobalObjects.get_value("FileHistory").Save(Kernel.GlobalObjects.get_value("programconfig"))

    def OnUndo(self, event):
        pass

    def OnRedo(self, event):
        pass

    def OnCopy(self, event):
        pass

    def OnCut(self, event):
        pass

    def OnPaste(self, event):
        pass

    def uiupdate(self, event):
        if Kernel.GlobalObjects.has_key("ProjectOpen") and (Kernel.GlobalObjects.get_value("ProjectOpen") == True):
            event.Enable(True)
        else:
            event.Enable(False)

class MainStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

class RMXPMapTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.parent = parent
        KM.get_event("CoreEventRefreshProject").register(self.Refresh_Map_List)

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER,
                                             wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_OTHER,
                                             wx.Size(16, 16)))
        self.AssignImageList(imglist)

        root = self.AddRoot("Advanced RPG Creator Project", 0)
        items = []
        self.maps = {}

        self.Expand(root)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.onClose, self)

    def Refresh_Map_List(self):
        project = Kernel.GlobalObjects.get_value("PROJECT")
        mapinfos = project.getData("MapInfos")
        self.DeleteAllItems()
        root = self.AddRoot(str(project.getInfo("Title")), 0)
        stack = []
        for key, value in mapinfos.iteritems():
            if value.parent_id == 0:
                data = wx.TreeItemData([key, value.name])
                self.maps[key] = self.AppendItem(root, value.name, 1, data=data)
            else:
                if self.maps.has_key(value.parent_id):
                    data = wx.TreeItemData([key, value.name])
                    self.maps[key] = self.AppendItem(self.maps[value.parent_id],
                                                     value.name, 1, data=data)
                else:
                    stack.append([key, value])
        i = 0
        while len(stack) > 0:
            key, value = stack[i]
            if self.maps.has_key(value.parent_id):
                data = wx.TreeItemData([key, value.name])
                self.maps[key] = self.AppendItem(self.maps[key], value.name, 1,
                                                 data=data)
            else:
                stack.append([key, value])
            i += 1
        self.Expand(root)

    def onClose(self, event):
        KM.get_event("CoreEventRefreshProject").unregister(self.Refresh_Map_List)
        event.Skip()

class RMXPMapTreePanel(wx.Panel):
    def __init__(self, parent, mapEditerPanel=None):
        wx.Panel.__init__(self, parent)

        self.mapEditerPanel = mapEditerPanel

        #set up Sizer
        box = wx.BoxSizer(wx.VERTICAL)
        #set up tree
        self.treectrl = RMXPMapTreeCtrl(self, -1, wx.Point(0, 0),
                                        wx.Size(160, 250),
                                        wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        #add ctrls to sizer
        box.Add(self.treectrl, 1, wx.ALL | wx.EXPAND)
        #set sizer
        self.SetSizerAndFit(box)

        #bind events
        self.treectrl.Bind(wx.EVT_LEFT_DCLICK, self.TreeLeftDClick)

    def TreeLeftDClick(self, event):
        pt = event.GetPosition();
        item, flags = self.treectrl.HitTest(pt)
        if item:
            data = self.treectrl.GetItemData(item).GetData()
            if data:
                map_id, name = data
                self.mapEditerPanel.add_page(map_id, name)
        event.Skip()

# TODO: Redo the MapWindow ctrl for pygame
class WxRMXPMapWindow(wx.ScrolledWindow):
    Autotiles = [
                [[27, 28, 33, 34], [5, 28, 33, 34], [27, 6, 33, 34],
                 [5, 6, 33, 34], [27, 28, 33, 12], [5, 28, 33, 12],
                 [27, 6, 33, 12], [5, 6, 33, 12] ],
                [[27, 28, 11, 34], [5, 28, 11, 34], [27, 6, 11, 34],
                 [5, 6, 11, 34], [27, 28, 11, 12], [5, 28, 11, 12],
                 [27, 6, 11, 12], [5, 6, 11, 12] ],
                [[25, 26, 31, 32], [25, 6, 31, 32], [25, 26, 31, 12],
                 [25, 6, 31, 12], [15, 16, 21, 22], [15, 16, 21, 12],
                 [15, 16, 11, 22], [15, 16, 11, 12] ],
                [[29, 30, 35, 36], [29, 30, 11, 36], [5, 30, 35, 36],
                 [5, 30, 11, 36], [39, 40, 45, 46], [5, 40, 45, 46],
                 [39, 6, 45, 46], [5, 6, 45, 46] ],
                [[25, 30, 31, 36], [15, 16, 45, 46], [13, 14, 19, 20],
                 [13, 14, 19, 12], [17, 18, 23, 24], [17, 18, 11, 24],
                 [41, 42, 47, 48], [5, 42, 47, 48] ],
                [[37, 38, 43, 44], [37, 6, 43, 44], [13, 18, 19, 24],
                 [13, 14, 43, 44], [37, 42, 43, 48], [17, 18, 47, 48],
                 [13, 18, 43, 48], [1, 2, 7, 8] ]
                ]
    Layer1 = 0
    Layer2 = 1
    Layer3 = 2
    LayerE = 3
    LayerP = 4

    LayerTransparencyFactor = 0.5


    def __init__(self, parent, id= -1, size=wx.DefaultSize, map_id=0):
        '''
        
        @param parent: the parent window
        @param id: the window id
        @param size: the size of the window
        @param map_id: the id of the map to open
        '''
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
        # get plugin components
        self.RPG = KM.get_component("RPG", "RMXP").object
        self.Table = KM.get_component("Table", "RMXP").object
        self.Project = Kernel.Global.Project
        self.Cache = KM.get_component("WxCache", "RMXP").object
        #init data
        self.map_id = 0
        self.map = self.RPG.Map(20, 15)
        self.width = self.map.width
        self.height = self.map.height
        self.data = self.Table(self.width, self.height, 3)
        self.tileset_id = self.map.tileset_id
        self.events = {}
        self.zoom = 1.0
        self.active = 0
        self.old_active = 0
        self.mode = 0
        self.old_mode = 0
        self.tileset = self.Project.getTilesets()[self.tileset_id]
        self.autotile_names = []
        self.tileset_name = ""
        self.tileset_passages = self.Table()
        self.autotiles_b = []
        #layer buffers
        self.layer1 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layer1
        self.layer2 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layer2
        self.layer3 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layer3
        self.layer4 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layerEvents
        self.layer5 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layerBrush
        self.layer6 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layerMouse
        self.layerP = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height) #layerPreview
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.EmptyBitmap(sz.width, sz.height, 32)
        self.setup(map_id)
        #bind events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_MOTION, self.OnLeftButtonEvent)

    def OnLeftButtonEvent(self, event):
        if self.mode != self.LayerE:
            self.SetMouseXY(event)
        if event.LeftDown():
            self.SetFocus()
            self.SetMouseXY(event)
            self.CaptureMouse()
            self.drawing = True

        elif event.Dragging() and self.drawing:
            self.buildBrush()

        elif event.LeftUp():
            self.ReleaseMouse()
            if self.drawing:
                self.commitBrush()

        dc = wx.BufferedDC(None, self._buffer)
        gc = wx.GraphicsContext.Create(dc)
        self.DoDrawing(gc, self.init)

        # refresh it
        self.Refresh(eraseBackground=False)

    def buildBrush(self):
        pass

    def commitBrush(self):
        pass

    def setup(self, id):
        self.init = True
        self.map_id = id
        self.map = self.Project.getMap(self.map_id)
        self.width = self.map.width
        self.height = self.map.height
        self.data = self.Table(self.width, self.height, 3)
        self.tileset_id = self.map.tileset_id
        self.events = self.map.events
        self.mouse_x = self.old_mouse_x = self.mouse_y = self.old_mouse_y = 0
        self.last_mouse_x = self.last_mouse_y = 0
        self.zoom = 1.0
        self.old_zoom = 1
        self.active = 0
        self.old_active = 0
        self.mode = 0
        self.old_mode = 0
        self.tileset = self.Project.getTilesets()[self.tileset_id]
        self.autotile_names = []
        self.tileset_name = ""
        self.tileset_passages = self.Table()
        self.autotiles_b = [None] * 7
        self.layer1 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layer1
        self.layer2 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layer2
        self.layer3 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layer3
        self.layer4 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layerEvents
        self.layer5 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layerBrush
        self.layer6 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layerMouse
        self.layerP = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                         self.map.height) #layerPreview
        self._dimlayer = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
                                            self.map.height)
        self.InitBuffer()
        self.SetVirtualSize((((self.map.width) * 32) * self.zoom,
                             ((self.map.height) * 32) * self.zoom))
        self.SetScrollRate(1, 1)

    def SetMouseXY(self, event):
        x, y = self.ConvertEventCoords(event)
        x = x / int(32 * self.zoom)
        y = y / int(32 * self.zoom)
        self.mouse_x, self.mouse_y = x, y

    def ConvertEventCoords(self, event):
        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return newpos

    def needRedraw(self):
        # set flags
        flag = False
        layer1flag = False
        layer2flag = False
        layer3flag = False
        layerEflag = False
        previewflag = False
        mouseflag = False
        brushflag = False
        #test width and height
        if self.width != self.map.width:
            self.width = self.map.width
            flag = True
        if self.height != self.map.height:
            self.height = self.map.height
            flag = True
        #test tileset & autotiles
        if self.tileset_id != self.map.tileset_id:
            self.tileset_id = self.map.tileset_id
            flag = True
        if self.autotile_names != self.tileset.autotile_names:
            self.autotile_names = self.tileset.autotile_names[:]
            self.load_autotiles()
            flag = True
        if self.tileset_name != self.tileset.tileset_name:
            self.tileset_name = self.tileset.tileset_name
            flag = True
        #test data
        eq = self.data._data != self.map.data._data
        layerflags = eq.reshape(-1, 3).any(axis=0)
        layer1flag = layerflags[0]
        layer2flag = layerflags[1]
        layer3flag = layerflags[2]
        if layerflags.any():
            self.data._data[:] = self.map.data._data
        #test events
        if self.Project.Event_redraw_flags.has_key(self.map_id):
            if self.Project.Event_redraw_flags[self.map_id]:
                layerEflag = True
        #test active
        if self.old_active != self.active:
            self.old_active = self.active
            layerEflag = True
        # test mouse
        if (self.old_mouse_x != self.mouse_x) or (self.old_mouse_y != self.mouse_y):
            self.old_mouse_x = self.mouse_x
            self.old_mouse_y = self.mouse_y
            mouseflag = True
        #test brush 
        if False:
            brushflag = True

        return (flag, layer1flag, layer2flag, layer3flag, layerEflag, previewflag, mouseflag, brushflag)

    def InitBuffer(self):
        self._buffer = wx.EmptyBitmap(self.map.width * 32,
                                      self.map.height * 32, 32)
        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(wx.NullColor))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self.DoDrawing(gc, True)

    def OnPaint(self, event):
        #prepare dc and the draw to it
        dc = wx.BufferedPaintDC(self, self._buffer, wx.BUFFER_VIRTUAL_AREA)
        #gc = wx.GraphicsContext.Create(dc)
        #self.DoDrawing(gc, self.init)

    def DoDrawing(self, dc, init=False):
        flag, layer1flag, layer2flag, layer3flag, layerEflag, previewflag, mouseflag, brushflag = self.needRedraw()
        self.init = False
        if flag:
            self.draw_dimlayer()
        if flag or layer1flag:
            self.drawlayer1()
        if flag or layer2flag:
            self.drawlayer2()
        if flag or layer3flag:
            self.drawlayer3()
        if flag or layerEflag:
            self.draw_events()
        if flag or previewflag:
            self.draw_preview
        if flag or mouseflag:
            self.draw_mouse()
        if flag or brushflag:
            self.draw_brush
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 255), 1))
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 255)))
        #combine the layers onto the primary dc
        newWidth = self.layer1.GetWidth() * self.zoom
        newHeight = self.layer1.GetHeight() * self.zoom
        if self.mode == self.LayerP:
            if previewflag != True or init != True:
                return
            size = self.layerP.GetSize()
            dc.DrawRectangle(0, 0, size.width * self.zoom, size.height * self.zoom)
            imagelayerP = self.layerP.ConvertToImage()
            imagelayerP.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layerP = imagelayerP.ConvertToBitmap()
            dc.DrawBitmap(layerP, 0, 0, size.width * self.zoom, size.height)
        elif self.mode == self.Layer1:
            if (layer1flag != True and layer2flag != True and layer3flag !=
                True and layerEflag != True) and init != True and mouseflag != True:
                return
            dc.DrawRectangle(0, 0, self.layer1.GetWidth() * self.zoom, self.layer1.GetWidth() * self.zoom)
            #layer 1
            imagelayer1 = self.layer1.ConvertToImage()
            imagelayer1.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer1 = imagelayer1.ConvertToBitmap()
            dc.DrawBitmap(layer1, 0, 0, newWidth, newHeight)
            #brush layer
            imagelayer5 = self.layer5.ConvertToImage()
            imagelayer5.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer5 = imagelayer5.ConvertToBitmap()
            dc.DrawBitmap(layer5, 0, 0, newWidth, newHeight)
            #layer 2
            imagelayer2 = self.layer2.ConvertToImage()
            imagelayer2.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            imagelayer2.AdjustChannels(1.0, 1.0, 1.0, self.LayerTransparencyFactor)
            layer2 = imagelayer2.ConvertToBitmap()
            dc.DrawBitmap(layer2, 0, 0, newWidth, newHeight)
            #layer 3
            imagelayer3 = self.layer3.ConvertToImage()
            imagelayer3.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            imagelayer3.AdjustChannels(1.0, 1.0, 1.0, self.LayerTransparencyFactor)
            layer3 = imagelayer3.ConvertToBitmap()
            dc.DrawBitmap(layer3, 0, 0, newWidth, newHeight)
            #event layer
            imagelayerE = self.layer4.ConvertToImage()
            imagelayerE.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            imagelayerE.AdjustChannels(1.0, 1.0, 1.0, self.LayerTransparencyFactor)
            layerE = imagelayerE.ConvertToBitmap()
            dc.DrawBitmap(layerE, 0, 0, newWidth, newHeight)
            #mouse
            imagelayer6 = self.layer6.ConvertToImage()
            imagelayer6.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer6 = imagelayer6.ConvertToBitmap()
            dc.DrawBitmap(layer6, 0, 0, newWidth, newHeight)

        elif self.mode == self.Layer2:
            if (layer1flag != True and layer2flag != True and layer3flag !=
                True and layerEflag != True) and init != True and mouseflag != True:
                return
            dc.DrawRectangle(0, 0, self.layer1.GetWidth() * self.zoom, self.layer1.GetWidth() * self.zoom)
            #layer 1
            imagelayer1 = self.layer1.ConvertToImage()
            imagelayer1.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer1 = imagelayer1.ConvertToBitmap()
            dc.DrawBitmap(layer1, 0, 0, newWidth, newHeight)
            #dimlayers
            dc.DrawBitmap(self._dimlayer, 0, 0, newWidth, newHeight)
            #layer 2
            imagelayer2 = self.layer2.ConvertToImage()
            imagelayer2.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer2 = imagelayer2.ConvertToBitmap()
            dc.DrawBitmap(layer2, 0, 0, newWidth, newHeight)
            #brush layer
            imagelayer5 = self.layer5.ConvertToImage()
            imagelayer5.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer5 = imagelayer5.ConvertToBitmap()
            dc.DrawBitmap(layer5, 0, 0, newWidth, newHeight)
            #layer 3
            imagelayer3 = self.layer3.ConvertToImage()
            imagelayer3.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            imagelayer3.AdjustChannels(1.0, 1.0, 1.0, self.LayerTransparencyFactor)
            layer3 = imagelayer3.ConvertToBitmap()
            dc.DrawBitmap(layer3, 0, 0, newWidth, newHeight)
            #event layer
            imagelayerE = self.layer4.ConvertToImage()
            imagelayerE.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            imagelayerE.AdjustChannels(1.0, 1.0, 1.0, self.LayerTransparencyFactor)
            layerE = imagelayerE.ConvertToBitmap()
            dc.DrawBitmap(layerE, 0, 0, newWidth, newHeight)
            #mouse
            imagelayer6 = self.layer6.ConverToImage()
            imagelayer6.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer6 = imagelayer6.ConvertToBitmap()
            dc.DrawBitmap(layer6, 0, 0, newWidth, newHeight)
        elif self.mode == self.Layer3:
            if (layer1flag != True and layer2flag != True and layer3flag !=
                True and layerEflag != True) and init != True and mouseflag != True:
                return
            dc.DrawRectangle(0, 0, self.layer1.GetWidth() * self.zoom, self.layer1.GetWidth() * self.zoom)
            #layer 1
            imagelayer1 = self.layer1.ConvertToImage()
            imagelayer1.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer1 = imagelayer1.ConvertToBitmap()
            dc.DrawBitmap(layer1, 0, 0, newWidth, newHeight)
            #layer 2
            imagelayer2 = self.layer2.ConvertToImage()
            imagelayer2.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer2 = imagelayer2.ConvertToBitmap()
            dc.DrawBitmap(layer2, 0, 0, newWidth, newHeight)
            #dimlayers
            dc.DrawBitmap(self._dimlayer, 0, 0, newWidth, newHeight)
            #layer 3
            imagelayer3 = self.layer3.ConvertToImage()
            imagelayer3.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer3 = imagelayer3.ConvertToBitmap()
            dc.DrawBitmap(layer3, 0, 0, newWidth, newHeight)
            #brush layer
            imagelayer5 = self.layer5.ConvertToImage()
            imagelayer5.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer5 = imagelayer5.ConvertToBitmap()
            dc.DrawBitmap(layer5, 0, 0, newWidth, newHeight)
            #event layer
            imagelayerE = self.layer4.ConvertToImage()
            imagelayerE.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            imagelayerE.AdjustChannels(1.0, 1.0, 1.0, self.LayerTransparencyFactor)
            layerE = imagelayerE.ConvertToBitmap()
            dc.DrawBitmap(layerE, 0, 0, newWidth, newHeight)
            #mouse
            imagelayer6 = self.layer6.ConverToImage()
            imagelayer6.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer6 = imagelayer6.ConvertToBitmap()
            dc.DrawBitmap(layer6, 0, 0, newWidth, newHeight)
        elif self.mode == self.LayerE:
            if (layer1flag != True and layer2flag != True and layer3flag !=
                True and layerEflag != True) and init != True and mouseflag != True:
                return
            dc.DrawRectangle(0, 0, self.layer1.GetWidth() * self.zoom, self.layer1.GetWidth() * self.zoom)
            #layer 1
            imagelayer1 = self.layer1.ConvertToImage()
            imagelayer1.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer1 = imagelayer1.ConvertToBitmap()
            dc.DrawBitmap(layer1, 0, 0, newWidth, newHeight)
            #layer 2
            imagelayer2 = self.layer2.ConvertToImage()
            imagelayer2.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer2 = imagelayer2.ConvertToBitmap()
            dc.DrawBitmap(layer2, 0, 0, newWidth, newHeight)
            #layer 3
            imagelayer3 = self.layer3.ConvertToImage()
            imagelayer3.Rescale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH)
            layer3 = imagelayer3.ConvertToBitmap()
            dc.DrawBitmap(layer3, 0, 0, newWidth, newHeight)
            #event layer
            dc.DrawBitmap(self.layer4, 0, 0, self.layer4.GetWidth(), self.layer4.GetHeight())
            path = dc.CreatePath()
            path.AddRectangle(0, 0, 31, 31)
            dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, 80), 1))
            dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 255)))
            for x in xrange(0, self.map.width - 1):
                # Passes Through Z Coordinates
                for y in xrange(0, self.map.height - 1):
                    dc.PushState()             # save current translation/scale/other state 
                    dc.Scale(self.zoom, self.zoom)
                    dc.Translate(x * 32 * self.zoom, y * 32 * self.zoom)
                    dc.StrokePath(path)
                    dc.PopState()              # restore saved state

    def load_autotiles(self):
        for i in xrange(7):
            autotile_name = self.autotile_names[i]
            self.autotiles_b[i] = self.Cache.Autotile(autotile_name, self.Project.Location)
            if not self.autotiles_b[i]:
                self.autotiles_b[i] = self.Cache.Autotile(autotile_name, self.Project.RTP_Location)
            if not self.autotiles_b[i]:
                self.autotiles_b[i] = wx.EmptyBitmapRGBA(32 * 3, 32 * 4)

    def draw_brush(self):
        if (self.layer5.GetWidth() != self.map.width * 32) or (self.layer5.GetHeight() != self.map.width * 32):
            self.layer5 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)

    def draw_dimlayer(self):
        if (self._dimlayer.GetWidth() != self.map.width * 32) or (self._dimlayer.GetHeight() != self.map.width * 32):
            self._dimlayer = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self._dimlayer)
        dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0, 80)))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)

    def draw_mouse(self):
        if (self.layer6.GetWidth() != self.map.width * 32) or (self.layer6.GetHeight() != self.map.width * 32):
            self.layer6 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self.layer6)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, 0), wx.TRANSPARENT))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        path = gc.CreatePath()
        path.AddRectangle(0, 0, 31, 31)
        path.AddRectangle(3, 3, 25, 25)
        gc.SetPen(wx.Pen("black", 1))
        gc.SetBrush(wx.Brush("white"))
        gc.PushState()             # save current translation/scale/other state 
        gc.Translate(self.mouse_x * 32, self.mouse_y * 32)
        gc.DrawPath(path)
        gc.PopState()              # restore saved state
        dc.SelectObject(wx.NullBitmap)

    def draw_preview(self):
        if (self.layerP.GetWidth() != self.map.width * 32) or (self.layerP.GetHeight() != self.map.width * 32):
            self.layerP = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        if self.mode == self.LayerP:
            dc = wx.MemoryDC()
            dc.SelectObject(self.layerP)
            dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, 0), wx.TRANSPARENT))
            dc.Clear()
            tileset = self.Cache.Tileset(self.tileset_name, self.Project.Location)
            if not tileset:
                tileset = self.Cache.Tileset(self.tileset_name, self.Project.RTP_Location)
            if not tileset:
                tileset = wx.EmptyBitmapRGBA(32 * 6, 32)
            for p in xrange(0, 5):
                # Passes Through Layers
                for z in xrange(0, 2):
                    # Passes Through X Coordinates
                    for x in xrange(0, self.map.width - 1):
                        # Passes Through Z Coordinates
                        for y in xrange(0, self.map.height - 1):
                            # Collects Tile ID
                            id = self.data[x, y, z]
                            # if not 0 tile
                            if id != 0:
                                # If Priority Matches
                                if p == self.tileset.Priorities[id]:
                                    # Cap Priority to Layer 3
                                    if p > 2:
                                        p = 2
                                    # Draw Tile
                                    if id < 384:
                                        if self.autotiles[id / 48 - 1].GetWidth() / 96 > 1:
                                            autotile = self.autotiles_b[id / 48 - 1]
                                            tile_id = id % 48
                                            bitmap = wx.EmptyBitmapRGBA(32, 32)
                                            # Collects Auto-Tile Tile Layout
                                            tiles = self.Autotiles[tile_id / 8][tile_id % 8]
                                            dc_at = wx.MemoryDC()
                                            dc_at.SelectObject(bitmap)
                                            for i in xrange(4):
                                                tile_position = tiles[i] - 1
                                                src_rect = wx.Rect(tile_position % 6 * 16, tile_position / 6 * 16, 16, 16)
                                                sub_at_bitmap = autotile.GetSubBitmap(src_rect)
                                                dc_at.DrawBitmap(sub_at_bitmap, i % 2 * 16, i / 2 * 16, True)
                                            dc_at.SelectObject(wx.NullBitmap)
                                            t_x = x * 32
                                            t_y = y * 32
                                            dc.DrawBitmap(bitmap, t_x, t_y, True)
                                    else:
                                        rect = wx.Rect((id - 384) % 8 * 32, (id - 384) / 8 * 32, 32, 32)
                                        sub_bitmap = tileset.GetSubBitmap(rect)
                                        dc.DrawBitmap(sub_bitmap, x * 32, y * 32, True)
            dc.SelectObject(wx.NullBitmap)

    def draw_events(self):
        if (self.layer4.GetWidth() != self.map.width * 32) or (self.layer4.GetHeight() != self.map.width * 32):
            self.layer4 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self.layer4)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, 0), wx.TRANSPARENT))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        path = gc.CreatePath()
        gc.SetPen(wx.Pen("white", 1))
        gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255, 80)))
        path.AddRectangle(4, 4, 23, 23)
        for key in self.events.iterkeys():
            event = self.events[key]
            eventGraphic = self.events[key].pages[0].graphic
            if eventGraphic.tile_id >= 384:
                temp_bitmap = self.Cache.Tile(self.tileset_name, eventGraphic.tile_id,
                                              eventGraphic.character_hue, self.Project.Location)
                if not temp_bitmap:
                    temp_bitmap = self.Cache.Tile(self.tileset_name, eventGraphic.tile_id,
                                                  eventGraphic.character_hue, self.Project.RTP_Location)
                if not temp_bitmap:
                    temp_bitmap = wx.EmptyBitmapRGBA(32, 32)
                rect = wx.Rect(5, 5, 22, 22)
                bitmap = temp_bitmap.GetSubBitmap(rect)
            else:
                temp_bitmap = self.Cache.Character(eventGraphic.character_name,
                                                   eventGraphic.character_hue, self.Project.Location)
                if not temp_bitmap:
                    temp_bitmap = self.Cache.Character(eventGraphic.character_name, eventGraphic.character_hue,
                                                       self.Project.RTP_Location)
                if not temp_bitmap:
                    temp_bitmap = wx.EmptyBitmapRGBA(32 * 4, 32 * 4)
                cw = temp_bitmap.GetWidth() / 4
                ch = temp_bitmap.GetHeight() / 4
                sx = eventGraphic.pattern * cw
                sy = (eventGraphic.direction - 2) / 2 * ch
                rect = wx.Rect(sx + 5, sy + 5, 22, 22)
                bitmap = temp_bitmap.GetSubBitmap(rect)
            bitmapSize = bitmap.GetSize()
            gc.PushState()             # save current translation/scale/other state 
            gc.Translate(event.x * 32, event.y * 32)
            gc.DrawPath(path)
            gc.PopState()              # restore saved state
            gc.DrawBitmap(bitmap, event.x * 32 + 5, event.y * 32 + 5, bitmapSize.width, bitmapSize.height)
        dc.SelectObject(wx.NullBitmap)

    def drawlayer1(self):
        if (self.layer1.GetWidth() != self.map.width * 32) or (self.layer1.GetHeight() != self.map.width * 32):
            self.layer1 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self.layer1)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, 0), wx.TRANSPARENT))
        dc.Clear()
        dc = wx.GCDC(dc)
        emptybitmap = False
        tileset = self.Cache.Tileset(self.tileset_name, self.Project.Location)
        if not tileset:
            tileset = self.Cache.Tileset(self.tileset_name, self.Project.RTP_Location)
        if not tileset:
            tileset = wx.EmptyBitmapRGBA(32 * 8, 32)
            emptybitmap = True
        for x in xrange(self.map.width):
            for y in xrange(self.map.height):
                id = int(self.data[x, y, 0])
                if id != 0:
                    if id < 384:
                        if self.autotiles_b[id / 48 - 1].GetWidth() / 96 >= 1:
                            autotile = self.autotiles_b[id / 48 - 1]
                            tile_id = id % 48
                            # Collects Auto-Tile Tile Layout
                            tiles = self.Autotiles[tile_id / 8][tile_id % 8]
                            t_x = x * 32
                            t_y = y * 32
                            for i in xrange(4):
                                tile_position = tiles[i] - 1
                                src_rect = wx.Rect(tile_position % 6 * 16, tile_position / 6 * 16, 16, 16)
                                sub_at_bitmap = autotile.GetSubBitmap(src_rect)
                                dc.DrawBitmap(sub_at_bitmap, t_x + (i % 2 * 16),
                                              t_y + (i / 2 * 16), True)
                    else:
                        rect = wx.Rect((id - 384) % 8 * 32, (id - 384) / 8 * 32, 32, 32)
                        if emptybitmap and tileset.GetHeight() < (rect.GetY() + 32):
                            tileset = wx.EmptyBitmap(32 * 8, rect.GetY() + 32)
                        sub_bitmap = tileset.GetSubBitmap(rect)
                        dc.DrawBitmap(sub_bitmap, x * 32, y * 32, True)

    def drawlayer2(self):
        if (self.layer2.GetWidth() != self.map.width * 32) or (self.layer2.GetHeight() != self.map.width * 32):
            self.layer2 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self.layer2)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, 0), wx.TRANSPARENT))
        dc.Clear()
        dc = wx.GCDC(dc)
        emptybitmap = False
        tileset = self.Cache.Tileset(self.tileset_name, self.Project.Location)
        if not tileset:
            tileset = self.Cache.Tileset(self.tileset_name, self.Project.RTP_Location)
        if not tileset:
            tileset = wx.EmptyBitmapRGBA(32 * 8, 32)
            emptybitmap = True
        for x in xrange(self.map.width):
            for y in xrange(self.map.height):
                id = int(self.data[x, y, 1])
                if id != 0:
                    if id < 384:
                        if self.autotiles_b[id / 48 - 1].GetWidth() / 96 >= 1:
                            autotile = self.autotiles_b[id / 48 - 1]
                            tile_id = id % 48
                            # Collects Auto-Tile Tile Layout
                            tiles = self.Autotiles[tile_id / 8][tile_id % 8]
                            t_x = x * 32
                            t_y = y * 32
                            for i in xrange(4):
                                tile_position = tiles[i] - 1
                                src_rect = wx.Rect(tile_position % 6 * 16, tile_position / 6 * 16, 16, 16)
                                sub_at_bitmap = autotile.GetSubBitmap(src_rect)
                                dc.DrawBitmap(sub_at_bitmap, t_x + (i % 2 * 16),
                                              t_y + (i / 2 * 16), True)
                    else:
                        rect = wx.Rect((id - 384) % 8 * 32, (id - 384) / 8 * 32, 32, 32)
                        if emptybitmap and tileset.GetHeight() < (rect.GetY() + 32):
                            tileset = wx.EmptyBitmap(32 * 8, rect.GetY() + 32)
                        sub_bitmap = tileset.GetSubBitmap(rect)
                        dc.DrawBitmap(sub_bitmap, x * 32, y * 32, True)

    def drawlayer3(self):
        if (self.layer3.GetWidth() != self.map.width * 32) or (self.layer3.GetHeight() != self.map.width * 32):
            self.layer3 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 * self.map.height)
        dc = wx.MemoryDC()
        dc.SelectObject(self.layer3)
        dc.SetBackground(wx.Brush(wx.Colour(255, 255, 255, 0), wx.TRANSPARENT))
        dc.Clear()
        dc = wx.GCDC(dc)
        emptybitmap = False
        tileset = self.Cache.Tileset(self.tileset_name, self.Project.Location)
        if not tileset:
            tileset = self.Cache.Tileset(self.tileset_name, self.Project.RTP_Location)
        if not tileset:
            tileset = wx.EmptyBitmapRGBA(32 * 8, 32)
            emptybitmap = True
        for x in xrange(self.map.width):
            for y in xrange(self.map.height):
                id = int(self.data[x, y, 2])
                if id != 0:
                    if id < 384:
                        if self.autotiles_b[id / 48 - 1].GetWidth() / 96 >= 1:
                            autotile = self.autotiles_b[id / 48 - 1]
                            tile_id = id % 48
                            # Collects Auto-Tile Tile Layout
                            tiles = self.Autotiles[tile_id / 8][tile_id % 8]
                            t_x = x * 32
                            t_y = y * 32
                            for i in xrange(4):
                                tile_position = tiles[i] - 1
                                src_rect = wx.Rect(tile_position % 6 * 16, tile_position / 6 * 16, 16, 16)
                                sub_at_bitmap = autotile.GetSubBitmap(src_rect)
                                dc.DrawBitmap(sub_at_bitmap, t_x + (i % 2 * 16),
                                              t_y + (i / 2 * 16), True)
                    else:
                        rect = wx.Rect((id - 384) % 8 * 32, (id - 384) / 8 * 32, 32, 32)
                        if emptybitmap and tileset.GetHeight() < (rect.GetY() + 32):
                            tileset = wx.EmptyBitmap(32 * 8, rect.GetY() + 32)
                        sub_bitmap = tileset.GetSubBitmap(rect)
                        dc.DrawBitmap(sub_bitmap, x * 32, y * 32, True)


# broken pygame version
#===============================================================================
# class PyGameRMXPMapWindow(wx.ScrolledWindow):
# 
#    Autotiles = [
#                [[27, 28, 33, 34], [5, 28, 33, 34], [27, 6, 33, 34],
#                 [5, 6, 33, 34], [27, 28, 33, 12], [5, 28, 33, 12],
#                 [27, 6, 33, 12], [5, 6, 33, 12] ],
#                [[27, 28, 11, 34], [5, 28, 11, 34], [27, 6, 11, 34],
#                 [5, 6, 11, 34], [27, 28, 11, 12], [5, 28, 11, 12],
#                 [27, 6, 11, 12], [5, 6, 11, 12] ],
#                [[25, 26, 31, 32], [25, 6, 31, 32], [25, 26, 31, 12],
#                 [25, 6, 31, 12], [15, 16, 21, 22], [15, 16, 21, 12],
#                 [15, 16, 11, 22], [15, 16, 11, 12] ],
#                [[29, 30, 35, 36], [29, 30, 11, 36], [5, 30, 35, 36],
#                 [5, 30, 11, 36], [39, 40, 45, 46], [5, 40, 45, 46],
#                 [39, 6, 45, 46], [5, 6, 45, 46] ],
#                [[25, 30, 31, 36], [15, 16, 45, 46], [13, 14, 19, 20],
#                 [13, 14, 19, 12], [17, 18, 23, 24], [17, 18, 11, 24],
#                 [41, 42, 47, 48], [5, 42, 47, 48] ],
#                [[37, 38, 43, 44], [37, 6, 43, 44], [13, 18, 19, 24],
#                 [13, 14, 43, 44], [37, 42, 43, 48], [17, 18, 47, 48],
#                 [13, 18, 43, 48], [1, 2, 7, 8] ]
#                ]
#    Layer1 = 0 #layer1
#    Layer2 = 1 #layer2
#    Layer3 = 2 #layer3
#    LayerE = 3 #layerEvents
#    LayerB = 4 #layerBrush
#    LayerP = 5 #layerPreview
# 
#    LayerTransparency = 80
# 
#    def __init__(self, parent, id= -1, size=wx.DefaultSize, map_id=0):
#        '''
#        
#        @param parent: the parent window
#        @param id: the window id
#        @param size: the size of the window
#        @param map_id: the id of the map to open
#        '''
# 
#        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
#        # get plugin components
#        self.RPG = KM.get_component("RPG", "RMXP").object
#        self.Table = KM.get_component("Table", "RMXP").object
#        self.Project = Kernel.Global.Project
#        self.Cache = KM.get_component("PyGameCache", "RMXP").object
#        self.adjust_alpha = KM.get_component("AdjustAlphaOperator", "RMXP").object
# 
#        #init data
#        self.map_id = 0
#        self.map = self.RPG.Map(20, 15)
#        self.width = self.map.width
#        self.height = self.map.height
#        self.data = self.Table(self.width, self.height, 3)
#        self.tileset_id = self.map.tileset_id
#        self.events = {}
#        self.zoom = 1
#        self.dim_layers = True
#        self.dim_event_layer = True
#        self.active = 0
#        self.old_active = 0
#        self.mode = 0
#        self.old_mode = 0
#        self.tileset = self.Project.getTilesets()[self.tileset_id]
#        self.autotile_names = []
#        self.tileset_name = ""
#        self.tileset_passages = self.Table()
#        self.autotiles_b = []
# 
#        #setup the map
#        self.setup(map_id)
# 
#        #layer buffers
#        self.init_layer_buffers()
#        self.init_outline_buffers()
# 
#        #bind events
#        self.Bind(wx.EVT_PAINT, self.OnPaint)
#        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
#        self.Bind(wx.EVT_LEFT_UP, self.OnLeftButtonEvent)
#        self.Bind(wx.EVT_MOTION, self.OnLeftButtonEvent)
# 
# 
#        #draw timer
#        self.timer = wx.Timer(self)
#        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
# 
#        self.fps = 10.0
#        self.timespacing = 1000.0 / self.fps
#        self.timer.Start(self.timespacing, False)
# 
#    def init_layer_buffers(self):
#        self.layers = []
#        for i in xrange(6): #@UnusedVariable
#            self.layers.append(pygame.Surface((32 * self.map.width,
#                                               32 * self.map.height),
#                                               pygame.SRCALPHA, 32).convert_alpha())
# 
#    def init_outline_buffers(self):
#        #mouse
#        self.mousesurf = pygame.Surface((32, 32), pygame.SRCALPHA, 32).convert_alpha()
#        self.mousesurf.fill((0, 0, 0, 255))
#        pygame.draw.rect(self.mousesurf, (255, 255, 255, 255), (1, 1, 30, 30))
#        pygame.draw.rect(self.mousesurf, (0, 0, 0, 255), (3, 3, 26, 26))
#        pygame.draw.rect(self.mousesurf, (0, 0, 0, 0), (4, 4, 24, 24))
#        #event
#        self.eventsurf = pygame.Surface((32, 32), pygame.SRCALPHA, 32).convert_alpha()
#        self.eventsurf.fill((0, 0, 0, 0))
#        pygame.draw.rect(self.eventsurf, (255, 255, 255, 255), (4, 4, 24, 24))
#        pygame.draw.rect(self.eventsurf, (255, 255, 255, 80), (5, 5, 22, 22))
# 
#    def Update(self, event):
#        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
#        self.Redraw()
#        dc = wx.ClientDC(self)
#        self.PyGameToClient(dc, self.DoDrawing())
# 
#    def OnLeftButtonEvent(self, event):
#        self.SetMouseXY(event)
#        if event.LeftDown():
#            self.SetFocus()
#            self.CaptureMouse()
#            self.drawing = True
# 
#        elif event.Dragging() and self.drawing:
#            self.buildBrush()
# 
#        elif event.LeftUp():
#            self.ReleaseMouse()
#            if self.drawing:
#                self.commitBrush()
# 
#        self.DoDrawing()
# 
#    def buildBrush(self):
#        pass
# 
#    def commitBrush(self):
#        pass
# 
#    def setup(self, id):
#        '''
#        sets up the window to draw a map
#        
#        @param id: the id of the map to set up
#        '''
#        self.init = True
#        self.map_id = id
#        self.map = self.Project.getMap(self.map_id)
#        self.width = self.map.width
#        self.height = self.map.height
#        self.data = self.Table(self.width, self.height, 3)
#        self.tileset_id = self.map.tileset_id
#        self.events = self.map.events
#        self.mouse_x = self.old_mouse_x = self.mouse_y = self.old_mouse_y = 0
#        self.last_mouse_x = self.last_mouse_y = 0
#        self.dim_layers = True
#        self.dim_event_layer = True
#        self.zoom = 1
#        self.old_zoom = 1
#        self.active = 0
#        self.old_active = 0
#        self.mode = 0
#        self.old_mode = 0
#        self.tileset = self.Project.getTilesets()[self.tileset_id]
#        self.autotile_names = []
#        self.tileset_name = ""
#        self.tileset_passages = self.Table()
#        self.autotiles_b = [None] * 7
#        self.layer1 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layer1
#        self.layer2 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layer2
#        self.layer3 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layer3
#        self.layer4 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layerEvents
#        self.layer5 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layerBrush
#        self.layer6 = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layerMouse
#        self.layerP = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                         self.map.height) #layerPreview
#        self._dimlayer = wx.EmptyBitmapRGBA(32 * self.map.width, 32 *
#                                            self.map.height)
# 
#        self.SetVirtualSize(((self.map.width) * 32,
#                             (self.map.height) * 32))
#        self.SetScrollRate(20, 20)
# 
#    def SetMouseXY(self, event):
#        '''
#        set the x,y of the mouse on the map
#        
#        @param event: the wx.Event that came form the mouse
#        '''
#        x, y = self.ConvertEventCoords(event)
#        x = x / int(32 * self.zoom)
#        y = y / int(32 * self.zoom)
#        self.mouse_x, self.mouse_y = x, y
# 
#    def ConvertEventCoords(self, event):
#        '''
#        convert the cooridnats to use the proper orign of the scrolled window
#        
#        @param event: the mouse event
#        '''
#        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
#        return newpos
# 
#    def needRedraw(self):
#        '''
#        test data and return a tuple of flags that indicate things that need 
#        to be redrawn
#        
#        the list is in the order
#        flag, layer1flag, layer2flag, layer3flag, layerEflag, previewflag, mouseflag, brushflag
#        the first flag indicats that everything needs to be redrawn
#        '''
#        # set flags
#        flag = False
#        layer1flag = False
#        layer2flag = False
#        layer3flag = False
#        layerEflag = False
#        previewflag = False
#        mouseflag = False
#        brushflag = False
# 
#        #test width and height
#        if self.width != self.map.width:
#            self.width = self.map.width
#            flag = True
#        if self.height != self.map.height:
#            self.height = self.map.height
#            flag = True
# 
#        #test tileset & autotiles
#        if self.tileset_id != self.map.tileset_id:
#            self.tileset_id = self.map.tileset_id
#            flag = True
#        if self.autotile_names != self.tileset.autotile_names:
#            self.autotile_names = self.tileset.autotile_names[:]
#            flag = True
#        if self.tileset_name != self.tileset.tileset_name:
#            self.tileset_name = self.tileset.tileset_name
#            flag = True
# 
#        #test data
#        eq = self.data._data != self.map.data._data
#        layerflags = eq.reshape(-1, 3).any(axis=0)
#        layer1flag = layerflags[0]
#        layer2flag = layerflags[1]
#        layer3flag = layerflags[2]
#        if layerflags.any():
#            self.data._data[:] = self.map.data._data
# 
#        #test events
#        if self.Project.Event_redraw_flags.has_key(self.map_id):
#            if self.Project.Event_redraw_flags[self.map_id]:
#                layerEflag = True
# 
#        #test active
#        if self.old_active != self.active:
#            self.old_active = self.active
#            layerEflag = True
# 
#        # test mouse
#        if (self.old_mouse_x != self.mouse_x) or (self.old_mouse_y != self.mouse_y):
#            self.old_mouse_x = self.mouse_x
#            self.old_mouse_y = self.mouse_y
#            mouseflag = True
# 
#        #test brush 
#        if False:
#            brushflag = True
# 
#        return (flag, layer1flag, layer2flag, layer3flag, layerEflag, previewflag, mouseflag, brushflag)
# 
#    def OnPaint(self, event):
#        #prepare dc and the draw to it
#        dc = wx.PaintDC(self)
#        self.PyGameToClient(dc, self.DoDrawing())
# 
#    def PyGameToClient(self, dc, surface):
#        #format = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
# #        surface.convert_alpha()
# #        bmp = wx.BitmapFromBufferRGBA(surface.get_width(),
# #                                      surface.get_height(),
# #                                      surface.get_buffer())
#        surface.convert()
#        s = pygame.image.tostring(surface, 'RGB')  # Convert the surface to an RGB string
#        img = wx.ImageFromData(surface.get_width(), surface.get_height(), s)  # Load this string into a wx image
#        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
#        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
#        del dc
# 
#    def DoDrawing(self):
#        #combine the layers onto a surface to be sent to the window
#        unitx , unity = self.GetScrollPixelsPerUnit()
#        viewx, viewy = self.GetViewStart()
#        scrollx, scrolly = viewx * unitx, viewy * unity
#        width, height = self.GetClientSizeTuple()
#        surface = pygame.Surface((int(width / self.zoom),
#                                  int(height / self.zoom)),
#                                  pygame.SRCALPHA, 32)
#        #preview mode
#        if self.mode == self.LayerP:
#            self.draw_preview_mode(surface, (scrollx, scrolly), (width,
#                                                                 height))
#        elif self.mode == self.Layer1:
#            self.draw_layer1_mode(surface, (scrollx, scrolly), (width,
#                                                                height))
#        elif self.mode == self.Layer2:
#            self.draw_layer2_mode(surface, (scrollx, scrolly), (width,
#                                                                height))
#        elif self.mode == self.Layer3:
#            self.draw_layer3_mode(surface, (scrollx, scrolly), (width,
#                                                                height))
# 
#        elif self.mode == self.LayerE:
#            self.draw_events_mode(surface, (scrollx, scrolly), (width,
#                                                                height))
#        return surface
# 
#    def draw_preview_mode(self, surface, xy, wh):
#        x, y = xy
#        width, height = wh
#        rect = (x, y, int(width / self.zoom), int(height / self.zoom))
#        surface.blit(self.layers[self.LayerP], (0, 0), rect)
#        if self.zoom != 1.0:
#            surface = pygame.transform.scale(surface, (width, height))
# 
#    def draw_layer1_mode(self, surface, xy, wh):
#        x, y = xy
#        width, height = wh
#        partwidth, partheight = int(width / self.zoom), int(height / self.zoom)
#        rect = (int(x * self.zoom), int(y * self.zoom), partwidth, partheight)
#        #layer 1
#        surface.blit(self.layers[self.Layer1], (0, 0), rect)
#        #brush layer
#        surface.blit(self.layers[self.LayerB], (0, 0), rect)
#        #layer 2
#        if self.dim_layers:
#            blitsurface = pygame.Surface((partwidth, partheight),
#                                         pygame.SRCALPHA, 32)
#            blitsurface.blit(self.layers[self.Layer2], (0, 0), rect)
#            self.adjust_alpha(blitsurface, self.LayerTransparency)
#        else:
#            blitsurface = self.layers[self.Layer2].subsurface(rect)
#        surface.blit(blitsurface, (0, 0))
#        #layer 3
#        if self.dim_layers:
#            blitsurface = pygame.Surface((partwidth, partheight),
#                                         pygame.SRCALPHA, 32)
#            blitsurface.blit(self.layers[self.Layer3], (0, 0), rect)
#            self.adjust_alpha(blitsurface, self.LayerTransparency)
#        else:
#            blitsurface = self.layers[self.Layer3].subsurface(rect)
#        surface.blit(blitsurface, (0, 0))
#        #event layer
#        if self.dim_event_layer:
#            blitsurface = pygame.Surface((partwidth, partheight),
#                                         pygame.SRCALPHA, 32)
#            blitsurface.blit(self.layers[self.LayerE], (0, 0), rect)
#            self.adjust_alpha(blitsurface, self.LayerTransparency)
#        else:
#            blitsurface = self.layers[self.LayerE].subsurface(rect)
#        surface.blit(blitsurface, (0, 0))
#        #mouse
#        mousex = (self.mouse_x * 32)
#        mousey = (self.mouse_y * 32)
#        if (mousex > rect[0] and mousey > rect[1] and mousex < rect[2] and
#            mousey < rect[3]):
#            surface.blit(self.mousesurf, (mousex - x, mousey - y))
#        #scale the surface to the right zoom value
#        if self.zoom != 1.0:
#            surface = pygame.transform.scale(surface, (width, height))
# 
#    def draw_layer2_mode(self, surface, xy, wh):
#        x, y = xy
#        width, height = wh
#        partwidth, partheight = int(width / self.zoom), int(height / self.zoom)
#        rect = (int(x * self.zoom), int(y * self.zoom), partwidth, partheight)
#        #layer 1
#        surface.blit(self.layers[self.Layer1], (0, 0), rect)
#        #dimlayers
#        if self.dim_layers:
#            dim = pygame.Surface((partwidth, partheight),
#                                 pygame.SRCALPHA, 32)
#            dim.fill((0, 0, 0, 80))
#            surface.blit(dim, (0, 0))
#        #layer 2
#        surface.blit(self.layers[self.Layer2], (0, 0), rect)
#        #brush layer
#        surface.blit(self.layers[self.LayerB], (0, 0), rect)
#        #layer 3
#        if self.dim_layers:
#            blitsurface = pygame.Surface((partwidth, partheight),
#                                         pygame.SRCALPHA, 32)
#            blitsurface.blit(self.layers[self.Layer3], (0, 0), rect)
#            self.adjust_alpha(blitsurface, self.LayerTransparency)
#        else:
#            blitsurface = self.layers[self.Layer3].subsurface(rect)
#        surface.blit(blitsurface, (0, 0))
#        #event layer
#        if self.dim_event_layer:
#            blitsurface = pygame.Surface((partwidth, partheight),
#                                         pygame.SRCALPHA, 32)
#            blitsurface.blit(self.layers[self.LayerE], (0, 0), rect)
#            self.adjust_alpha(blitsurface, self.LayerTransparency)
#        else:
#            blitsurface = self.layers[self.LayerE].subsurface(rect)
#        surface.blit(blitsurface, (0, 0))
#        #mouse
#        mousex = (self.mouse_x * 32)
#        mousey = (self.mouse_y * 32)
#        if (mousex > rect[0] and mousey > rect[1] and mousex < rect[2] and
#            mousey < rect[3]):
#            surface.blit(self.mousesurf, (mousex - x, mousey - y))
#        #scale the surface to the right zoom value
#        if self.zoom != 1.0:
#            surface = pygame.transform.scale(surface, (width, height))
# 
#    def draw_layer3_mode(self, surface, xy, wh):
#        x, y = xy
#        width, height = wh
#        partwidth, partheight = int(width / self.zoom), int(height / self.zoom)
#        rect = (int(x * self.zoom), int(y * self.zoom), partwidth, partheight)
#        #layer 1
#        surface.blit(self.layers[self.Layer1], (0, 0), rect)
#        #layer 2
#        surface.blit(self.layers[self.Layer2], (0, 0), rect)
#        #dimlayers
#        if self.dim_layers:
#            dim = pygame.Surface((partwidth, partheight), pygame.SRCALPHA, 32)
#            dim.fill((0, 0, 0, 80))
#            surface.blit(dim, (0, 0))
#        #layer 3
#        surface.blit(self.layers[self.Layer3], (0, 0), rect)
#        #brush layer
#        surface.blit(self.layers[self.LayerB], (0, 0), rect)
#        #event layer
#        if self.dim_event_layer:
#            blitsurface = pygame.Surface((partwidth, partheight),
#                                         pygame.SRCALPHA, 32)
#            blitsurface.blit(self.layers[self.LayerE], (0, 0), rect)
#            self.adjust_alpha(blitsurface, self.LayerTransparency)
#        else:
#            blitsurface = self.layers[self.LayerE].subsurface(rect)
#        surface.blit(blitsurface, (0, 0))
#        #mouse
#        mousex = (self.mouse_x * 32)
#        mousey = (self.mouse_y * 32)
#        if (mousex > rect[0] and mousey > rect[1] and mousex < rect[2] and
#            mousey < rect[3]):
#            surface.blit(self.mousesurf, (mousex - x, mousey - y))
#        #scale the surface to the right zoom value
#        if self.zoom != 1.0:
#            surface = pygame.transform.scale(surface, (width, height))
# 
#    def draw_events_mode(self, surface, xy, wh):
#        x, y = xy
#        width, height = wh
#        partwidth, partheight = int(width / self.zoom), int(height / self.zoom)
#        rect = (int(x * self.zoom), int(y * self.zoom), partwidth, partheight)
#        #layer 1
#        surface.blit(self.layers[self.Layer1], (0, 0), rect)
#        #layer 2
#        surface.blit(self.layers[self.Layer2], (0, 0), rect)
#        #layer 3
#        surface.blit(self.layers[self.Layer3], (0, 0), rect)
#        #event layer
#        surface.blit(self.layers[self.LayerE], (0, 0), rect)
#        #tile outlines
#        self.draw_tile_outlines(surface, x % 32, y % 32)
#        #mouse
#        mousex = (self.mouse_x * 32)
#        mousey = (self.mouse_y * 32)
#        if (mousex > rect[0] and mousey > rect[1] and mousex < rect[2] and
#            mousey < rect[3]):
#            surface.blit(self.mousesurf, (mousex - x, mousey - y))
#        #scale the surface to the right zoom value
#        if self.zoom != 1.0:
#            surface = pygame.transform.scale(surface, (width, height))
# 
#    def Redraw(self):
#        flag, layer1flag, layer2flag, layer3flag, layerEflag, previewflag, mouseflag, brushflag = self.needRedraw()
#        self.init = False
#        if flag:
#            self.init_layer_buffers()
#        if flag or layer1flag:
#            self.drawlayer(self.Layer1)
#        if flag or layer2flag:
#            self.drawlayer(self.Layer2)
#        if flag or layer3flag:
#            self.drawlayer(self.Layer3)
#        if flag or layerEflag:
#            self.draw_events()
#        if flag or previewflag:
#            self.draw_preview
#        if flag or brushflag:
#            self.draw_brush
# 
#    def draw_brush(self):
#        pass
# 
#    def draw_tile(self, surface, x, y, id):
#        #get the tile bitmap
#        #autotile
#        if id < 384:
#            #get the filename
#            autotile = self.autotile_names[int(id) / 48 - 1]
#            #get the right pattern
#            pattern = id % 48
#            #collect the tile form the cache checking the local project folder
#            #and the system RTP folder
#            bitmap = self.Cache.AutotilePattern(autotile, pattern,
#                                                self.Project.Location)
#            if not bitmap:
#                bitmap = self.Cache.AutotilePattern(autotile, pattern, self.Project.RTP_Location)
#            if not bitmap:
#                flag = True
#                bitmap = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
#        #normal tile
#        else:
#            #get the tile bitmap
#            bitmap = self.Cache.Tile(self.tileset_name, id, 0, self.Project.Location)
#            if not bitmap:
#                bitmap = self.Cache.Tile(self.tileset_name, id, 0, self.Project.RTP_Location)
#            if not bitmap:
#                bitmap = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
#        #draw the tile to the surface
#        surface.blit(bitmap, (x * 32, y * 32))
# 
#    def draw_preview(self):
#        if self.mode == self.LayerP:
#            surface = self.layers[self.LayerP]
#            surface.fill((0, 0, 0, 0))
#            for p in xrange(0, 5):
#                # Passes Through Layers
#                for z in xrange(0, 2):
#                    # Passes Through X Coordinates
#                    for x in xrange(0, self.map.width - 1):
#                        # Passes Through Y Coordinates
#                        for y in xrange(0, self.map.height - 1):
#                            # Collects Tile ID
#                            id = self.data[x, y, z]
#                            # if not 0 tile
#                            if id != 0:
#                                # If Priority Matches
#                                if p == self.tileset.Priorities[id]:
#                                    self.draw_tile(surface, x, y, id)
# 
#    def draw_events(self):
#        surface = self.layers[self.LayerE]
#        surface.fill((0, 0, 0, 0))
#        #for each event
#        for key in self.events.iterkeys():
#            #get the event graphic
#            event = self.events[key]
#            eventGraphic = self.events[key].pages[0].graphic
#            #if the graphic is a tile
#            if eventGraphic.tile_id >= 384:
#                bitmap = self.Cache.Tile(self.tileset_name,
#                                         eventGraphic.tile_id,
#                                         eventGraphic.character_hue,
#                                         self.Project.Location)
#                if not bitmap:
#                    bitmap = self.Cache.Tile(self.tileset_name,
#                                             eventGraphic.tile_id,
#                                             eventGraphic.character_hue,
#                                             self.Project.RTP_Location)
#                if not bitmap:
#                    bitmap = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
#                rect = (5, 5, 22, 22)
#            #other wise the graphic is a sprite
#            else:
#                bitmap = self.Cache.Character(eventGraphic.character_name,
#                                              eventGraphic.character_hue,
#                                              self.Project.Location)
#                if not bitmap:
#                    bitmap = self.Cache.Character(eventGraphic.character_name,
#                                                  eventGraphic.character_hue,
#                                                  self.Project.RTP_Location)
#                if not bitmap:
#                    bitmap = pygame.Surface((32 * 4, 32 * 4),
#                                            pygame.SRCALPHA, 32)
#                cw = bitmap.get_width() / 4
#                ch = bitmap.get_height() / 4
#                sx = eventGraphic.pattern * cw
#                sy = (eventGraphic.direction - 2) / 2 * ch
#                rect = (sx + 5, sy + 5, 22, 22)
#            #draw the background
#            surface.blit(self.eventsurf, (event.x * 32, event.y * 32))
#            #draw a portion of the event graphic
#            surface.blit(bitmap, (event.x * 32 + 5, event.y * 32 + 5), rect)
# 
#    def draw_tile_outlines(self, surface, offx, offy):
#        width = int(surface.get_width())
#        height = int(surface.get_height())
#        linesh = width / 32
#        linesv = height / 32
#        for line in xrange(linesh):
#            x = line + offx
#            pygame.draw.line(surface, (0, 0, 0, 80), (x, 0), (x, height), 2)
#        for line in xrange(linesv):
#            y = line + offy
#            pygame.draw.line(surface, (0, 0, 0, 80), (0, y), (width, y), 2)
# 
#    def drawlayer(self, layer):
#        surface = self.layers[layer]
#        surface.fill((0, 0, 0, 0))
#        #loop through the x values of the tiles
#        for x in xrange(self.map.width):
#            #loop though the y values of the tiles
#            for y in xrange(self.map.height):
#                #get the tile id
#                id = self.data[x, y, layer]
#                #draw the tile
#                self.draw_tile(surface, x, y, id)
# 
#    def Kill(self, event):
#        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
#        # call the Redraw() method
#        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
#        # This may or may not be necessary now that Pygame is just drawing to surfaces
#        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
#        self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)
#        self.Destroy()
#===============================================================================

class WxRMXPMapPanel(wx.Panel):
    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent)

        #set up Sizer
        box = wx.BoxSizer(wx.VERTICAL)

        #set up notebook
        self.notebook = aui.AuiNotebook(self, -1, wx.Point(0, 0),
                                        wx.Size(430, 200), agwStyle=style)

        #add ctrls to sizer
        box.Add(self.notebook, 1, wx.ALL | wx.EXPAND)
        #set sizer
        self.SetSizerAndFit(box)

    def add_page(self, map_id, name):
            editor = WxRMXPMapWindow(self, map_id=map_id)
            self.notebook.AddPage(editor, name)

#broken pygame version
#===============================================================================
# class PyGameRMXPMapPanel(wx.Panel):
#    def __init__(self, parent, style):
#        wx.Panel.__init__(self, parent)
# 
#        #set up containers
#        self.editors = []
# 
#        #set up Sizer
#        box = wx.BoxSizer(wx.VERTICAL)
# 
#        #set up notebook
#        self.notebook = aui.AuiNotebook(self, -1, wx.Point(0, 0),
#                                        wx.Size(430, 200), agwStyle=style)
# 
#        #add ctrls to sizer
#        box.Add(self.notebook, 1, wx.ALL | wx.EXPAND)
#        #set sizer
#        self.SetSizerAndFit(box)
# 
#        #bind events
#        self.Bind(wx.EVT_CLOSE, self.Kill)
# 
#    def add_page(self, map_id, name):
#            editor = PyGameRMXPMapWindow(self, map_id=map_id)
#            self.editors.append(editor)
#            self.notebook.AddPage(editor, name)
# 
#    def Kill(self, event):
#        for editor in self.editors:
#            editor.Kill(event)
#        self.editors = []
#        self.Destroy()
#===============================================================================

