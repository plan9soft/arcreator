import os, sys
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

import wx
import ARCed_Templates
import ARCedActorParameters_Dialog
import ARCedActors_Panel
import ARCedAnimationCellBatch_Dialog
import ARCedAnimationCellProperties_Dialog
import ARCedAnimationEntireSlide_Dialog
import ARCedAnimations_Panel
import ARCedAnimationTiming_Dialog
import ARCedAnimationTweening_Dialog
import ARCedArmors_Panel
import ARCedBattleAnimation_Dialog
import ARCedBattleProcessing_Dialog
import ARCedButonProcessing_Dialog
import ARCedCallCommonEvent_Dialog
import ARCedChangeAccess_Dialog
import ARCedChangeActorClass_Dialog
import ARCedChangeActorGraphic_Dialog
import ARCedChangeActorName_Dialog
import ARCedChangeBlending_Dialog
import ARCedChangeEquipment_Dialog
import ARCedChangeFogOpacity_Dialog
import ARCedChangeFrequency_Dialog
import ARCedChangeHP_Dialog
import ARCedChangelGold_Dialog
import ARCedChangelPartyEquipment_Dialog
import ARCedChangeMapSettings_Dialog
import ARCedChangeMaximum_Dialog
import ARCedChangeParameters_Dialog
import ARCedChangePartyMember_Dialog
import ARCedChangePictureColorTone_Dialog
import ARCedChangeSkills_Dialog
import ARCedChangeSpeed_Dialog
import ARCedChangeState_Dialog
import ARCedChangeStat_Dialog
import ARCedChangeTextOptions_Dialog
import ARCedChangeTone_Dialog
import ARCedChooseActor_Dialog
import ARCedChooseAudio_Dialog
import ARCedChooseFogGraphic_Dialog
import ARCedChooseGraphic_Dialog
import ARCedChooseSwitchVariable_Dialog
import ARCedChooseTreasure_Dialog
import ARCedClasses_Panel
import ARCedComment_Dialog
import ARCedCommonEvents_Panel
import ARCedConditionalBranch_Dialog
import ARCedControlSelfSwitches_Dialog
import ARCedControlSwitches_Dialog
import ARCedControlTimer_Dialog
import ARCedControlVariables_Dialog
import ARCedDatabaseMain_Panel
import ARCedDealDamage_Dialog
import ARCedEnemies_Panel
import ARCedEnemyAction_Dialog
import ARCedEnemyAppearance_Dialog
import ARCedEnemyTransform_Dialog
import ARCedErasePicture_Dialog
import ARCedEventCommands1_Panel
import ARCedEventCommands2_Panel
import ARCedEventCommands3_Panel
import ARCedEventCondition_Dialog
import ARCedEventEditor_Panel
import ARCedEventPage_Panel
import ARCedExpCurve_Dialog
import ARCedFadeOutAudio_Dialog
import ARCedForceAction_Dialog
import ARCedGenerateCurve_Dialog
import ARCedInputNumber_Dialog
import ARCedItems_Panel
import ARCedJump_Dialog
import ARCedLabel_Dialog
import ARCedMovePicture_Dialog
import ARCedMoveRoute_Dialog
import ARCedNameProcessing_Dialog
import ARCedRecoverAll_Dialog
import ARCedRotatePicture_Dialog
import ARCedScreenShake_Dialog
import ARCedScriptCall_Dialog
import ARCedScrollMap_Dialog
import ARCedSetEventLocation_Dialog
import ARCedShopGoods_Dialog
import ARCedShopProcessing_Dialog
import ARCedShowAnimation_Dialog
import ARCedShowChoices_Dialog
import ARCedShowPicture_Dialog
import ARCedShowText_Dialog
import ARCedSkills_Panel
import ARCedSkill_Dialog
import ARCedStates_Panel
import ARCedSystem_Panel
import ARCedTilesets_Panel
import ARCedTransferEventTilemap_Dialog
import ARCedTransferPlayerTilemap_Dialog
import ARCedTransferPlayer_Dialog
import ARCedTransparentFlag_Dialog
import ARCedTroops_Panel
import ARCedWait_Dialog
import ARCedWeapons_Panel
import ARCedWeatherEffects_Dialog

class ARCedTest(wx.App):

	def __init__(self, redirect=False, filename=None):
		wx.App.__init__(self, redirect, filename)
		self.frame = wx.Frame(None, wx.ID_ANY, title='ARCed Panel Test', size=(800, 600))
		nb = wx.Notebook(self.frame, wx.ID_ANY)
		tabs = ('Actors', 'Classes', 'Skills', 'Items', 'Weapons', 'Armors',
				'Enemies', 'Troops', 'States', 'Animations', 'Tilesets',
				'Common Events', 'System')
		pages = (ARCedActors_Panel.ARCedActors_Panel, ARCedClasses_Panel.ARCedClasses_Panel,
				 ARCedSkills_Panel.ARCedSkills_Panel, ARCedItems_Panel.ARCedItems_Panel,
				 ARCedWeapons_Panel.ARCedWeapons_Panel, ARCedArmors_Panel.ARCedArmors_Panel,
				 ARCedEnemies_Panel.ARCedEnemies_Panel, ARCedTroops_Panel.ARCedTroops_Panel,
				 ARCedStates_Panel.ARCedStates_Panel, ARCedAnimations_Panel.ARCedAnimations_Panel,
				 ARCedTilesets_Panel.ARCedTilesets_Panel, ARCedCommonEvents_Panel.ARCedCommonEvents_Panel,
				 ARCedSystem_Panel.ARCedSystem_Panel)
		for i in range(len(pages)):
			nb.AddPage(pages[i](nb), tabs[i], False, i)
		self.frame.Show()

if __name__ == '__main__':
	app = ARCedTest()
	app.MainLoop()
	app.Destroy()