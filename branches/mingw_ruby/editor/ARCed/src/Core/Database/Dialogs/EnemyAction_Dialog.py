"""Subclass of EnemyAction_Dialog, which is generated by wxFormBuilder."""

import wx
from Core.Database import ARCed_Templates as Templates

# Implementing EnemyAction_Dialog
class EnemyAction_Dialog( Templates.EnemyAction_Dialog ):
	def __init__( self, parent ):
		Templates.EnemyAction_Dialog.__init__( self, parent )
	
	# Handlers for EnemyAction_Dialog events.
	def checkBoxTurn_CheckChanged( self, event ):
		# TODO: Implement checkBoxTurn_CheckChanged
		pass
	
	def checkBoxHP_CheckChanged( self, event ):
		# TODO: Implement checkBoxHP_CheckChanged
		pass
	
	def checkBoxLevel_CheckChanged( self, event ):
		# TODO: Implement checkBoxLevel_CheckChanged
		pass
	
	def checkBoxSwitch_CheckChanged( self, event ):
		# TODO: Implement checkBoxSwitch_CheckChanged
		pass
	
	def radioBtnBasic_CheckChanged( self, event ):
		# TODO: Implement radioBtnBasic_CheckChanged
		pass
	
	def radioBtnSkill_CheckChanged( self, event ):
		# TODO: Implement radioBtnSkill_CheckChanged
		pass
	
	def sliderRating_ValueChanged( self, event ):
		# TODO: Implement sliderRating_ValueChanged
		pass
	
	def spinCtrlRating_ValueChanged( self, event ):
		# TODO: Implement spinCtrlRating_ValueChanged
		pass
	
	def buttonOK_Clicked( self, event ):
		# TODO: Implement buttonOK_Clicked
		pass
	
	def buttonCancel_Clicked( self, event ):
		# TODO: Implement buttonCancel_Clicked
		pass
	
	