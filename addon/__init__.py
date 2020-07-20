import bpy
# pylint: disable=E1111
bl_info = {
    "name" : "Real Caustics",
    "author" : "Dev",
    "description" : "Generate Caustics",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "dwadwa",
    "warning" : "dwadwad",
    "category" : "Render",
    "doc_url" : "dawdwa",
    "tracker_url" : "hdr"
}

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Add Cuboid"

    subdivisions: bpy.props.IntProperty(
        name = "Subdivisions",
        description = "Number of Subdivisions",
        default = 3,
        min = 1,
        max = 6,
    )
    shade_smooth: bpy.props.BoolProperty(
        name = "Shade smooth",
        description = "Shade smooth",
        default = True,
    )
    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        # bpy.ops.mesh.primitive_cube_add()
        # bpy.ops.object.modifier_add(type='SUBSURF')
        # bpy.context.active_object.modifiers["Subdivision"].levels = self.subdivisions
        # if self.shade_smooth:
        #     bpy.ops.object.shade_smooth()
        self.report(
            {"ERROR_OUT_OF_MEMORY"},
            "hihhh"
        )
        return {'CANCELLED'}
        #return {'FINISHED'}



class VIEW3D_PT_Real_Caustics(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Casutic"
    bl_label = "Real Caustics"

    def draw(self, context):
        layout = self.layout
        coll = layout.column()
        coll.prop(context.scene, "test_int")
        coll.operator("object.simple_operator", text = "Warning")
        coll.operator("object.search_enum_operator")
        coll.operator("object.modal_operator")
        





blender_classes = [
   VIEW3D_PT_Real_Caustics,
   SimpleOperator,
]
def register():
    bpy.types.Scene.test_int = bpy.props.IntVectorProperty(
    name="Testtt", 
    )
    

    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class) 
  

def unregister():
    del bpy.types.Scene.test_int
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)