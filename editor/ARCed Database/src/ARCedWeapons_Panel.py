import wx
import ARCed_Templates
from Core.RMXP import RGSS1_RPG as RPG
from DatabaseManager import DatabaseManager as DM
import Kernel

class ARCedWeapons_Panel( ARCed_Templates.Weapons_Panel ):
	def __init__( self, parent, weapon_index=0 ):
		"""Basic constructor for the Weapons panel"""
		ARCed_Templates.Weapons_Panel.__init__( self, parent )
		global Config, DataWeapons, DataStates, DataAnimations, DataElements
		Config = Kernel.GlobalObjects.get_value('ARCed_config')
		try:
			proj = Kernel.GlobalObjects.get_value('PROJECT')
			DataWeapons = proj.getData('Weapons')
			DataAnimations = proj.getData('Animations')
			DataStates = proj.getData('States')
			DataElements = proj.getData('System').elements
		except NameError:
			Kernel.Log('Database opened before Project has been initialized', '[Database:WEAPONS]', True)
			self.Destroy()
		self.listCtrlStates.AssignImageList(DM.GetAddSubImageList(), wx.IMAGE_LIST_SMALL)
		font = wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		font.SetFaceName(Config.get('Misc', 'NoteFont')) 
		self.textCtrlNotes.SetFont(font)
		self.ParameterControls = [self.spinCtrlPrice, self.spinCtrlAtk,
			self.spinCtrlPdef, self.spinCtrlMdef]
		self.ParameterControls.extend(DM.AddParameterSpinCtrls(self.panelParameters, 
			self.spinCtrlParameter_ValueChanged, '+:', 4))
		self.SelectedWeapon = DataWeapons[DM.FixedIndex(weapon_index)]
		self.refreshAll()
		self.listBoxWeapons.SetSelection(weapon_index)
		DM.DrawHeaderBitmap(self.bitmapWeapons, 'Weapons')

	def refreshAll( self ):
		"""Refreshes all the controls on the panel"""
		self.refreshWeaponList()
		self.refreshElements()
		self.refreshStates()
		self.refreshAnimations()
		self.refreshValues()

	def refreshWeaponList( self ):
		"""Refreshes the list of weapons"""
		digits = len(Config.get('GameObjects', 'Weapons'))
		DM.FillControl(self.listBoxWeapons, DataWeapons, digits, [])

	def refreshElements( self ):
		"""Refreshes the list of elements in the wxCheckListBox"""
		self.checkListElements.Clear()
		self.checkListElements.AppendItems(DataElements[DM.FixedIndex(0):])

	def refreshStates( self ):
		"""Clears and refreshes the list of states in the checklist"""
		self.listCtrlStates.DeleteAllItems()
		start = DM.FixedIndex(0)
		names = [DataStates[i].name for i in xrange(start, len(DataStates))]
		self.listCtrlStates.InsertColumn(0, '')
		for i in xrange(len(names)):
			self.listCtrlStates.InsertStringItem(i, names[i], 0)

	def refreshAnimations( self ):
		"""Refreshes the choices in the user and target animation controls"""
		digits = len(Config.get('GameObjects', 'Animations'))
		DM.FillControl(self.comboBoxUserAnimation, DataAnimations, digits, ['(None)'])
		DM.FillControl(self.comboBoxTargetAnimation, DataAnimations, digits, ['(None)'])

	def refreshValues( self ):
		weapon = self.SelectedWeapon
		self.textCtrlName.ChangeValue(weapon.name)
		self.labelIconName.SetLabel(weapon.icon_name)
		DM.DrawButtonIcon(self.bitmapButtonIcon, weapon.icon_name, False)
		self.textCtrlDescription.ChangeValue(weapon.description)
		self.comboBoxUserAnimation.SetSelection(weapon.animation1_id)
		self.comboBoxTargetAnimation.SetSelection(weapon.animation2_id)
		self.spinCtrlPrice.SetValue(weapon.price)
		self.spinCtrlAtk.SetValue(weapon.atk)
		self.spinCtrlPdef.SetValue (weapon.pdef)
		self.spinCtrlMdef.SetValue(weapon.mdef)
		if DM.ARC_FORMAT:
			# TODO: Implement
			addstates = skill.plus_state_set
			minusstates = skill.minus_state_set
			checked = weapon.element_set
		else:
			checked = [i - 1 for i in weapon.element_set]
			addstates = [id - 1 for id in weapon.plus_state_set]
			minusstates = [id - 1 for id in weapon.minus_state_set]
			self.ParameterControls[0].SetValue(weapon.price)
			self.ParameterControls[1].SetValue(weapon.atk)
			self.ParameterControls[2].SetValue(weapon.pdef)
			self.ParameterControls[3].SetValue(weapon.mdef)
			self.ParameterControls[4].SetValue(weapon.str_plus)
			self.ParameterControls[5].SetValue(weapon.dex_plus)
			self.ParameterControls[6].SetValue(weapon.agi_plus)
			self.ParameterControls[7].SetValue(weapon.int_plus)
		self.checkListElements.SetChecked(checked)
		for i in xrange(self.listCtrlStates.GetItemCount()):
			if i in addstates:
				self.listCtrlStates.SetItemImage(i, 1)
			elif i in minusstates:
				self.listCtrlStates.SetItemImage(i, 2)
			else:
				self.listCtrlStates.SetItemImage(i, 0)
		if not hasattr(weapon, 'note'):
			setattr(weapon, 'note', '')
		self.textCtrlNotes.ChangeValue(weapon.note)

	def spinCtrlParameter_ValueChanged( self, event ):
		index = self.ParameterControls.index(event.GetEventObject())
		if DM.ARC_FORMAT:
			# TODO: Implement
			pass
		else:
			value = event.GetInt()
			if index == 0: self.SelectedWeapon.price = value
			elif index == 1: self.SelectedWeapon.atk = value
			elif index == 2: self.SelectedWeapon.pdef = value
			elif index == 3: self.SelectedWeapon.mdef = value
			elif index == 4: self.SelectedWeapon.str_plus = value
			elif index == 5: self.SelectedWeapon.dex_plus = value
			elif index == 6: self.SelectedWeapon.agi_plus = value
			elif index == 7: self.SelectedWeapon.int_plus = value

	def listBoxWeapons_SelectionChanged( self, event ):
		"""Changes the selected weapon and update the values on the panel"""
		index = DM.FixedIndex(event.GetSelection())
		if DataWeapons[index] == None:
			DataWeapons[index] = RPG.Weapon()
		self.SelectedWeapon = DataWeapons[index]
		self.refreshValues()
	
	def buttonMaximum_Clicked( self, event ):
		"""Starts the Change Maximum dialog"""
		max = Config.getint('GameObjects', 'Weapons')
		DM.ChangeDataCapacity(self, self.listBoxWeapons, DataWeapons, max)
	
	def textCtrlName_TextChanged( self, event ):
		"""Updates the selected weapon's name"""
		DM.UpdateObjectName(self.SelectedWeapon, event.GetString(),
			self.listBoxWeapons, len(Config.get('GameObjects', 'Weapons')))
	
	def bitmapButtonIcon_Clicked( self, event ):
		"""Opens dialog to select an icon for the selected skill"""
		DM.ChooseGraphic('Graphics/Icon/', self.SelectedWeapon.icon_name, 0, False)
	
	def textCtrlDescription_TextChange( self, event ):
		"""Set the selected weapon's description"""
		self.SelectedWeapon.description = event.GetString()
	
	def comboBoxUserAnimation_SelectionChanged( self, event ):
		"""Set the selected weapon's user animation"""
		self.SelectedWeapon.animation1_id = event.GetInt()
	
	def comboBoxTargetAnimation_SelectionChanged( self, event ):
		"""Set the selected weapon's target animation"""
		self.SelectedWeapon.animation2_id = event.GetInt()
	
	def checkListElements_CheckChanged( self, event ):
		"""Sets the IDs that are in the selected weapon's element set"""
		ids = [DM.FixedIndex(id) for id in self.checkListElements.GetChecked()]
		self.SelectedWeapon.element_set = ids

	def listCtrlStates_LeftClicked( self, event ):
		"""Cycles the State change up one"""
		DM.ChangeSkillStates(self.listCtrlStates, self.SelectedWeapon, event, 1)

	def listCtrlStates_RightClicked( self, event ):
		"""Cycles the State change down one"""
		DM.ChangeSkillStates(self.listCtrlStates, self.SelectedWeapon, event, -1)
	
	def textCtrlNotes_TextChanged( self, event ):
		"""Set the selected weapon's magical defense"""
		self.SelectedWeapon.note = event.GetString()
	
	