import bpy
from . import ui
from . import generation
from . import select_objects
from . import catcher_selector
from . import light_selector

# pylint: disable=E1111
bl_info = {
    "name": "Real Caustics",
    "author": "Dev",
    "description": "Generate Caustics",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "dwadwa",
    "category": "Render",
    "doc_url": "dawdwa",
    "tracker_url": "hdr",
}


def register():
    light_selector.register()
    ui.register()
    generation.register()
    select_objects.register()
    catcher_selector.register()


def unregister():
    ui.unregister()
    generation.unregister()
    select_objects.unregister()
    catcher_selector.unregister()
    light_selector.unregister()
