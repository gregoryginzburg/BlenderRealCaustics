import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty
# pylint: disable=E1111


def update_camera_resolution(self, context):
    pass


class REAL_CAUSTICS_OT_generate_caustics(bpy.types.Operator):
    bl_idname = "real_caustics.generate_caustics"
    bl_label = "Generate Caustics"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        context.active_object.data.test_mesh = True
        return {"FINISHED"}


class CausticsSettings(bpy.types.PropertyGroup):
    resolution_x: IntProperty(
        name = "",
        description = "Number of horizontal pixels in rendered image",
        default = 1920,
        min = 4,
        subtype = 'PIXEL'
    )
    resolution_y: IntProperty(
        name = "",
        description = "Number of vertical pixels in rendered image",
        default = 1080,
        min = 4,
        subtype = 'PIXEL'
    )
    synchronize_with_camera: BoolProperty(
        name = "",
        description = "Synchronize with active camera",
        default = True,
        update = update_camera_resolution,
    )
    photons_count: FloatProperty(
        name = "",
        description = "Number of emitted photons (millions)",
        default = 5.0,
        min = 0.1,
        soft_max = 100.0,
        step = 10,
        precision = 1,
    )
    search_radius: FloatProperty(
        name = "",
        description = "Photons radius search",
        default = 0.015,
        min = 0.0001,
        precision = 4,
        soft_max = 1.0,
        subtype = 'DISTANCE'
    )


classes = [
    REAL_CAUSTICS_OT_generate_caustics,
    CausticsSettings,
]


def register():

    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.caustics_settings = PointerProperty(
        type=CausticsSettings, options={"HIDDEN"}
    )


def unregister():
    del bpy.types.Scene.caustics_settings
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
