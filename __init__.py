import bpy
from . import generation
from . import selectors
from . import ui

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
    selectors.register()
    ui.register()
    generation.register()

def unregister():
    selectors.unregister()
    ui.unregister()
    generation.unregister()
