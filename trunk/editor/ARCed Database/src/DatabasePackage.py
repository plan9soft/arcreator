'''
Exports all the core components of the Database to the kernel
'''
from ARCedActors_Panel import ARCedActors_Panel
from ARCedClasses_Panel import ARCedClasses_Panel
from ARCedSkills_Panel import ARCedSkills_Panel
from ARCedItems_Panel import ARCedItems_Panel
from ARCedWeapons_Panel import ARCedWeapons_Panel
from ARCedArmors_Panel import ARCedArmors_Panel
from ARCedEnemies_Panel import ARCedEnemies_Panel
from ARCedTroops_Panel import ARCedTroops_Panel
from ARCedStates_Panel import ARCedStates_Panel
from ARCedAnimations_Panel import ARCedAnimations_Panel
from ARCedTilesets_Panel import ARCedTilesets_Panel
from ARCedCommonEvents_Panel import ARCedCommonEvents_Panel
from ARCedSystem_Panel import ARCedSystem_Panel

import Kernel
from Kernel import Manager, Type, SuperType, Component, Package, Event

#=============================================================================
# * Package Declaration
#=============================================================================
class DatabasePackage(Package):

	def __init__(self):
		Package.__init__(self, "DATABASE", "CORE")
		self.setup_types()
		self.setup_events()
		self.setup_components()

	def setup_types(self):
		#=============================================================================
		# * Type Declaration 
		#=============================================================================
		#------------------------------ functions ------------------------------------

		#---------------------------- Data handlers ----------------------------------

		#------------------------------- frames --------------------------------------


		#-------------------------------- ctrls --------------------------------------

		#-------------------------------- layouts ------------------------------------
		MainActorsPanel = Type("MainActorsPanel")
		MainClassesPanel = Type("MainClassesPanel")
		MainSkillsPanel = Type("MainSkillsPanel")
		MainItemsPanel = Type("MainItemsPanel")
		MainWeaponsPanel = Type("MainWeaponsPanel")
		MainArmorsPanel = Type("MainArmorsPanel")
		MainEnemiesPanel = Type("MainEnemiesPanel")
		MainTroopsPanel = Type("MainTroopsPanel")
		MainStatesPanel = Type("MainStatesPanel")
		MainAnimationsPanel = Type("MainAnimationsPanel")
		MainTilesetsPanel = Type("MainTilesetsPanel")
		MainCommonEventsPanel = Type("MainCommonEventsPanel")
		MainSystemPanel = Type("MainSystemPanel")

		#-------------------------------- menus --------------------------------------

		#------------------------------- dialogs -------------------------------------


		#-------------------------------actions---------------------------------------

		#=====================================================================
		# * add the types to be registered 
		#=====================================================================
		#------------------------------ super types ----------------------------------
		#self.add_types()

		#------------------------------- functions -----------------------------------
		#self.add_types()

		#------------------------------ data handlers --------------------------------
		#self.add_types()

		#-------------------------------- frames -------------------------------------
		#self.add_types()

		#-------------------------------- ctrls --------------------------------------
		#self.add_types()

		#-------------------------------- layouts --------------------------------
		self.add_types(MainActorsPanel, MainClassesPanel, MainSkillsPanel, 
				MainItemsPanel, MainWeaponsPanel, MainArmorsPanel, MainEnemiesPanel, 
				MainTroopsPanel, MainStatesPanel, MainAnimationsPanel, MainTilesetsPanel, 
				MainCommonEventsPanel, MainSystemPanel)
		#-------------------------------- menus --------------------------------------
		#self.add_types()

		#-------------------------------- dialogs ------------------------------------
		#self.add_types()

		#-------------------------------actions---------------------------------------
		#self.add_types()

		#self.add_types()

	def setup_events(self):
		pass
		
		#=============================================================================
		# * events
		#=============================================================================

		#=====================================================================
		# * add the events to be registered 
		#=====================================================================

		#self.add_events()

		#=====================================================================
		# * add even hooks to be registered
		#=====================================================================
		#self.add_event_hook()

	def setup_components(self):
		#=====================================================================
		# * add components (main components)
		#=====================================================================

		#--------------------------- functions -------------------------------

		#-------------------------- data Handler -----------------------------

		#---------------------------- frames ---------------------------------


		#----------------------------- ctrls ---------------------------------


		#----------------------------- layouts -------------------------------
		
		self.add_component(Component(ARCedActors_Panel, "MainActorsLayout", 
							   None, "COREMainActorsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedClasses_Panel, "MainClassesLayout", 
							   None, "COREMainClassesLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedSkills_Panel, "MainSkillsLayout", 
							   None, "COREMainSkillsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedItems_Panel, "MainItemsLayout", 
							   None, "COREMainItemsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedWeapons_Panel, "MainWeaponsLayout", 
							   None, "COREMainWeaponsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedArmors_Panel, "MainArmorsLayout", 
							   None, "COREMainArmorsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedEnemies_Panel, "MainEnemiesLayout", 
							   None, "COREMainEnemiesLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedTroops_Panel, "MainTroopsLayout", 
							   None, "COREMainTroopsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedStates_Panel, "MainStatesLayout", 
							   None, "COREMainStatesLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedAnimations_Panel, "MainAnimationsLayout", 
							   None, "COREMainAnimationsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedTilesets_Panel, "MainTilesetsLayout", 
							   None, "COREMainTilesetsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedCommonEvents_Panel, "MainCommonEventsLayout", 
							   None, "COREMainCommonEventsLayout", "CORE", 1.0, self))
		self.add_component(Component(ARCedSystem_Panel, "MainSystemLayout", 
							   None, "COREMainSystemLayout", "CORE", 1.0, self))

		#----------------------------- menus ---------------------------------

		#---------------------------- dialogs --------------------------------


package = DatabasePackage()
key = Manager.add_package(package)

# this line is only here because it is the core and should be enabled by default, 
# if it was a normal plug-in it would be enabled else where
Manager.enable_packages(key)



