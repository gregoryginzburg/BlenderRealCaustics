import bpy
import os
import sys
import ctypes as ct
from bpy.props import IntProperty, BoolProperty, FloatProperty, PointerProperty
import multiprocessing
from timeit import default_timer as timer
directory = __file__.split("\\generation\\generation.py")[0]
path = directory + "\\engine\\Real Caustics.dll"
engine = ct.CDLL(path)
path2 = directory + "\\engine\\Project2.dll"


# pylint: disable=assignment-from-no-return
# pylint: disable=no-member
# pylint: disable=unused-variable
def print_m(m):
    print(m[0][0], " ", m[0][1], " ", m[0][2], " ", m[0][3])
    print(m[1][0], " ", m[1][1], " ", m[1][2], " ", m[1][3])
    print(m[2][0], " ", m[2][1], " ", m[2][2], " ", m[2][3])
    print(m[3][0], " ", m[3][1], " ", m[3][2], " ", m[3][3])
                

class vec3(ct.Structure):
    _fields_ = [("x", ct.c_float), ("y", ct.c_float), ("z", ct.c_float)]

class vec4(ct.Structure):
    _fields_ = [("x", ct.c_float), ("y", ct.c_float), ("z", ct.c_float), ("w", ct.c_float)]

class colorf(ct.Structure):
    _fields_ = [("r", ct.c_float), ("g", ct.c_float), ("b", ct.c_float)]

class matrix_4x4(ct.Structure):
    _fields_ = [("i", vec4), ("j", vec4), ("k", vec4), ("w", vec4)]
test1 = ct.CDLL(path2)
test1.test.argtypes = (ct.c_longlong, ct.c_int, ct.c_int, vec3, ct.c_float, ct.c_float, ct.POINTER(ct.c_char))
# :rotation - in degrees
class Python_Light(ct.Structure):
    _fields_ = [("type", ct.c_char),
                ("position", vec3),
                ("width", ct.c_float),
                ("height", ct.c_float),
                ("rotation", vec3),
                ("power", ct.c_float),
                ("angle", ct.c_float)]

class Python_Material(ct.Structure):
    _fields_ = [("type", ct.c_char),
                ("ior", ct.c_float),
                ("color", colorf)]

# :number_of_photons - number of emitted photons
# :n_closest - maximum number of photons used for gathering
# :radius - maximum gather radius
# :mesh_pointers - array of pointers to blender meshes
# :number_of_meshes
# :meshes_number_of_verts - array of number of vertices
# :meshes_number_of_tris - array of number of triangles 
# :camera_x - camera width resolution
# :camera_y - camera height resolution  
# :camera_position
# :camera_corner 0,1,2,3 - top right, boottom right, bottom left, top left corners of camera
#  4----1
#	|    |  - Camera corners
#  |    |
#  3----2
# :lights - Lights from Python, need to be converted
# :number_of_lights
# :materials - Materials from Python, need to be converted 
# :number_of_materials
# :meshes_material_idx - Array with length of number_of_meshes, indices of materials
engine.init.argtypes = [ct.c_int, ct.c_int, ct.c_float,
                        ct.POINTER(ct.c_longlong),
                        ct.c_uint,
                        ct.POINTER(matrix_4x4),
                        ct.POINTER(ct.c_uint),
                        ct.POINTER(ct.c_uint),
                        ct.c_uint,
                        ct.c_uint,
                        vec3,
                        vec3,
                        vec3,
                        vec3,
                        vec3,
                        ct.POINTER(Python_Light),
                        ct.c_uint,
                        ct.POINTER(Python_Material),
                        ct.c_uint,
                        ct.POINTER(ct.c_int),
                        ct.POINTER(ct.c_char)]









def thread_func(self, context):
    engine.main()


# def reporting(self):
#     global test_fl
#     from time import sleep
#     while not exit_pr:  
#         sleep(0.001)    
#         self.report({'INFO'}, str(test_fl).split("c_float")[1])
#     self.report({'INFO'}, "FINISHED")

def update_camera_resolution(self, context):
    pass




class REAL_CAUSTICS_OT_generate_caustics(bpy.types.Operator):
    bl_idname = "real_caustics.generate_caustics"
    bl_label = "Generate Caustics"
    bl_options = {"INTERNAL"}


    
    def invoke(self, context, event):
        context.scene.test_finished = False

        from threading import Thread
        self.thread = Thread(target=thread_func, args=(self, context))
        self.thread.start()

        self.finihed = False    
        wm = context.window_manager
        wm.modal_handler_add(self)
    
        return {'RUNNING_MODAL'}


    def modal(self, context, event):
        scene = context.scene
        collection = scene.collection
        collections = collection.children
        objects = collection.objects
        if self.finihed:
            #self.process.terminate()
            self.thread.join()
            for coll in collections:
                coll.hide_select = False
            for ob in objects:
                ob.hide_select = False
            return {'CANCELLED'}

        
        for coll in collections:
            coll.hide_select = True
        for ob in objects:
            ob.hide_select = True
               
        return {'PASS_THROUGH'}


class REAL_CAUSTICS_OT_test_free(bpy.types.Operator):
    bl_idname = "real_caustics.test_free"
    bl_label = "Generate Caustics"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        #engine.test_free()
        # engine.init_exit(True)
        # global exit_pr
        # exit_pr = True  
        # start = timer()
        # scene = context.scene
        # obj = context.active_object
        # dg = bpy.context.evaluated_depsgraph_get()
        # eval_obj = obj.evaluated_get(dg)
        # mesh = eval_obj.data

        # mesh_ptr = mesh.as_pointer()
        # engine.test(mesh_ptr, len(mesh.vertices), len(mesh.polygons))

        # mesh.update()
        # end = timer()
        # print(end - start)
        scene = context.scene
        caustic_set = scene.caustics_settings
        CatcherSelector = scene.CatcherSelector
        ObjectSelector = scene.ObjectSelector
        # :number_of_photons, :n_closest, :radius
        number_of_photons = ct.c_int(int(caustic_set.photons_count * 1_000_000))
        n_closest = caustic_set.max_cache_photons
        radius = caustic_set.search_radius
        # :number_of_meshes
        number_of_meshes = len(CatcherSelector.catchers) + len(ObjectSelector.caustic_objects)  
        mesh_pointers_cl = ct.c_longlong * number_of_meshes
        number_of_verts_tris_cl = ct.c_uint * number_of_meshes
        # :mesh_pointers 
        mesh_pointers = mesh_pointers_cl()
        # :mesh_matrices
        mesh_matrices_cl = matrix_4x4 * number_of_meshes
        mesh_matrices = mesh_matrices_cl()
        # :meshes_number_of_verts
        meshes_number_of_verts = number_of_verts_tris_cl()
        # :meshes_number_of_tris
        meshes_number_of_tris = number_of_verts_tris_cl()
        # :camera_x, :camera_y
        camera_x = scene.render.resolution_x
        camera_y = scene.render.resolution_y
        # :camera position
        camera_ob = scene.camera
        camera = camera_ob.data

        camera_position = vec3(camera_ob.location.x, camera_ob.location.y, camera_ob.location.z)

        # :camera_corner 0,1,2,3

        frame = camera.view_frame(scene = scene)
        frame = [camera_ob.matrix_world @ corner for corner in frame]

        camera_corner0 = vec3(frame[0].x, frame[0].y, frame[0].z)
        camera_corner1 = vec3(frame[1].x, frame[1].y, frame[1].z)
        camera_corner2 = vec3(frame[2].x, frame[2].y, frame[2].z)
        camera_corner3 = vec3(frame[3].x, frame[3].y, frame[3].z)


        # :number_of_lights
        LightSelector = scene.LightSelector
        number_of_lights = len(LightSelector.lights)

        # :lights
        lights_cl = Python_Light * number_of_lights
        lights = lights_cl()

        # :number_of_materials
        number_of_obs = len(ObjectSelector.caustic_objects)
        number_of_materials = 1 + number_of_obs 
        # :materials 
        materials_cl = Python_Material * number_of_materials
        materials = materials_cl()
        # :meshes_material_idx

        meshes_material_idx_cl = ct.c_int32 * number_of_meshes
        meshes_material_idx =  meshes_material_idx_cl()



        number_of_catchers = len(CatcherSelector.catchers)
        # 67 - C
        materials[0] = Python_Material(67, 0.0, colorf(0.0, 0.0, 0.0))


        depsgraph = context.evaluated_depsgraph_get()

        for i, catcher_ob in enumerate(CatcherSelector.catchers):
            ob = catcher_ob.catcher
            #print(ob.matrix_world)
            ob = ob.evaluated_get(depsgraph)
            mesh_pointers[i] = ob.data.as_pointer()
            m = ob.matrix_world

            mesh_matrices[i] = matrix_4x4(vec4(m[0][0], m[1][0], m[2][0], m[3][0]),
                                          vec4(m[0][1], m[1][1], m[2][1], m[3][1]),
                                          vec4(m[0][2], m[1][2], m[2][2], m[3][2]),
                                          vec4(m[0][3], m[1][3], m[2][3], m[3][3]))
            meshes_number_of_verts[i] = len(ob.data.vertices)
            meshes_number_of_tris[i] = len(ob.data.polygons)
            meshes_material_idx[i] = 0 

            
        material_idx = 1
        for i, caustic_ob in enumerate(ObjectSelector.caustic_objects, number_of_catchers):
            ob = caustic_ob.caustic_object
            #print(ob.matrix_world)
            ob = ob.evaluated_get(depsgraph)
            mesh_pointers[i] = ob.data.as_pointer()
            m = ob.matrix_world

            mesh_matrices[i] = matrix_4x4(vec4(m[0][0], m[1][0], m[2][0], m[3][0]),
                                          vec4(m[0][1], m[1][1], m[2][1], m[3][1]),
                                          vec4(m[0][2], m[1][2], m[2][2], m[3][2]),
                                          vec4(m[0][3], m[1][3], m[2][3], m[3][3]))
            meshes_number_of_verts[i] = len(ob.data.vertices)
            meshes_number_of_tris[i] = len(ob.data.polygons)
            ObjectSettings = ob.ObjectSettings
            color = colorf(ObjectSettings.color.r,
                           ObjectSettings.color.g,
                           ObjectSettings.color.b)
            # 71 - G
            materials[material_idx] = Python_Material(71, ObjectSettings.ior, color)
            meshes_material_idx[i] = material_idx

            material_idx += 1

        for i, light_ob in enumerate(LightSelector.lights):
            ob = light_ob.light
            # 83 - S
            lights[i].type = 83
            pos = vec3(ob.location.x, ob.location.y, ob.location.z)
            rot = vec3(ob.rotation_euler.x, ob.rotation_euler.y, ob.rotation_euler.z)

            lights[i].position = pos
            lights[i].rotation = rot
            lights[i].power = 38

        engine.init(number_of_photons, n_closest, radius,
                    mesh_pointers,
                    number_of_meshes,
                    mesh_matrices,
                    meshes_number_of_verts,
                    meshes_number_of_tris,
                    camera_x,
                    camera_y,
                    camera_position,
                    camera_corner0,
                    camera_corner1,
                    camera_corner2,
                    camera_corner3,
                    lights,
                    number_of_lights,
                    materials,
                    number_of_materials,
                    meshes_material_idx,
                    "caustic_set.hdri_path".encode('utf-8'))
        engine.main()
        return {"FINISHED"}





class REAL_CAUSTICS_OT_test(bpy.types.Operator):
    bl_idname = "real_caustics.test"
    bl_label = "Test"
    bl_options = {"INTERNAL"}


    
    def execute(self, context):
        ob = context.active_object

        depsgraph = context.evaluated_depsgraph_get()
        object_eval = ob.evaluated_get(depsgraph)
        mesh_eval = object_eval.data

        mesh = ob.data
        mesh_ptr = mesh.as_pointer()
        verts = len(mesh.vertices)
        dir_view = bpy.data.objects["Empty"].location
        vector = vec3(dir_view.x, dir_view.y, dir_view.z)
        #text = ct.c_wchar_p("Hi from c++")
        #text = ct.cast(ct.POINTER(ct.c_char), text)
        test1.test(mesh_ptr, verts, 0, vector, context.scene.caustics_settings.search_radius, context.scene.caustics_settings.photons_count,
        context.scene.caustics_settings.hdri_path.encode('utf-8')) 
        print("\n")
        mesh = context.active_object.data
        mesh.update()
        return {'FINISHED'}
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
        min=0.000001,
        soft_max=100.0,
        step=10,
        precision=2,
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
    hdri_path: bpy.props.StringProperty(
        subtype = 'FILE_PATH',
    )


classes = [
    REAL_CAUSTICS_OT_generate_caustics,
    CausticsSettings,
    REAL_CAUSTICS_OT_test_free,
    REAL_CAUSTICS_OT_test,
]


def register():

    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    bpy.types.Scene.caustics_settings = PointerProperty(type=CausticsSettings,
                                                        options={"HIDDEN"})
    bpy.types.Scene.test_finished = BoolProperty()
    bpy.types.Scene.test_string = bpy.props.StringProperty()

def unregister():
    del bpy.types.Scene.caustics_settings
    del bpy.types.Scene.test_finished
    del bpy.types.Scene.test_string  
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)
