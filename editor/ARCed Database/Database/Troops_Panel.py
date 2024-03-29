import wx
import Database.ARCed_Templates as Templates
from Database.Dialogs import ChangeMaximum_Dialog, ChooseGraphic_Dialog, BattleTest_Dialog, EventCondition_Dialog
import EventCommands1_Panel
import EventCommands2_Panel
import EventCommands3_Panel
import Database.Manager as DM
#--------------------------------------------------------------------------------------
# Troops_Panel
#--------------------------------------------------------------------------------------

# Implementing Troops_Panel
class Troops_Panel( Templates.Troops_Panel ):
	def __init__( self, parent ):
		Templates.Troops_Panel.__init__( self, parent )


		DM.DrawHeaderBitmap(self.bitmapTroops, 'Troops')

	# Handlers for Troops_Panel events.
	def listBoxTroops_SelectionChanged( self, event ):
		# TODO: Implement listBoxTroops_SelectionChanged
		pass

	def buttonMaximum_Clicked( self, event ):
		# TODO: Implement buttonMaximum_Clicked
		pass

	def textCtrlName_ValueChanged( self, event ):
		# TODO: Implement textCtrlName_ValueChanged
		pass

	def buttonAutoname_Clicked( self, event ):
		# TODO: Implement buttonAutoname_Clicked
		pass

	def buttonBattleback_Click( self, event ):
		# TODO: Implement buttonBattleback_Click
		pass

	def buttonBattleTest_Click( self, event ):
		# TODO: Implement buttonBattleTest_Click
		pass

	def buttonAddEnemy_Click( self, event ):
		# TODO: Implement buttonAddEnemy_Click
		pass

	def buttonRemoveEnemy_Click( self, event ):
		# TODO: Implement buttonRemoveEnemy_Click
		pass

	def buttonClearTroop_Click( self, event ):
		# TODO: Implement buttonClearTroop_Click
		pass

	def buttonAlignTroop_Click( self, event ):
		# TODO: Implement buttonAlignTroop_Click
		pass

	def listBoxEnemies_SelectionChanged( self, event ):
		# TODO: Implement listBoxEnemies_SelectionChanged
		pass

	def buttonNewEventPage_Click( self, event ):
		# TODO: Implement buttonNewEventPage_Click
		pass

	def buttonCopyEventPage_Click( self, event ):
		# TODO: Implement buttonCopyEventPage_Click
		pass

	def buttonPasteEventPage_Click( self, event ):
		# TODO: Implement buttonPasteEventPage_Click
		pass

	def buttonDeleteEventPage_Click( self, event ):
		# TODO: Implement buttonDeleteEventPage_Click
		pass

	def buttonClearEventPage_Click( self, event ):
		# TODO: Implement buttonClearEventPage_Click
		pass

	def comboBoxCondition_Clicked( self, event ):
		# TODO: Implement comboBoxCondition_Clicked
		pass

	def comboBoxSpan_ValueChanged( self, event ):
		# TODO: Implement comboBoxSpan_ValueChanged
		pass

	def listBoxEvents_DoubleClick( self, event ):
		# TODO: Implement listBoxEvents_DoubleClick
		pass


