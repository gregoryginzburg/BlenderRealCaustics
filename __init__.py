import bpy

# pylint: disable=E1111
bl_info = {
    "name": "Real Caustics",
    "author": "Dev",
    "description": "Generate Caustics",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "dwadwa",
    "warning": "dwadwad",
    "category": "Render",
    "doc_url": "dawdwa",
    "tracker_url": "hdr",
}


class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Add Cuboid"
    bl_options = {"INTERNAL"}

    subdivisions: bpy.props.IntProperty(
        name="Subdivisions",
        description="Number of Subdivisions",
        default=3,
        min=1,
        max=6,
    )
    shade_smooth: bpy.props.BoolProperty(
        name="Shade smooth", description="Shade smooth", default=True,
    )

    

    def execute(self, context):
        # bpy.ops.mesh.primitive_cube_add()
        # bpy.ops.object.modifier_add(type='SUBSURF')
        # bpy.context.active_object.modifiers["Subdivision"].levels = self.subdivisions
        # if self.shade_smooth:
        #     bpy.ops.object.shade_smooth()
        # self.report(
        #     {"ERROR_OUT_OF_MEMORY"},
        #     "hihhh"
        # )
        context.scene.object_color[0] = context.scene.test_float / 100
        # return {'CANCELLED'}
        return {"FINISHED"}


class VIEW3D_PT_Real_Caustics(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Casutic"
    bl_label = "Real Caustics"

    def draw(self, context):
        layout = self.layout
        coll = layout.column()
        coll1 = layout.column()
        row1 = coll.menu_pie()
        coll1.scale_y = 3
        row1.prop(context.scene, "test_float")
        row1.use_property_decorate = False
        row1.use_property_split = True
        coll1.operator("object.simple_operator", text="Update")
        row1.prop(context.scene, "object_color")
        row1.prop(context.active_object, "test_object")


blender_classes = [
    VIEW3D_PT_Real_Caustics,
    SimpleOperator,
]


def register():
    bpy.types.Scene.test_int = bpy.props.IntVectorProperty(name="Testtt",)

    bpy.types.Scene.object_color = bpy.props.FloatVectorProperty(
        name="object_color",
        subtype="COLOR",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        description="color picker",
    )
    bpy.types.Scene.test_float = bpy.props.FloatProperty(
        name="scene_float", subtype="PERCENTAGE", min=0, max=100,
    )
    bpy.types.Object.test_object = bpy.props.BoolProperty(
        name = "Object int tetst"
    )

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    del bpy.types.Scene.test_int
    del bpy.types.Scene.object_color
    del bpy.types.Scene.test_float
    del bpy.types.Object.test_object 
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)
