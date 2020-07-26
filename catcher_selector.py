import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty, CollectionProperty, FloatVectorProperty, StringProperty
# pylint: disable=E1111
def add_catcher(scene, mesh):
    """ Adds Mesh to Caustic Objects"""
    if bpy.data.collections.find(f"catcher{id(mesh)}") != -1: 
        return None
    bpy.data.collections.new(f"catcher{id(mesh)}")
    new_mesh = scene.catcher_meshes.add()
    new_mesh.catcher = mesh
    new_mesh.name = mesh.name
    scene.catcher_mesh_idx = len(scene.catcher_meshes) - 1
    scene.catcher_to_add = None

def remove_catcher(scene, mesh, index):
    coll_name = f"catcher{id(mesh)}"  
    bpy.data.collections.remove(bpy.data.collections[coll_name])
    scene.catcher_meshes.remove(index)
    if scene.catcher_mesh_idx == 0:
        scene.catcher_mesh_idx = 0
    else:
        scene.catcher_mesh_idx -= 1



class REAL_CAUSTICS_OT_auto_select_catchers(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_catchers"
    bl_label = "Auto Select Catchers"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        all_objects = bpy.data.objects
        scene = context.scene
        bpy.ops.real_caustics.refresh_list_of_catchers('INVOKE_DEFAULT')
        for bl_object in all_objects:
            if not bl_object.active_material:
                continue 

            nodes = bl_object.active_material.node_tree.nodes
            for node in nodes:
                if (node.bl_idname != "ShaderNodeBsdfDiffuse" and node.bl_idname != "ShaderNodeBsdfPrincipled"):
                    continue
                elif node.bl_idname == "ShaderNodeBsdfPrincipled":
                    inputs = node.inputs
                    if ((inputs[4].default_value < 0.05 or inputs[15].default_value < 0.05)):
                        add_catcher(scene, bl_object)
                    else:
                        continue
                elif node.bl_idname == "ShaderNodeBsdfDiffuse":
                    add_catcher(scene, bl_object)    
        return {"FINISHED"}

class REAL_CAUSTICS_OT_add_catcher(bpy.types.Operator):
    bl_idname = "real_caustics.add_catcher"
    bl_label = "Add Catcher"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene

        if not scene.catcher_to_add:
            self.report(type = {'WARNING'}, message = "No Active object selected")
            return {"FINISHED"}

        add_catcher(scene, scene.catcher_to_add)
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_catcher(bpy.types.Operator):
    bl_idname = "real_caustics.remove_catcher"
    bl_label = "Remove Catcher"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        
        if not scene.catcher_meshes:
            return {"FINISHED"}
        if scene.catcher_mesh_idx == -1:
            self.report(type = {'WARNING'}, message = "No object selected") 
            return {"FINISHED"}

        remove_catcher(scene, scene.catcher_meshes[scene.catcher_mesh_idx].catcher, scene.catcher_mesh_idx)
        return {"FINISHED"}

class REAL_CAUSTICS_OT_append_selected_catchers(bpy.types.Operator):
    bl_idname = "real_caustics.append_selected_catchers"
    bl_label = "Append selected catchers"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        selected_objects = context.selected_objects
        for ob in selected_objects:
            if ob.type != "MESH":
                continue
            add_catcher(scene, ob)
        return {"FINISHED"}

class REAL_CAUSTICS_OT_refresh_list_of_catchers(bpy.types.Operator):
    bl_idname = "real_caustics.refresh_list_of_catchers"
    bl_label = "Refresh List of Catchers"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        object_list = scene.catcher_meshes
        new_object_list = []
        for ob in object_list:
            if ob.catcher.users == 1 or (ob.catcher.users == 2 and ob.catcher.use_fake_user):
                coll_name = f"catcher{id(ob.catcher)}"  
                bpy.data.collections.remove(bpy.data.collections[coll_name])
                bpy.data.objects.remove(ob.catcher)         
            else:
                new_object_list.append(ob.catcher) 
        object_list.clear()

        for mesh in new_object_list:
            new_mesh = object_list.add()
            new_mesh.catcher = mesh
            new_mesh.name = mesh.name
        scene.catcher_mesh_idx = -1 
        return {"FINISHED"}

class REAL_CAUSTICS_OT_remove_all_catchers(bpy.types.Operator):
    bl_idname = "real_caustics.remove_all_catchers"
    bl_label = "Remove all catchers"
    bl_options = {"INTERNAL"}
    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if not context.scene.catcher_meshes:
            return {"FINISHED"}    
        scene = context.scene
        object_list = scene.catcher_meshes
        for ob in object_list:
            coll_name = f"catcher{id(ob.catcher)}" 
            bpy.data.collections.remove(bpy.data.collections[coll_name])
        object_list.clear()
        return {"FINISHED"}


class OBJECT_UL_caustic_catchers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.catcher:
                layout.label(text = item.catcher.name, icon = "VIEW_PERSPECTIVE")
            else:
                layout.label(text = "", icon = "MESH_DATA")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "MESH_DATA")



class CatcherCollection(bpy.types.PropertyGroup):
    catcher: PointerProperty(
        name = "Catcher",
        type = bpy.types.Object,
    )
    name = bpy.props.StringProperty(default = "")




classes = [
    REAL_CAUSTICS_OT_auto_select_catchers,
    OBJECT_UL_caustic_catchers,
    CatcherCollection,
    REAL_CAUSTICS_OT_add_catcher,
    REAL_CAUSTICS_OT_remove_catcher,
    REAL_CAUSTICS_OT_append_selected_catchers,
    REAL_CAUSTICS_OT_refresh_list_of_catchers,
    REAL_CAUSTICS_OT_remove_all_catchers,
]
def update_auto_select_catchers_is_on(self, context):
    self.auto_selector_catchers_is_expanded = not self.auto_select_catchers_is_on
    return None
def register():   
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.catcher_meshes = CollectionProperty(type = CatcherCollection, options = {"HIDDEN"})
    bpy.types.Scene.catcher_mesh_idx = IntProperty(default = 0, options = {"HIDDEN"})
    bpy.types.Scene.auto_select_catchers_is_on = BoolProperty(default = True, update = update_auto_select_catchers_is_on)
    bpy.types.Scene.auto_selector_catchers_is_expanded = BoolProperty(default = False) 
    

def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.catcher_meshes
    del bpy.types.Scene.catcher_mesh_idx
    del bpy.types.Scene.auto_select_catchers_is_on
    del bpy.types.Scene.auto_selector_catchers_is_expanded  
  
