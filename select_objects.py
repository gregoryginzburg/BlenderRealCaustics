import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty, CollectionProperty
# pylint: disable=E1111

class REAL_CAUSTICS_OT_auto_select_objects(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_objects"
    bl_label = "Auto Select Objects"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        return {"FINISHED"}

class REAL_CAUSTICS_OT_add_mesh(bpy.types.Operator):
    bl_idname = "real_caustics.add_mesh"
    bl_label = "Add Mesh"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene

        if not scene.mesh_to_add:
            self.report(type = {'ERROR'}, message = "No Active object selected")
            return {"FINISHED"}

        new_mesh = scene.caustic_meshes.add()
        new_mesh.mesh = scene.mesh_to_add
        scene.caustic_mesh_idx = len(scene.caustic_meshes) - 1
        return {"FINISHED"}



class REAL_CAUSTICS_OT_remove_mesh(bpy.types.Operator):
    bl_idname = "real_caustics.remove_mesh"
    bl_label = "Remove Mesh"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        
        if not scene.caustic_meshes:
            return {"FINISHED"}
        
        scene.caustic_meshes.remove(scene.caustic_mesh_idx)
        if scene.caustic_mesh_idx == 0:
            scene.caustic_mesh_idx = 0
        else:
            scene.caustic_mesh_idx -= 1
        return {"FINISHED"}


class OBJECT_UL_caustic_meshes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.mesh:
                layout.label(text = item.mesh.name_full, icon = "MESH_DATA")
            else:
                layout.label(text = "", icon = "MESH_DATA")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "MESH_DATA")
    def invoke(self, context, event):
        pass








class MeshCollection(bpy.types.PropertyGroup):
    mesh: PointerProperty(
        name = "Mesh",
        type = bpy.types.Mesh,
    )





classes = [
    REAL_CAUSTICS_OT_auto_select_objects,
    OBJECT_UL_caustic_meshes,
    MeshCollection,
    REAL_CAUSTICS_OT_add_mesh,
    REAL_CAUSTICS_OT_remove_mesh,
]
def register():
    
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.caustic_meshes = CollectionProperty(type = MeshCollection, options = {"HIDDEN"})
    bpy.types.Scene.caustic_mesh_idx = IntProperty(default = 0, options = {"HIDDEN"})
    bpy.types.Scene.mesh_to_add = PointerProperty(type = bpy.types.Mesh, options = {"HIDDEN"})

def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.caustic_meshes
    del bpy.types.Scene.caustic_mesh_idx 
    del bpy.types.Scene.mesh_to_add
