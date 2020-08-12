import bpy
import os
import ctypes as ct
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty

from timeit import default_timer as timer



script_file = os.path.realpath(__file__)
directory = os.path.dirname(script_file)
path = directory + "\\engine\\engine.dll"
engine = ct.CDLL(path)
# engine.init.argtypes = [ct.c_int, ct.c_int, ct.c_float]
# engine.array_test.argtypes = [ct.POINTER(ct.c_int)]
engine.class_test1.argtypes = []

# engine.main.restype = ct.c_int

# pylint: disable=assignment-from-no-return
# pylint: disable=no-member
# pylint: disable=unused-variable

# def my_handler(scene):
#     print(scene.collection.all_objects[0].location)

# bpy.app.handlers.frame_change_pre.append(my_handler)
# arr = ct.c_int * 10
#         array = arr()
#         for i in range(len(array)):
#             array[i] = i
#         dawi = ct.c_int(6)
#         engine.array_test(array)
# int* arr
class vec3(ct.Structure):
    _fields_ = [("x", ct.c_float),
                ("y", ct.c_float),
                ("z", ct.c_float)]



class Triangle(ct.Structure):
    _fields_ = [("mesh_index", ct.c_uint),

                ("vertex0_idx", ct.c_uint),
                ("vertex1_idx", ct.c_uint),
                ("vertex2_idx", ct.c_uint),

                ("uv_vertex0_idx", ct.c_uint),
                ("uv_vertex1_idx", ct.c_uint),
                ("uv_vertex2_idx", ct.c_uint),

                ("normal_vertex0_idx", ct.c_uint),
                ("normal_vertex1_idx", ct.c_uint),
                ("normal_vertex2_idx", ct.c_uint),

                ("material", ct.c_uint)]

engine.class_test1.argtypes = []

def update_camera_resolution(self, context):
    pass


class REAL_CAUSTICS_OT_generate_caustics(bpy.types.Operator):
    bl_idname = "real_caustics.generate_caustics"
    bl_label = "Generate Caustics"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        start = timer()
        scene = context.scene
        # arr = (ct.c_int * 10)
        # array = arr()
        # for i in range(10):
        #     array[i] = i
        # arrs = ct.POINTER(ct.c_int) * 10
        # arr_ct = arrs()
        # for i in range(10):
        #     arr_ct[i] = array 
        # for i in range(10_000_000):
        #     pass

        print(os.getcwd())
        print(bpy.data.filepath)
        all_meshes = bpy.data.meshes
        number_of_meshes = len(all_meshes) 
        #engine.class_test1(arr_ct)
        ##################################
        ###### POINTERS TO ARRAYS ########
        ##################################  
        verts_cl = ct.POINTER(vec3) * number_of_meshes
        uv_verts_cl = ct.POINTER(vec3) * number_of_meshes
        verts_normals_cl = ct.POINTER(vec3) * number_of_meshes
        tris_cl = ct.POINTER(Triangle) * number_of_meshes
        ##################################
        ########### ARRAYS ###############
        ##################################
  
        for mesh_idx in range(number_of_meshes):
            mesh = all_meshes[mesh_idx]
            verts = mesh.vertices  
            number_of_verts = len(verts)

            uv_ob = mesh.uv_layers[0]
            test = uv_ob.data
            test1 = uv_ob.data[1]
            data = uv_ob.data[0].uv
            ##################################
            ########### ARRAYS ###############
            ##################################
            vertices_cl = vec3 * number_of_verts
            vertices = vertices_cl()
                      
            for vertex_idx in range(number_of_verts):
                pos = verts[vertex_idx].co 
                vertices[vertex_idx] = vec3(pos.x, pos.y, pos.z)



        end = timer()
        print(end - start)  
        return {"FINISHED"}

class REAL_CAUSTICS_OT_test_free(bpy.types.Operator):
    bl_idname = "real_caustics.test_free"
    bl_label = "Generate Caustics"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        #engine.test_free()
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
    REAL_CAUSTICS_OT_test_free,
]


def register():

    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.caustics_settings = PointerProperty(type=CausticsSettings,
                                                        options={"HIDDEN"})


def unregister():
    del bpy.types.Scene.caustics_settings
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
