import bpy
from bpy.props import (
    IntProperty,
    BoolProperty,
    FloatProperty,
    PointerProperty,
    CollectionProperty,
    FloatVectorProperty,
    StringProperty,
)
from RealCaustics.utils import alert

# import utils
# pylint: disable=assignment-from-no-return
# pylint: disable=no-member
# pylint: disable=unused-variable


def set_catcher_settings():
    pass


def add_catcher(scene, catcher):
    CatcherSelector = scene.CatcherSelector
    if bpy.data.collections.find(f"catcher{id(catcher)}") != -1:
        return None
    bpy.data.collections.new(f"catcher{id(catcher)}")
    new_catcher = CatcherSelector.catchers.add()
    new_catcher.catcher = catcher
    new_catcher.name = catcher.name
    CatcherSelector.catchers_index = len(CatcherSelector.catchers) - 1
    set_catcher_settings()
    return None


def remove_catcher(scene, catcher, index):
    CatcherSelector = scene.CatcherSelector
    coll_name = f"catcher{id(catcher)}"
    bpy.data.collections.remove(bpy.data.collections[coll_name])
    CatcherSelector.catchers.remove(index)
    if CatcherSelector.catchers_index == 0:
        CatcherSelector.catchers_index = 0
    else:
        CatcherSelector.catchers_index -= 1
    return None


def update_auto_select_catchers(self, context):
    self.catchers_panel_is_expanded = not self.auto_select_catchers
    if self.auto_select_catchers:
        # pylint: disable=fixme, line-too-long
        bpy.ops.real_caustics.auto_select_catchers()
    return None


def update_selected_catcher(self, context):
    if self.selected_catcher_name == "":
        return None
    try:
        ob = bpy.data.objects[self.selected_catcher_name]
    except KeyError:
        alert(
            context,
            message="No object with this name in the list",
            top_title="Refresh the list",
        )
        self.selected_catcher = None
        return None
    self.selected_catcher = ob
    return None


class REAL_CAUSTICS_OT_auto_select_catchers(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_catchers"
    bl_label = "Auto Select Catchers"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        all_objects = bpy.data.objects
        scene = context.scene
        bpy.ops.real_caustics.refresh_list_of_catchers()
        for ob in all_objects:
            if not ob.active_material:
                continue
            nodes = ob.active_material.node_tree.nodes
            for node in nodes:
                if (node.bl_idname != "ShaderNodeBsdfDiffuse"
                        and node.bl_idname != "ShaderNodeBsdfPrincipled"):
                    continue
                elif node.bl_idname == "ShaderNodeBsdfPrincipled":
                    inputs = node.inputs
                    if (inputs[4].default_value < 0.05
                            or inputs[15].default_value < 0.05):
                        add_catcher(scene, ob)
                    else:
                        continue
                elif node.bl_idname == "ShaderNodeBsdfDiffuse":
                    add_catcher(scene, ob)
        return {"FINISHED"}


class REAL_CAUSTICS_OT_add_catcher(bpy.types.Operator):
    bl_idname = "real_caustics.add_catcher"
    bl_label = "Add Catcher"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_catcher(bpy.types.Operator):
    bl_idname = "real_caustics.remove_catcher"
    bl_label = "Remove Catcher"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        CatcherSelector = scene.CatcherSelector
        if not CatcherSelector.catchers:
            return {"FINISHED"}
        if CatcherSelector.catchers_index == -1:
            self.report(type={"WARNING"}, message="No object selected")
            return {"FINISHED"}

        remove_catcher(
            scene,
            CatcherSelector.catchers[CatcherSelector.catchers_index].catcher,
            CatcherSelector.catchers_index,
        )
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

    def execute(self, context):
        scene = context.scene
        CatcherSelector = scene.CatcherSelector
        object_list = CatcherSelector.catchers
        new_object_list = []
        for ob in object_list:
            if ob.catcher.users == 1 or (ob.catcher.users == 2
                                         and ob.catcher.use_fake_user):
                coll_name = f"catcher{id(ob.catcher)}"
                bpy.data.collections.remove(bpy.data.collections[coll_name])
                bpy.data.objects.remove(ob.catcher)
            else:
                new_object_list.append(ob.catcher)
        object_list.clear()

        for catcher in new_object_list:
            new_catcher = object_list.add()
            new_catcher.catcher = catcher
            new_catcher.name = catcher.name
        CatcherSelector.catchers_index = -1
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_all_catchers(bpy.types.Operator):
    bl_idname = "real_caustics.remove_all_catchers"
    bl_label = "Remove all catchers"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        CatcherSelector = context.scene.CatcherSelector
        if not CatcherSelector.catchers:
            return {"FINISHED"}
        object_list = CatcherSelector.catchers
        for ob in object_list:
            coll_name = f"catcher{id(ob.catcher)}"
            bpy.data.collections.remove(bpy.data.collections[coll_name])
        object_list.clear()
        return {"FINISHED"}


class OBJECT_UL_caustic_catchers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if item.catcher:
                layout.label(text=item.catcher.name, icon="VIEW_PERSPECTIVE")
            else:
                layout.label(text="", icon="VIEW_PERSPECTIVE")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon="VIEW_PERSPECTIVE")


class Catcher(bpy.types.PropertyGroup):
    catcher: PointerProperty(
        name="Catcher",
        type=bpy.types.Object,
    )
    name = bpy.props.StringProperty(default="")


class CatcherSelector(bpy.types.PropertyGroup):
    catchers: CollectionProperty(type=Catcher, )
    catchers_index: IntProperty(default=0, )
    auto_select_catchers: BoolProperty(
        default=True,
        update=update_auto_select_catchers,
    )
    catchers_panel_is_expanded: BoolProperty(default=False, )
    selected_catcher: PointerProperty(type=bpy.types.Object, )
    selected_catcher_name: StringProperty(update=update_selected_catcher, )


classes = [
    REAL_CAUSTICS_OT_auto_select_catchers,
    OBJECT_UL_caustic_catchers,
    REAL_CAUSTICS_OT_add_catcher,
    REAL_CAUSTICS_OT_remove_catcher,
    REAL_CAUSTICS_OT_append_selected_catchers,
    REAL_CAUSTICS_OT_refresh_list_of_catchers,
    REAL_CAUSTICS_OT_remove_all_catchers,
    Catcher,
    CatcherSelector,
]


def register():
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.CatcherSelector = PointerProperty(type=CatcherSelector,
                                                      options={"HIDDEN"})


def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.CatcherSelector
