import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty

# pylint: disable=assignment-from-no-return
# pylint: disable=no-member
# pylint: disable=unused-variable


def update_camera_resolution(self, context):
    pass


class REAL_CAUSTICS_OT_generate_caustics(bpy.types.Operator):
    bl_idname = "real_caustics.generate_caustics"
    bl_label = "Generate Caustics"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        return {"FINISHED"}


class CausticsSettings(bpy.types.PropertyGroup):
    resolution_percentage: IntProperty(
        name="",
        description="Scaling factor",
        default=100,
        min=0,
        max=100,
        subtype="PERCENTAGE",
    )
    photons_count: FloatProperty(
        name="",
        description="Number of emitted photons (millions)",
        default=5.0,
        min=0.1,
        soft_max=100.0,
        step=10,
        precision=1,
    )
    search_radius: FloatProperty(
        name="",
        description="Photons radius search",
        default=0.015,
        min=0.0001,
        precision=4,
        soft_max=1.0,
        subtype="DISTANCE",
    )
    max_cache_photons: IntProperty(
        name="",
        description="Max numbers of photons in cache",
        default=200,
        min=0,
        soft_max=10000,
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
