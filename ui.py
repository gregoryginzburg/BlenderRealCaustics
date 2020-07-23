import bpy


class VIEW3D_PT_real_caustics(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Casutic"
    bl_label = "Real Caustics"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # Generate Button
        col = layout.column()
        
        col.scale_y = 2
        col.operator("real_caustics.generate_caustics")
        col.separator(factor = 0.5)
        col = layout.column()
        # Label - settings
        col.label(text = "Settings:")

        # Box - settings
        # Settings of generation
        # Column 1
        box = layout.box()
        col = box.column()
        split = box.split()
        col = split.column(align = True)
        col.alignment = 'RIGHT'
        col.label(text = "Resolution X")
        col.label(text = "Y")

        # Settings of generation
        # Column 2
        col = split.column(align = True)
        col.alignment = 'LEFT'
        col.prop(scene.caustics_settings, "resolution_x")
        col.prop(scene.caustics_settings, "resolution_y")

        # Checkbox with text to the right
        col = box.column()
        row = col.row()
        row.alignment = 'RIGHT'
        row.label(text = "Synchronize with camera")
        row.prop(scene.caustics_settings, "synchronize_with_camera")
        
        # Settings of generation (photons count and search radius) - continiued
        # Collumn 1
        col = box.column(align = True)
        split = box.split()
        col = split.column()
        col.alignment = 'RIGHT'
        col.label(text = "Photon count (millions)")
        col.label(text = "Search Radius")

        # Column 2
        col = split.column()
        col.prop(scene.caustics_settings, "photons_count")
        col.prop(scene.caustics_settings, "search_radius")
        # Label Object selector
        col = layout.column()
        col.label(text = "Object Selector:")

        # Box - Object Selector
        box = layout.box()

        # Auto-select Button
        col = box.column()
        col.scale_y = 1.2
        col.operator("real_caustics.auto_select_objects")
        col.separator(factor = 0.5)
        # UIList - Caustic Objects
        row = box.row()
        row.template_list("OBJECT_UL_caustic_meshes", "caustic_meshes", scene, "caustic_meshes", 
            scene, "caustic_mesh_idx", rows = 2)
        # Buttons: add and remove mesh from list
        col = row.column(align = True)
        col.operator("real_caustics.add_mesh", text = "", icon = "ADD")
        col.operator("real_caustics.remove_mesh", text = "", icon = "REMOVE")
        # Select mesh
        col = box.column()
        col.prop(scene, "mesh_to_add", text = "")

        

        # UIList with objects

        

        

classes = [
    VIEW3D_PT_real_caustics,
    ]


def register():
    for blender_class in classes:
        bpy.utils.register_class(blender_class)
    


def unregister():
    for blender_class in classes:
        bpy.utils.unregister_class(blender_class)

