import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty, CollectionProperty, FloatVectorProperty, StringProperty
# pylint: disable=E1111
def add_mesh(scene, mesh):
    """ Adds Mesh to Caustic Objects"""
    if bpy.data.collections.find(str(id(mesh))) != -1: 
        return None
    bpy.data.collections.find(str(id(mesh)))
    bpy.data.collections.new(str(id(mesh)))
    new_mesh = scene.caustic_meshes.add()
    new_mesh.mesh = mesh
    new_mesh.name = mesh.name
    scene.caustic_mesh_idx = len(scene.caustic_meshes) - 1
    scene.mesh_to_add = None

def remove_mesh(scene, mesh, index):
    coll_name = str(id(mesh))  
    bpy.data.collections.remove(bpy.data.collections[coll_name])
    scene.caustic_meshes.remove(index)
    if scene.caustic_mesh_idx == 0:
            scene.caustic_mesh_idx = 0
    else:
        scene.caustic_mesh_idx -= 1

def alert(context):

    def draw(self, context):
        self.layout.label(text = "Refresh the list")

    context.window_manager.popup_menu(draw, title = "No object with this name", icon = 'ERROR')


def update_selected_settings_object(self, context):
    try:
        ob = bpy.data.objects[self.selected_object_name]
    except KeyError:
        alert(context)
        self.selected_object = None
        return None         
    self.selected_object = ob
    return None


class REAL_CAUSTICS_OT_auto_select_objects(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_objects"
    bl_label = "Auto Select Objects"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        all_objects = bpy.data.objects
        scene = context.scene
        for bl_object in all_objects:
            if not bl_object.active_material:
                continue 

            nodes = bl_object.active_material.node_tree.nodes
            for node in nodes:
                if (node.bl_idname != "ShaderNodeBsdfGlass" and node.bl_idname != "ShaderNodeBsdfPrincipled"
                    and node.bl_idname != "ShaderNodeBsdfRefraction"):
                    continue
                elif node.bl_idname == "ShaderNodeBsdfPrincipled":
                    inputs = node.inputs
                    if ((inputs[4].default_value > 0.95 or inputs[15].default_value > 0.95)
                         and inputs[7].default_value < 0.1):
                        add_mesh(scene, bl_object)
                        print(inputs[7].default_value)
                    else:
                        continue
                elif node.bl_idname == "ShaderNodeBsdfGlass":
                    inputs = node.inputs
                    if inputs[1].default_value < 0.1:
                        add_mesh(scene, bl_object)
                    else:
                        continue
                elif node.bl_idname == "ShaderNodeBsdfRefraction":
                    inputs = node.inputs
                    if inputs[1].default_value < 0.1:
                        add_mesh(scene, bl_object)
                    else:
                        continue


                     

        
        return {"FINISHED"}

class REAL_CAUSTICS_OT_add_mesh(bpy.types.Operator):
    bl_idname = "real_caustics.add_mesh"
    bl_label = "Add Mesh"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene

        if not scene.mesh_to_add:
            self.report(type = {'WARNING'}, message = "No Active object selected")
            return {"FINISHED"}

        add_mesh(scene, scene.mesh_to_add)
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_mesh(bpy.types.Operator):
    bl_idname = "real_caustics.remove_mesh"
    bl_label = "Remove Mesh"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        
        if not scene.caustic_meshes:
            return {"FINISHED"}
        if scene.caustic_mesh_idx == -1:
            self.report(type = {'WARNING'}, message = "No object selected") 
            return {"FINISHED"}
        coll_name = str(id(scene.caustic_meshes[scene.caustic_mesh_idx].mesh))  
        bpy.data.collections.remove(bpy.data.collections[coll_name])
        scene.caustic_meshes.remove(scene.caustic_mesh_idx)
        if scene.caustic_mesh_idx == 0:
            scene.caustic_mesh_idx = 0
        else:
            scene.caustic_mesh_idx -= 1
        return {"FINISHED"}

class REAL_CAUSTICS_OT_append_selected_meshes(bpy.types.Operator):
    bl_idname = "real_caustics.append_selected_meshes"
    bl_label = "Append selected meshes"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        selected_objects = context.selected_objects
        for ob in selected_objects:
            if ob.type != "MESH":
                continue
            add_mesh(scene, ob)
        return {"FINISHED"}

class REAL_CAUSTICS_OT_refresh_list(bpy.types.Operator):
    bl_idname = "real_caustics.refresh_list"
    bl_label = "Refresh List"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        object_list = scene.caustic_meshes
        new_object_list = []
        for ob in object_list:
            if ob.mesh.users == 1 or (ob.mesh.users == 2 and ob.mesh.use_fake_user):
                coll_name = str(id(ob.mesh))  
                bpy.data.collections.remove(bpy.data.collections[coll_name])         
            else:
                new_object_list.append(ob.mesh) 
        object_list.clear()

        for mesh in new_object_list:
            new_mesh = object_list.add()
            new_mesh.mesh = mesh
            new_mesh.name = mesh.name

        scene.caustic_mesh_idx = -1 
        return {"FINISHED"}

class REAL_CAUSTICS_OT_remove_all_objects(bpy.types.Operator):
    bl_idname = "real_caustics.remove_all_objects"
    bl_label = "Remove all objects"
    bl_options = {"INTERNAL"}
    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if not context.scene.caustic_meshes:
            return {"FINISHED"}    
        scene = context.scene
        object_list = scene.caustic_meshes
        for ob in object_list:
            coll_name = str(id(ob.mesh))  
            bpy.data.collections.remove(bpy.data.collections[coll_name])
        object_list.clear()
        return {"FINISHED"}


class OBJECT_UL_caustic_meshes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.mesh:
                layout.label(text = item.mesh.name, icon = "MESH_DATA")
            else:
                layout.label(text = "", icon = "MESH_DATA")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "MESH_DATA")



class MeshCollection(bpy.types.PropertyGroup):
    mesh: PointerProperty(
        name = "Mesh",
        type = bpy.types.Object,
    )
    name = bpy.props.StringProperty(default = "dwadaw")


class ObjectSettings(bpy.types.PropertyGroup):
    color: FloatVectorProperty(
        name = "",
        description = "",
        default = (0.0, 0.0, 0.0),
        min = 0.0,
        max = 1.0,
        subtype = 'COLOR',

    )
    roughness: FloatProperty(
        name = "",
        description = "",
        min = 0.0,
        max = 0.1,
        subtype = 'FACTOR',
        precision = 3,
    )
    ior: FloatProperty(
        name = "",
        description = "",
        min = 0.0,
        default = 1.33
    )


classes = [
    REAL_CAUSTICS_OT_auto_select_objects,
    OBJECT_UL_caustic_meshes,
    MeshCollection,
    REAL_CAUSTICS_OT_add_mesh,
    REAL_CAUSTICS_OT_remove_mesh,
    REAL_CAUSTICS_OT_append_selected_meshes,
    REAL_CAUSTICS_OT_refresh_list,
    REAL_CAUSTICS_OT_remove_all_objects,
    ObjectSettings,
]

def register():
    
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.caustic_meshes = CollectionProperty(type = MeshCollection, options = {"HIDDEN"})
    bpy.types.Scene.caustic_mesh_idx = IntProperty(default = 0, options = {"HIDDEN"})
    bpy.types.Scene.mesh_to_add = PointerProperty(type = bpy.types.Object, options = {"HIDDEN"})
    bpy.types.Object.object_settings = PointerProperty(type = ObjectSettings, options = {"HIDDEN"})
    bpy.types.Scene.selected_object_name = StringProperty(default = "", options = {'HIDDEN'}, update = update_selected_settings_object)
    bpy.types.Scene.selected_object = PointerProperty(type = bpy.types.Object, options = {'HIDDEN'})
    

def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.caustic_meshes
    del bpy.types.Scene.caustic_mesh_idx 
    del bpy.types.Scene.mesh_to_add
    del bpy.types.Object.object_settings
    del bpy.types.Scene.selected_object_name
    del bpy.types.Scene.selected_object 
  
