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
        box = layout.box()
        # Settings of generation
        # Column 1
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
        col = box.column(align = True)
        row = col.row()
        row.template_list("OBJECT_UL_caustic_meshes", "caustic_meshes", scene, "caustic_meshes", 
            scene, "caustic_mesh_idx", rows = 2)
        # Buttons: add and remove mesh from list
        col = row.column(align = True)
        col.operator("real_caustics.add_mesh", text = "", icon = "ADD")
        col.operator("real_caustics.remove_mesh", text = "", icon = "REMOVE")
        col.separator(factor = 1.5)
        col.operator("real_caustics.refresh_list", text = "", icon = "FILE_REFRESH")
        # Select mesh
        col = box.column(align = True)
        row = col.row()
        row.prop(scene, "mesh_to_add", text = "")
        row.operator("real_caustics.append_selected_meshes", text = "Add Selected", icon = "PLUS")
        # Remove All Objects
        col.separator(factor = 0.8)
        col.operator("real_caustics.remove_all_objects", text = "Remove All Objects", icon = "CANCEL")
        col.separator(factor = 1.0)
        # Object Settings Selector
        col = box.column()
        col.prop_search(context.scene, "selected_object_name", scene, "caustic_meshes", text = "", icon = "MESH_DATA")
        col.separator(factor = 0.5)      
        if scene.selected_object:
            # Object Settings
            split = col.split()
            # Labels - 1 collumn
            col = split.column()
            col.label(text = "Color")
            col.label(text = "Roughness")
            col.label(text = "Ior")
            # Props - 2 collumn
            col = split.column()
            col.prop(scene.selected_object.object_settings, "color")
            col.prop(scene.selected_object.object_settings, "roughness")
            col.prop(scene.selected_object.object_settings, "ior")

        # Box - Catcher Selector
        box = layout.box()
        


        

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

