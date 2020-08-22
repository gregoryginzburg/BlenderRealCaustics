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
        #layout.label(text = scene.test_string)
        CausticsSettings = scene.caustics_settings
        col = layout.column()

        col.scale_y = 2
        col.operator("real_caustics.generate_caustics")
        col.operator("real_caustics.test_free", text="Free")
        col.operator("real_caustics.test")

        col.label(text = scene.test_string)
        col.separator(factor=0.5)
        col = layout.column()
        

        # Box - settings
        box = layout.box()
        # Settings of generation
        split = box.split()
        # Column 1
        col = split.column()
        col.alignment = "RIGHT"
        col.label(text="Resolution %")
        col.label(text="Photon count (millions)")
        col.label(text="Search Radius")
        col.label(text="Number of cache photons")

        # Settings of generation
        # Column 2
        col = split.column()
        col.alignment = "LEFT"
        col.prop(CausticsSettings, "resolution_percentage", text="")
        col.prop(CausticsSettings, "photons_count")
        col.prop(CausticsSettings, "search_radius")
        col.prop(CausticsSettings, "max_cache_photons")

        # -------------------------------------------------
        # CAUSTIC OBJECT SELECTOR
        # -------------------------------------------------

        ObjectSelector = scene.ObjectSelector
        # Label Object selector
        col = layout.column()
        col.label(text="Object Selector:")

        # Box - Object Selector
        box = layout.box()

        # Auto-select Button
        col = box.column()
        col.scale_y = 1.2
        row = col.row()
        if ObjectSelector.caustic_objects_panel_is_expanded:
            row.prop(
                ObjectSelector,
                "caustic_objects_panel_is_expanded",
                icon="TRIA_DOWN",
                icon_only=True,
                emboss=False,
            )
        else:
            row.prop(
                ObjectSelector,
                "caustic_objects_panel_is_expanded",
                icon="TRIA_RIGHT",
                icon_only=True,
                emboss=False,
            )

        row.prop(
            ObjectSelector,
            "auto_select_caustic_objects",
            text="Auto-Select Objects",
            toggle=1,
        )

        # UIList - Caustic Objects
        if ObjectSelector.caustic_objects_panel_is_expanded:
            col.separator(factor=0.5)
            col = box.column(align=True)
            row = col.row()
            row.template_list(
                "OBJECT_UL_caustic_objects",
                "",
                ObjectSelector,
                "caustic_objects",
                ObjectSelector,
                "caustic_objects_index",
                rows=2,
            )
            # Buttons: add and remove mesh from list
            col = row.column(align=True)
            col.operator("real_caustics.add_caustic_object", text="", icon="ADD")
            col.operator("real_caustics.remove_caustic_object", text="", icon="REMOVE")
            col.separator(factor=1.5)
            col.operator(
                "real_caustics.refresh_list_of_caustic_objects",
                text="",
                icon="FILE_REFRESH",
            )
            # Select mesh
            col = box.column(align=True)
            row = col.row()
            # Add objects
            row.operator(
                "real_caustics.append_selected_caustic_objects",
                text="Add Selected",
                icon="PLUS",
            )
            # Remove All Objects
            row.operator(
                "real_caustics.remove_all_caustic_objects",
                text="Remove All Objects",
                icon="CANCEL",
            )

            # Object Settings Selector
            col = box.column()

            col.label(text="Object Settings:")
            col.separator(factor=0.3)
            row = col.row()
            row.prop_search(
                ObjectSelector,
                "selected_caustic_object_name",
                ObjectSelector,
                "caustic_objects",
                text="",
                icon="MESH_DATA",
            )
            #######################################
            # --------------TO DO------------------
            #######################################
            if ObjectSelector.selected_caustic_object:
                row.prop(
                    ObjectSelector.selected_caustic_object.ObjectSettings,
                    "synchronize",
                    text="Synchronize",
                    icon="FILE_REFRESH",
                    toggle=1,
                )

            col.separator(factor=0.5)

            if ObjectSelector.selected_caustic_object:
                object_settings = ObjectSelector.selected_caustic_object.ObjectSettings
                # Object Settings
                split = col.split()
                if object_settings.synchronize:
                    split.enabled = False
                # Labels - 1 collumn
                col = split.column()
                col.label(text="Color")
                col.label(text="Roughness")
                col.label(text="Ior")
                # Props - 2 collumn
                col = split.column()
                col.prop(object_settings, "color", text="")
                col.prop(object_settings, "roughness", text="")
                col.prop(object_settings, "ior", text="")

        # -------------------------------------------------
        # CATCHER SELECTOR
        # -------------------------------------------------
        CatcherSelector = scene.CatcherSelector
        # Label Object selector
        col = layout.column()
        col.label(text="Catcher Selector:")
        # Box - Catcher Selector
        box = layout.box()
        col = box.column()
        col.scale_y = 1.2
        row = col.row()

        if CatcherSelector.catchers_panel_is_expanded:
            row.prop(
                CatcherSelector,
                "catchers_panel_is_expanded",
                icon="TRIA_DOWN",
                icon_only=True,
                emboss=False,
            )
        else:
            row.prop(
                CatcherSelector,
                "catchers_panel_is_expanded",
                icon="TRIA_RIGHT",
                icon_only=True,
                emboss=False,
            )

        row.prop(
            CatcherSelector,
            "auto_select_catchers",
            text="Auto-Select Catchers",
            toggle=1,
        )

        if CatcherSelector.catchers_panel_is_expanded:
            col.separator(factor=0.5)
            # UIList - Caustic Objects
            col = box.column(align=True)
            row = col.row()
            row.template_list(
                "OBJECT_UL_caustic_catchers",
                "",
                CatcherSelector,
                "catchers",
                CatcherSelector,
                "catchers_index",
                rows=2,
            )
            # Buttons: add and remove mesh from list
            col = row.column(align=True)
            col.operator("real_caustics.add_catcher", text="", icon="ADD")
            col.operator("real_caustics.remove_catcher", text="", icon="REMOVE")
            col.separator(factor=1.5)
            col.operator(
                "real_caustics.refresh_list_of_catchers", text="", icon="FILE_REFRESH"
            )
            # Select mesh
            col = box.column(align=True)
            row = col.row()
            # Add and remove
            row.operator(
                "real_caustics.append_selected_catchers",
                text="Add Selected",
                icon="PLUS",
            )
            row.operator(
                "real_caustics.remove_all_catchers",
                text="Remove All Objects",
                icon="CANCEL",
            )

        # -------------------------------------------------
        # LIGHT SELECTOR
        # -------------------------------------------------

        # Label Lights selector
        LightSelector = scene.LightSelector

        col = layout.column()
        col.label(text="Lights Selector:")
        # Box - Lights Selector
        box = layout.box()
        col = box.column()
        col.scale_y = 1.2
        row = col.row()

        if LightSelector.lights_panel_is_expanded:
            row.prop(
                LightSelector,
                "lights_panel_is_expanded",
                icon="TRIA_DOWN",
                icon_only=True,
                emboss=False,
            )
        else:
            row.prop(
                LightSelector,
                "lights_panel_is_expanded",
                icon="TRIA_RIGHT",
                icon_only=True,
                emboss=False,
            )

        row.prop(
            LightSelector, "auto_select_lights", text="Auto-Select Lights", toggle=1
        )

        if LightSelector.lights_panel_is_expanded:
            col.separator(factor=0.5)
            # UIList - Caustic Objects
            col = box.column(align=True)
            row = col.row()
            row.template_list(
                "OBJECT_UL_lights",
                "",
                LightSelector,
                "lights",
                LightSelector,
                "light_index",
                rows=2,
            )
            # Buttons: add and remove mesh from list
            col = row.column(align=True)
            col.operator("real_caustics.add_light", text="", icon="ADD")
            col.operator("real_caustics.remove_light", text="", icon="REMOVE")
            col.separator(factor=1.5)
            col.operator(
                "real_caustics.refresh_list_of_lights", text="", icon="FILE_REFRESH"
            )
            # Select mesh
            col = box.column(align=True)
            row = col.row()
            # Add and remove
            row.operator(
                "real_caustics.append_selected_lights", text="Add Selected", icon="PLUS"
            )
            row.operator(
                "real_caustics.remove_all_lights",
                text="Remove All Lights",
                icon="CANCEL",
            )
            # Light Settings
            col = box.column()
            col.label(text="Light Settings:")
            col.separator(factor=0.3)
            row = col.row()

            row.prop_search(
                LightSelector,
                "selected_light_name",
                LightSelector,
                "lights",
                text="",
                icon="OUTLINER_DATA_LIGHT",
            )

            col.separator(factor=0.5)
            if LightSelector.selected_light:
                lights_settings = LightSelector.selected_light.lights_settings
                # Object Settings
                split = col.split()
                # Labels - 1 collumn
                col = split.column()
                col.label(text="Color")
                col.label(text="Power")
                col.label(text="Light Type")
                # Props - 2 collumn
                col = split.column()
                col.prop(lights_settings, "color")
                col.prop(lights_settings, "power")
                col.prop(lights_settings, "light_type")

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

