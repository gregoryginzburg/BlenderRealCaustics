from . import catcher_selector
from . import light_selector
from . import select_objects

def register():
    light_selector.register()
    select_objects.register()
    catcher_selector.register()


def unregister():
    light_selector.unregister()
    select_objects.unregister()
    catcher_selector.unregister()