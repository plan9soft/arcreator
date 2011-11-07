"""Subclass of Weapons_Panel, which is generated by wxFormBuilder."""

import wx
import ARCed_Templates
import ARCedChangeMaximum_Dialog
import ARCedChooseGraphic_Dialog
from DatabaseUtil import DatabaseUtil as util

# Implementing Weapons_Panel
class ARCedWeapons_Panel( ARCed_Templates.Weapons_Panel ):
	def __init__( self, parent ):
		ARCed_Templates.Weapons_Panel.__init__( self, parent )


		util.DrawHeaderBitmap(self.bitmapWeapons, 'Weapons')

	# Handlers for Weapons_Panel events.
	def listBoxWeapons_SelectionChanged( self, event ):
		# TODO: Implement listBoxWeapons_SelectionChanged
		pass

	def buttonMaximum_Clicked( self, event ):
		# TODO: Implement buttonMaximum_Clicked
		pass

	def textCtrlName_TextChanged( self, event ):
		# TODO: Implement textCtrlName_TextChanged
		pass

	def comboBoxIcon_Clicked( self, event ):
		# TODO: Implement comboBoxIcon_Clicked
		pass

	def textCtrlDescription_TextChange( self, event ):
		# TODO: Implement textCtrlDescription_TextChange
		pass

	def comboBoxUserAnimation_SelectionChanged( self, event ):
		# TODO: Implement comboBoxUserAnimation_SelectionChanged
		pass

	def comboBoxOccasion_SelectionChanged( self, event ):
		# TODO: Implement comboBoxOccasion_SelectionChanged
		pass

	def spinCtrlPrice_ValueChanged( self, event ):
		# TODO: Implement spinCtrlPrice_ValueChanged
		pass

	def spinCtrlStrPlus_ValueChanged( self, event ):
		# TODO: Implement spinCtrlStrPlus_ValueChanged
		pass

	def spinCtrlAtk_ValueChanged( self, event ):
		# TODO: Implement spinCtrlAtk_ValueChanged
		pass

	def spinCtrlDexPlus_ValueChanged( self, event ):
		# TODO: Implement spinCtrlDexPlus_ValueChanged
		pass

	def spinCtrlPdef_ValueChanged( self, event ):
		# TODO: Implement spinCtrlPdef_ValueChanged
		pass

	def spinCtrlAgiPlus_ValueChanged( self, event ):
		# TODO: Implement spinCtrlAgiPlus_ValueChanged
		pass

	def spinCtrlMdef_ValueChanged( self, event ):
		# TODO: Implement spinCtrlMdef_ValueChanged
		pass

	def spinCtrlIntPlus_ValueChanged( self, event ):
		# TODO: Implement spinCtrlIntPlus_ValueChanged
		pass

	def checkListElements_CheckChanged( self, event ):
		# TODO: Implement checkListElements_CheckChanged
		pass

	def checkListStates_CheckChanged( self, event ):
		# TODO: Implement checkListStates_CheckChanged
		pass

	def textCtrlNotes_TextChanged( self, event ):
		# TODO: Implement textCtrlNotes_TextChanged
		pass


