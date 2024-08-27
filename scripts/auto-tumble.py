import maya.cmds as cmds
import maya.api.OpenMaya as om

class AutoTumblePivot:
    def __init__(self):
        self.active = False
        self.selection_job = None
        self.attribute_job = None
        self.create_ui()

    def create_ui(self):
        if cmds.window("autoTumblePivotWindow", exists=True):
            cmds.deleteUI("autoTumblePivotWindow")

        cmds.window("autoTumblePivotWindow", title="Auto Tumble Pivot", widthHeight=(200, 50))
        cmds.columnLayout(adjustableColumn=True)
        self.button = cmds.button(label="Activate Auto Tumble Pivot", command=self.toggle_auto_pivot)
        cmds.showWindow("autoTumblePivotWindow")

def toggle_auto_pivot(self, *args):
    self.active = not self.active
    if self.active:
        cmds.button(self.button, edit=True, label="Deactivate Auto Tumble Pivot", backgroundColor=(0.3, 0.8, 0.3))
        self.selection_job = cmds.scriptJob(event=["SelectionChanged", self.adjust_tumble_pivot])
        self.attribute_job = cmds.scriptJob(event=["DragRelease", self.adjust_tumble_pivot])
    else:
        cmds.button(self.button, edit=True, label="Activate Auto Tumble Pivot", backgroundColor=(0.3, 0.3, 0.3))
        if self.selection_job:
            cmds.scriptJob(kill=self.selection_job)
            self.selection_job = None
        if self.attribute_job:
            cmds.scriptJob(kill=self.attribute_job)
            self.attribute_job = None
        
        # Reset tumble pivot to world origin when deactivating
        panel = cmds.getPanel(withFocus=True)
        cam = cmds.modelEditor(panel, query=True, camera=True)
        cmds.tumbleCtx('tumbleContext', e=True, localTumble=0)
        cmds.setAttr(f"{cam}.tumblePivot", 0, 0, 0)
        print("Tumble pivot reset to world origin.")

    def adjust_tumble_pivot(self):
        if not self.active:
            return
        
        panel = cmds.getPanel(withFocus=True)
        cam = cmds.modelEditor(panel, query=True, camera=True)
        
        selection = cmds.ls(selection=True, long=True)
        
        if selection:
            bbox = cmds.exactWorldBoundingBox(selection)
            center = [(bbox[0] + bbox[3]) / 2, (bbox[1] + bbox[4]) / 2, (bbox[2] + bbox[5]) / 2]
        else:
            center = [0, 0, 0]  # Reset to origin when nothing is selected
        
        cmds.tumbleCtx('tumbleContext', e=True, localTumble=0)
        cmds.setAttr(f"{cam}.tumblePivot", *center)
        
        status = "adjusted to selection" if selection else "reset to origin"
        print(f"Tumble pivot {status}.")

# Create an instance of the AutoTumblePivot class
auto_tumble_pivot = AutoTumblePivot()