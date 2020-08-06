import bpy
from bpy.props import (
    IntProperty,
    BoolProperty,
    FloatProperty,
    PointerProperty,
    CollectionProperty,
    FloatVectorProperty,
    StringProperty,
    EnumProperty,
)
from RealCaustics.utils import alert

# pylint: disable=assignment-from-no-return
# pylint: disable=no-member
# pylint: disable=unused-variable


def set_object_settings(scene):
    pass


def add_light(scene, light):

    if bpy.data.collections.find(f"light{id(light)}") != -1:
        return None
    bpy.data.collections.new(f"light{id(light)}")
    new_light = scene.LightSelector.lights.add()
    new_light.light = light
    new_light.name = light.name
    scene.LightSelector.light_index = len(scene.LightSelector.lights) - 1
    set_object_settings(scene)
    return None


def remove_light(scene, light, index):
    coll_name = f"light{id(light)}"
    bpy.data.collections.remove(bpy.data.collections[coll_name])
    scene.LightSelector.lights.remove(index)

    if scene.LightSelector.light_index == 0:
        scene.LightSelector.light_index = 0
    else:
        scene.LightSelector.light_index -= 1
    return None


def update_auto_select_lights(self, context):
    self.lights_panel_is_expanded = not self.auto_select_lights
    if self.auto_select_lights:
        bpy.ops.real_caustics.auto_select_lights()
    return None


def update_selected_light(self, context):
    if self.selected_light_name == "":
        return None
    try:
        light = bpy.data.objects[self.selected_light_name]
    except KeyError:
        alert(
            context,
            message="No object with this name in the list",
            top_title="Refresh the list",
        )
        self.selected_object = None
        return None
    self.selected_light = light
    return None


class REAL_CAUSTICS_OT_auto_select_lights(bpy.types.Operator):
    bl_idname = "real_caustics.auto_select_lights"
    bl_label = "Auto Select Catchers"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        all_objects = bpy.data.objects
        scene = context.scene
        bpy.ops.real_caustics.refresh_list_of_lights()
        for ob in all_objects:
            if ob.type != "LIGHT":
                continue
            add_light(scene, ob)
        return {"FINISHED"}


class REAL_CAUSTICS_OT_add_light(bpy.types.Operator):
    bl_idname = "real_caustics.add_light"
    bl_label = "Add Catcher"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_light(bpy.types.Operator):
    bl_idname = "real_caustics.remove_light"
    bl_label = "Remove Light"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        LightSelector = scene.LightSelector
        if not LightSelector.lights:
            return {"FINISHED"}
        if LightSelector.light_index == -1:
            self.report(type={"WARNING"}, message="No object selected")
            return {"FINISHED"}

        remove_light(
            scene,
            LightSelector.lights[LightSelector.light_index].light,
            LightSelector.light_index,
        )
        return {"FINISHED"}


class REAL_CAUSTICS_OT_append_selected_lights(bpy.types.Operator):
    bl_idname = "real_caustics.append_selected_lights"
    bl_label = "Append selected lights"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        scene = context.scene
        selected_objects = context.selected_objects
        for ob in selected_objects:
            if ob.type != "LIGHT":
                continue
            add_light(scene, ob)
        return {"FINISHED"}


class REAL_CAUSTICS_OT_remove_all_lights(bpy.types.Operator):
    bl_idname = "real_caustics.remove_all_lights"
    bl_label = "Remove all lights"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        scene = context.scene
        object_list = scene.LightSelector.lights
        if not object_list:
            return {"FINISHED"}

        for ob in object_list:
            coll_name = f"light{id(ob.light)}"
            bpy.data.collections.remove(bpy.data.collections[coll_name])
        object_list.clear()
        scene.LightSelector.light_index = -1
        return {"FINISHED"}


class REAL_CAUSTICS_OT_refresh_list_of_lights(bpy.types.Operator):
    bl_idname = "real_caustics.refresh_list_of_lights"
    bl_label = "Refresh List of Lights"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        scene = context.scene
        object_list = scene.LightSelector.lights
        new_object_list = []
        for ob in object_list:
            if ob.light.users == 1 or (ob.light.users == 2 and ob.light.use_fake_user):
                coll_name = f"light{id(ob.light)}"
                bpy.data.collections.remove(bpy.data.collections[coll_name])
                bpy.data.objects.remove(ob.catcher)
            else:
                new_object_list.append(ob.light)
        object_list.clear()

        for ob in new_object_list:
            new_light = object_list.add()
            new_light.light = ob
            new_light.name = ob.name
        scene.LightSelector.light_index = -1
        return {"FINISHED"}


class OBJECT_UL_lights(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):

        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if item.light:
                layout.label(text=item.light.name, icon="OUTLINER_DATA_LIGHT")
            else:
                layout.label(text="", icon="OUTLINER_DATA_LIGHT")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon="OUTLINER_DATA_LIGHT")


class Light(bpy.types.PropertyGroup):
    light: PointerProperty(
        name="Light", type=bpy.types.Object,
    )
    name = bpy.props.StringProperty(default="")


class LightSelector(bpy.types.PropertyGroup):
    lights: CollectionProperty(type=Light,)
    light_index: IntProperty(default=0,)
    auto_select_lights: BoolProperty(default=True, update=update_auto_select_lights)
    lights_panel_is_expanded: BoolProperty(default=False,)
    selected_light: PointerProperty(type=bpy.types.Object,)
    selected_light_name: StringProperty(default="", update=update_selected_light)


class LightSettings(bpy.types.PropertyGroup):
    color: FloatVectorProperty(
        name="",
        description="",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        soft_max=1.0,
        subtype="COLOR",
    )
    power: FloatProperty(
        name="", description="", min=0.0, unit="POWER", precision=1, step=10,
    )
    light_type: EnumProperty(
        name="",
        items=[
            ("POINT", "Point", "Point Light", "LIGHT_POINT", 1),
            ("SUN", "Sun", "Directional light", "LIGHT_SUN", 2),
            ("SPOT", "Spot", "Point Light", "LIGHT_SPOT", 3),
            ("AREA", "Area", "Point Light", "LIGHT_AREA", 4),
        ],
        default="POINT",
        description="",
    )


classes = [
    REAL_CAUSTICS_OT_auto_select_lights,
    OBJECT_UL_lights,
    REAL_CAUSTICS_OT_add_light,
    REAL_CAUSTICS_OT_remove_light,
    REAL_CAUSTICS_OT_append_selected_lights,
    REAL_CAUSTICS_OT_refresh_list_of_lights,
    REAL_CAUSTICS_OT_remove_all_lights,
    Light,
    LightSelector,
    LightSettings,
]


def register():
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.LightSelector = PointerProperty(
        type=LightSelector, options={"HIDDEN"}
    )
    bpy.types.Object.lights_settings = PointerProperty(
        type=LightSettings, options={"HIDDEN"}
    )


def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
    del bpy.types.Scene.LightSelector
    del bpy.types.Object.lights_settings

