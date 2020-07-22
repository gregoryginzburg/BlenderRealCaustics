import bpy

class REAL_CAUSTICS_OT_auto_select_objects(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_objects"
    bl_label = "Auto Select Objects"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        return {"FINISHED"}




classes = [
    REAL_CAUSTICS_OT_auto_select_objects
]
def register():
    for blender_class in classes:
        bpy.utils.register_class(blender_class)

def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
