# import QtWindowOne
# import QtFunctions
# QtFunctions.spawnQtWindow(QtWindowOne.QtWindowOne)

import sys
import unreal
from PySide6 import QtGui, QtWidgets, QtUiTools

WINDOW_NAME = 'My Test'
UI_FILE_FULLNAME = __file__.replace('.py', '.ui')

class QtWindowOne(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(QtWindowOne, self).__init__(parent)
		self.aboutToClose = None # This is used to stop the tick when the window is closed
		self.widget = QtUiTools.QUiLoader().load(UI_FILE_FULLNAME)
		self.widget.setParent(self)
		self.setWindowTitle(WINDOW_NAME)
		self.setGeometry(100, 100, self.widget.width(), self.widget.height())
		self.initialiseWidget()

	def closeEvent(self, event):
		if self.aboutToClose:
			self.aboutToClose(self)
		event.accept()

	def eventTick(self, delta_seconds):
		self.myTick(delta_seconds)


	##########################################


	def initialiseWidget(self):
		self.time_while_this_window_is_open = 0.0
		self.random_actor = None
		self.widget.pathtracing_on_button.clicked.connect(self.rotateSelectedActorInScene)
		self.widget.quit_button.clicked.connect(self.closewindow)

	def openPathTracing(self):
		# Create a ChangeViewMode instance with default values
		# view_mode_change = unreal.ChangeViewMode()
		# view_mode_change.view_mode = unreal.ViewModeIndex.VMI_WIREFRAME

		return unreal.CppLib.get_active_viewport_index()



	def closewindow(self):
		self.time_while_this_window_is_open = 0.0
		self.random_actor = None
		self.destroy()

	def rotateSelectedActorInScene(self):
		import WorldFunctions
		selected_actors = WorldFunctions.getAllActors(use_selection = True, actor_class = unreal.HoudiniAssetActor, actor_tag = None)
		self.random_actor = selected_actors[0]
		print(selected_actors)

	def myTick(self, delta_seconds):
		# Set Time
		self.time_while_this_window_is_open += delta_seconds
		self.widget.lbl_Seconds.setText("%.1f Seconds" % self.time_while_this_window_is_open)
		# Affect Actor
		if self.random_actor:
			speed = 90.0 * delta_seconds
			self.random_actor.add_actor_world_rotation(unreal.Rotator(0.0, 0.0, speed), False, False)