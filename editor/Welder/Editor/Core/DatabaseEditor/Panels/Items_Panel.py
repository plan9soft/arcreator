import wx

import Kernel

from PyitectConsumes import DatabaseManager as DM
from PyitectConsumes import RGSS1_RPG as RPG

from PyitectConsumes import ChooseGraphic_Dialog

from PyitectConsumes import PanelBase, Items_Panel_Template
# --------------------------------------------------------------------------------------
# Items_Panel
# --------------------------------------------------------------------------------------


class Items_Panel(Items_Panel_Template, PanelBase):

    _arc_panel_info_string = "Name Caption Center CloseB CaptionV DestroyOC Floatable Float IconARCM MaximizeB MinimizeM MinimizeB Movable NotebookD Resizable Snappable"
    _arc_panel_info_data = {"Name": "Items Panel", "Caption": "Items Panel", "CaptionV": True,  "MinimizeM": ["POS_SMART", "CAPT_SMART", ],
                            "MinimizeB": True, "CloseB": True, 'IconARCM': 'itemsicon'}

    def __init__(self, parent, item_index=0):
        """Basic constructor for the Items panel"""
        Items_Panel_Template.__init__(self, parent)
        global Config
        global DataItems, DataStates, DataElements, DataCommonEvents, DataAnimations
        
        try:
            proj = Kernel.GlobalObjects['PROJECT']
            DataItems = proj.getData('Items')
            DataStates = proj.getData('States')
            DataElements = proj.getData('System').elements
            DataAnimations = proj.getData('Animations')
            DataCommonEvents = proj.getData('CommonEvents')
        except NameError:
            Kernel.Log(
                'Database opened before Project has been initialized', '[Database:ITEMS]', True)
            self.Destroy()
        font = wx.Font(
            8, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font.SetFaceName(Kernel.Config.getUnified()['Misc']['NoteFont'])
        self.textCtrlNotes.SetFont(font)
        DM.DrawButtonIcon(self.bitmapButtonAudioTest, 'play_button', True)
        self.comboBoxMenuSE.SetCursor(wx.STANDARD_CURSOR)
        self.SelectedItem = DataItems[DM.FixedIndex(item_index)]
        self.refreshAll()
        self.listBoxItems.SetSelection(item_index)
        DM.DrawHeaderBitmap(self.bitmapItems, 'Items')

        # Bind the panel tot he Panel Manager
        self.bindPanelManager()

    def setRange(self):
        pass

    def refreshItems(self):
        """Refreshes the values in the item wxListBox control"""
        digits = len(Kernel.Config.getUnified()['GameObjects']['Items'])
        DM.FillControl(self.listBoxItems, DataItems, digits, [])

    def refreshElements(self):
        """Clears and refreshes the list of elements in the checklist"""
        start = DM.FixedIndex(0)
        DM.FillWithoutNumber(self.checkListElements, [], DataElements[start:])

    def refreshStates(self):
        """Clears and refreshes the list of states in the checklist"""
        self.checkListStates.DeleteAllItems()
        names = [DataStates[i].name for i in range(
            DM.FixedIndex(0), len(DataStates))]
        self.checkListStates.AppendItems(names)

    def refreshParameters(self):
        """Refreshes the defined parameters"""
        self.comboBoxParameter.Clear()
        params = ['(None)', 'MaxHP', 'MaxSP']
        if DM.ARC_FORMAT:
            params.extend(list(Kernel.Config.getUnified()['GameSetup']['Parameters']))
        else:
            params.extend(['STR', 'DEX', 'AGI', 'INT'])
        self.comboBoxParameter.AppendItems(params)

    def refreshAnimations(self):
        """Refreshes the choices in the user and target animation controls"""
        digits = len(Kernel.Config.getUnified()['GameObjects']['Animations'])
        DM.FillControl(
            self.comboBoxTargetAnimation, DataAnimations, digits, ['(None)'])
        DM.FillControl(
            self.comboBoxUserAnimation, DataAnimations, digits, ['(None)'])

    def refreshCommonEvents(self):
        """Refreshes the common events in the combo box"""
        digits = len(Kernel.Config.getUnified()['GameObjects']['CommonEvents'])
        DM.FillControl(
            self.comboBoxCommonEvent, DataCommonEvents, digits, ['(None)'])

    def refreshValues(self):
        """Refreshes all the values on the panel to reflect the selected item"""
        item = self.SelectedItem
        self.textCtrlName.ChangeValue(item.name)
        self.textCtrlDescription.ChangeValue(item.description)
        self.labelIconName.SetLabel(item.icon_name)
        DM.DrawButtonIcon(self.bitmapButtonIcon, item.icon_name, False)
        self.comboBoxScope.SetSelection(item.scope)
        self.comboBoxOccasion.SetSelection(item.occasion)
        self.comboBoxUserAnimation.SetSelection(item.animation1_id)
        self.comboBoxTargetAnimation.SetSelection(item.animation2_id)
        self.comboBoxMenuSE.SetValue(item.menu_se.name)
        self.comboBoxCommonEvent.SetSelection(item.common_event_id)
        self.spinCtrlPrice.SetValue(item.price)
        if item.consumable:
            index = 0
        else:
            index = 1
        self.comboBoxConsumable.SetSelection(index)
        self.comboBoxParameter.SetSelection(item.parameter_type)
        self.spinCtrlParameterInc.SetValue(item.parameter_points)
        self.spinCtrlRecrHPRate.SetValue(item.recover_hp_rate)
        self.spinCtrlRecrHP.SetValue(item.recover_hp)
        self.spinCtrlRecrSPRate.SetValue(item.recover_sp_rate)
        self.spinCtrlRecrSP.SetValue(item.recover_sp)
        self.spinCtrlHitRate.SetValue(item.hit)
        self.spinCtrlPDEF.SetValue(item.pdef_f)
        self.spinCtrlMDEF.SetValue(item.mdef_f)
        self.spinCtrlVariance.SetValue(item.variance)
        if DM.ARC_FORMAT:
            addstates = self.SelectedSkill.plus_state_set
            minusstates = self.SelectedSkill.minus_state_set
            indices = item.element_set
        else:
            addstates = [id - 1 for id in item.plus_state_set]
            minusstates = [id - 1 for id in item.minus_state_set]
            indices = [i - 1 for i in item.element_set]
        self.checkListElements.SetChecked(indices)
        for i in range(self.checkListStates.GetItemCount()):
            if i in addstates:
                self.checkListStates.SetItemImage(i, 1)
            elif i in minusstates:
                self.checkListStates.SetItemImage(i, 2)
            else:
                self.checkListStates.SetItemImage(i, 0)

        if not hasattr(item, 'note'):
            setattr(item, 'note', '')
        self.textCtrlNotes.ChangeValue(item.note)

    def refreshAll(self):
        """Refreshes all the controls on the panel"""
        self.refreshItems()
        self.refreshElements()
        self.refreshStates()
        self.refreshParameters()
        self.refreshAnimations()
        self.refreshCommonEvents()
        self.refreshValues()

    def listBoxItems_SelectionChanged(self, event):
        """Changes the selected item"""
        index = DM.FixedIndex(event.GetInt())
        if DataItems[index] == None:
            DataItems[index] = RPG.Item()
        self.SelectedItem = DataItems[index]
        self.refreshValues()

    def buttonMaximum_Clicked(self, event):
        """Starts the Change Maximum dialog"""
        max = int(Kernel.Config.getUnified()['GameObjects']['Items'])
        DM.ChangeDataCapacity(self, self.listBoxItems, DataItems, max)

    def textCtrlName_TextChanged(self, event):
        """updates the selected items's name"""
        DM.updateObjectName(self.SelectedItem, event.GetString(),
                            self.listBoxItems, len(Kernel.Config.getUnified()['GameObjects']['Items']))

    def bitmapButtonIcon_Clicked(self, event):
        """Opens dialog to select an icon for the selected skill"""
        filename = DM.ChooseGraphic(self, 'Icons', self.SelectedItem.icon_name)
        if filename:
            self.SelectedItem.icon_name = filename
        self.refreshValues()

    def bitmapButtonAudioTest_Clicked(self, event):
        """Plays the sound effect as a quick test without opening the dialog"""
        DM.QuickPlay(self.SelectedItem.menu_se, 'SE')

    def textCtrlDescription_TextChange(self, event):
        """updates the selected item's description"""
        self.SelectedItem.description = event.GetString()

    def comboBoxScope_SelectionChanged(self, event):
        """updates the selected item's scope"""
        self.SelectedItem.scope = event.GetInt()

    def comboBoxUserAnimation_SelectionChanged(self, event):
        """updates the selected item's user animation"""
        self.SelectedItem.animation1_id = DM.FixedIndex(event.GetInt())

    def comboBoxMenuSE_Clicked(self, event):
        """Opens the dialog for selecting the audio file to use"""
        audio = DM.ChooseAudio(self, self.SelectedItem.menu_se, 'SE')
        if audio is not None:
            self.comboBoxMenuSE.SetValue(DM.GetAudioLabel(audio))

    def comboBoxOccasion_SelectionChanged(self, event):
        """updates the selected item's occasion"""
        self.SelectedItem.occasion = event.GetInt()

    def comboBoxTargetAnimation_SelectionChanged(self, event):
        """updates the selected item's target animation"""
        self.SelectedItem.animation2_id = DM.FixedIndex(event.GetInt())

    def comboBoxCommonEvent_SelectionChanged(self, event):
        """updates the selected item's common event"""
        self.SelectedItem.common_event_id = event.GetInt()

    def spinCtrlPrice_ValueChanged(self, event):
        """updates the selected item's price"""
        self.SelectedItem.price = event.GetInt()

    def spinCtrlRecrHPPercent_ValueChanged(self, event):
        """updates the selected item's recovery HP percent"""
        self.SelectedItem.recover_hp_rate = event.GetInt()

    def spinCtrlHitRate_ValueChanged(self, event):
        """updates the selected item's hit rate"""
        self.SelectedItem.hit = event.GetInt()

    def comboBoxConsumable_SelectionChanged(self, event):
        """updates the selected item's consumable flag"""
        self.SelectedItem.consumable = (event.GetInt() == 0)

    def spinCtrlRecrHP_ValueChanged(self, event):
        """updates the selected item's recovery HP"""
        self.SelectedItem.recover_hp = event.GetInt()

    def spinCtrlPDEF_ValueChanged(self, event):
        """updates the selected item's PDEF"""
        self.SelectedItem.pdef_f = event.GetInt()

    def comboBoxParameter_SelectionChanged(self, event):
        """updates the selected item's parameter type"""
        self.SelectedItem.parameter_type = event.GetInt()

    def spinCtrlRecrSPPercent_ValueChanged(self, event):
        """updates the selected item's recover SP percent"""
        self.SelectedItem.recover_sp_rate = event.GetInt()

    def spinCtrlMDEF_ValueChanged(self, event):
        """updates the selected item's MDEF"""
        self.SelectedItem.mdef_f = event.GetInt()

    def spinCtrlParameterInc_ValueChanged(self, event):
        """updates the selected item's parameter points"""
        self.SelectedItem.parameter_points = event.GetInt()

    def spinCtrlRecrSP_ValueChanged(self, event):
        """updates the selected item's recovery SP"""
        self.SelectedItem.recover_sp = event.GetInt()

    def spinCtrlVariance_ValueChanged(self, event):
        """updates the selected item's variance"""
        self.SelectedItem.variance = event.GetInt()

    def textCtrlNotes_TextChanged(self, event):
        """Sets the note for the selected skill"""
        self.SelectedItem.note = event.GetString()

    def checkListElements_Clicked(self, event):
        """updates the guard elements for the selected item"""
        self.checkListElements.ChangeState(event, 1)
        if DM.ARC_FORMAT:
            # TODO: Implement
            pass
        else:
            ids = [DM.FixedIndex(id)
                   for id in self.checkListElements.GetChecked()]
            self.SelectedItem.element_set = ids

    def checkListStates_LeftClicked(self, event):
        """updates the plus/minus state set for the selected item"""
        data = self.checkListStates.ChangeState(event, 1)
        DM.ChangeSkillStates(self.SelectedItem, data[0], data[1])

    def checkListStates_RigthClicked(self, event):
        """updates the plus/minus state set for the selected item"""
        data = self.checkListStates.ChangeState(event, -1)
        DM.ChangeSkillStates(self.SelectedItem, data[0], data[1])
