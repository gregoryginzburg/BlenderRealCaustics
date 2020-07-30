import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty, CollectionProperty, FloatVectorProperty, StringProperty
# from utils import alert
# pylint: disable=E1111


def set_object_settings():
    pass


def add_caustic_object(scene, caustic_object):

    if bpy.data.collections.find(f"caustic_object{id(caustic_object)}") != -1: 
        return None
    bpy.data.collections.new(f"caustic_object{id(caustic_object)}")
    new_caustic_object = scene.ObjectSelector.caustic_objects.add()
    new_caustic_object.caustic_object = caustic_object
    new_caustic_object.name = caustic_object.name
    scene.ObjectSelector.caustic_objects_index = len(scene.ObjectSelector.caustic_objects) - 1
    set_object_settings()


def remove_caustic_object(scene, caustic_object, index):
    ObjectSelector = scene.ObjectSelector   
    coll_name = f"caustic_object{id(caustic_object)}"  
    bpy.data.collections.remove(bpy.data.collections[coll_name])
    ObjectSelector.caustic_objects.remove(index)
    if ObjectSelector.caustic_objects_index == 0:
        ObjectSelector.caustic_objects_index = 0
    else:
        ObjectSelector.caustic_objects_index -= 1



def update_auto_select_caustic_objects(self, context):
    self.caustic_objects_panel_is_expanded = not self.auto_select_caustic_objects
    if self.auto_select_caustic_objects:
        bpy.ops.real_caustics.auto_select_caustic_objects() 
    return None


def update_selected_caustic_object(self, context):
    if self.selected_caustic_object_name == "":
        return None
    try:
        ob = bpy.data.objects[self.selected_caustic_object_name]
    except KeyError:
        # alert(context,
        #     message = "No object with this name in the list",
        #     top_title = "Refresh the list",
        # )
        self.selected_caustic_object = None
        return None         
    self.selected_caustic_object = ob
    return None



class REAL_CAUSTICS_OT_auto_select_caustic_objects(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_caustic_objects"
    bl_label = "Auto Select Objects"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        all_objects = bpy.data.objects
        scene = context.scene
        bpy.ops.real_caustics.refresh_list_of_caustic_objects()
        for ob in all_objects:
            if not ob.active_material:
                continue 

            nodes = ob.active_material.node_tree.nodes
            for node in nodes:
                if (node.bl_idname != "ShaderNodeBsdfGlass" and node.bl_idname != "ShaderNodeBsdfPrincipled"
                    and node.bl_idname != "ShaderNodeBsdfRefraction"):
                    continue
                elif node.bl_idname == "ShaderNodeBsdfPrincipled":
                    inputs = node.inputs
                    if ((inputs[4].default_value > 0.95 or inputs[15].default_value > 0.95)
                         and inputs[7].default_value < 0.1):
                        add_caustic_object(scene, ob)
                    else:
                        continue
                elif node.bl_idname == "ShaderNodeBsdfGlass":
                    inputs = node.inputs
                    if inputs[1].default_value < 0.1:
                        add_caustic_object(scene, ob)
                    else:
                        continue
                elif node.bl_idname == "ShaderNodeBsdfRefraction":
                    inputs = node.inputs
                    if inputs[1].default_value < 0.1:
                        add_caustic_object(scene, ob)
                    else:
                        continue
        return {"FINISHED"}

class REAL_CAUSTICS_OT_add_caustic_object(bpy.types.Operator):
    bl_idname = "real_caustics.add_caustic_object"
    bl_label = "Add Mesh"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_caustic_object(bpy.types.Operator):
    bl_idname = "real_caustics.remove_caustic_object"
    bl_label = "Remove Mesh"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        ObjectSelector = scene.ObjectSelector     
        if not ObjectSelector.caustic_objects:
            return {"FINISHED"}
        if ObjectSelector.caustic_objects_index == -1:
            self.report(type = {'WARNING'}, message = "No object selected") 
            return {"FINISHED"}
        coll_name = f"caustic_object{id(ObjectSelector.caustic_objects[ObjectSelector.caustic_objects_index].caustic_object)}" 
        bpy.data.collections.remove(bpy.data.collections[coll_name])
        ObjectSelector.caustic_objects.remove(ObjectSelector.caustic_objects_index)
        if ObjectSelector.caustic_objects_index == 0:
            ObjectSelector.caustic_objects_index = 0
        else:
            ObjectSelector.caustic_objects_index -= 1
        return {"FINISHED"}

class REAL_CAUSTICS_OT_append_selected_caustic_objects(bpy.types.Operator):
    bl_idname = "real_caustics.append_selected_caustic_objects"
    bl_label = "Append selected meshes"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        selected_objects = context.selected_objects
        for ob in selected_objects:
            if ob.type != "MESH":
                continue
            add_caustic_object(scene, ob)
        return {"FINISHED"}

class REAL_CAUSTICS_OT_refresh_list_of_caustic_objects(bpy.types.Operator):
    bl_idname = "real_caustics.refresh_list_of_caustic_objects"
    bl_label = "Refresh List"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        scene = context.scene
        object_list = scene.ObjectSelector.caustic_objects
        new_object_list = []
        for ob in object_list:
            if (ob.caustic_object.users == 1 or 
                (ob.caustic_object.users == 2 and ob.caustic_object.use_fake_user)):
                coll_name = f"caustic_object{id(ob.caustic_object)}"  
                bpy.data.collections.remove(bpy.data.collections[coll_name])
                bpy.data.objects.remove(ob.caustic_object)          
            else:
                new_object_list.append(ob.caustic_object) 
        object_list.clear()

        for ob in new_object_list:
            new_ob = object_list.add()
            new_ob.caustic_object = ob
            new_ob.name = ob.name

        scene.ObjectSelector.caustic_objects_index = -1 
        return {"FINISHED"}

class REAL_CAUSTICS_OT_remove_all_caustic_objects(bpy.types.Operator):
    bl_idname = "real_caustics.remove_all_caustic_objects"
    bl_label = "Remove all objects"
    bl_options = {"INTERNAL"}
    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        ObjectSelector = context.scene.ObjectSelector       
        if not ObjectSelector.caustic_objects:
            return {"FINISHED"}    
        object_list = ObjectSelector.caustic_objects
        for ob in object_list:
            coll_name = f"caustic_object{id(ob.caustic_object)}" 
            bpy.data.collections.remove(bpy.data.collections[coll_name])
        object_list.clear()
        return {"FINISHED"}


class OBJECT_UL_caustic_objects(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.caustic_object:
                layout.label(text = item.caustic_object.name, icon = "MESH_DATA")
            else:
                layout.label(text = "", icon = "MESH_DATA")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "MESH_DATA")



class CausticObject(bpy.types.PropertyGroup):
    caustic_object: PointerProperty(
        name = "Object",
        type = bpy.types.Object,
    )
    name = bpy.props.StringProperty(default = "")
class ObjectSelector(bpy.types.PropertyGroup):
    caustic_objects: CollectionProperty(
        type = CausticObject,
    )
    caustic_objects_index: IntProperty(
        default = 0,
    ) 
    auto_select_caustic_objects: BoolProperty(default = True,
        update = update_auto_select_caustic_objects,      
    )
    caustic_objects_panel_is_expanded: BoolProperty(
        default = False,
    )
    selected_caustic_object: PointerProperty(
        type = bpy.types.Object 
    )
    selected_caustic_object_name: StringProperty(default = "",  
        update = update_selected_caustic_object
    ) 

class ObjectSettings(bpy.types.PropertyGroup):
    color: FloatVectorProperty(
        name = "",
        description = "",
        default = (0.8, 0.8, 0.8),
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
        default = 1.33,
    )


classes = [
    REAL_CAUSTICS_OT_auto_select_caustic_objects,
    OBJECT_UL_caustic_objects,
    REAL_CAUSTICS_OT_add_caustic_object,
    REAL_CAUSTICS_OT_remove_caustic_object,
    REAL_CAUSTICS_OT_append_selected_caustic_objects,
    REAL_CAUSTICS_OT_refresh_list_of_caustic_objects,
    REAL_CAUSTICS_OT_remove_all_caustic_objects,
    CausticObject,
    ObjectSelector,
    ObjectSettings,
]


def register():
    
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.ObjectSelector = PointerProperty(
        type = ObjectSelector,
        options = {"HIDDEN"},
    ) 
    bpy.types.Object.ObjectSettings = PointerProperty(
        type = ObjectSettings,
        options = {"HIDDEN"},
    )
   

def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.ObjectSelector
    del bpy.types.Object.ObjectSettings   
  
