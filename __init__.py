import bpy
from . import ui
from . import generation

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


def register():
    ui.register()
    generation.register()
    
    


def unregister():
    ui.unregister()
    generation.unregister()
    
    
