from mocha import ui
from mocha.tools import register_custom_tool_type

from frame_jump import FrameJump
from mocha_common_tools import get_selected_layers
from set_surface_to_spline import SetSurfaceToSpline
from randomise_layer_colours import RandomiseColours
from layer_prepend import LayerPrepend
from shade_layers_by_order import ShadeMattesByOrder
from spot_cleaner import SpotCleaner
from nuke_multicorner_pin import NukeMultiCornerPin

from PySide2.QtWidgets import QMenuBar, QAction


# register our custom tool type
register_custom_tool_type(SpotCleaner)

# register our exporter
nuke_multi_exporter = NukeMultiCornerPin()
nuke_multi_exporter.register()

mocha_widget = ui.get_widgets()
main_window = mocha_widget["MainWindow"]
# grab all widgets (application is globally defined inside mocha)
widgets = application.allWidgets()


# import example script classes
def frame_jump():
    dialog = FrameJump(
        parent=main_window
    )  # Set parent so dialog doesn't sit behind Mocha window
    dialog.show()


def set_surface():
    surface = SetSurfaceToSpline()
    surface.set_surface_corners()


def random_colors():
    color = RandomiseColours()
    color.do_color()


def shade_mattes():
    color = ShadeMattesByOrder()
    color.do_shading()


def layer_label():
    dialog = LayerPrepend()


def copy_multiple_corner_pin():
    layers = get_selected_layers()
    for layer in layers:
        print(layer)


# add the scripts as actions to the menu
def add_scripts_menu():
    mocha_menubar = list(
        filter(lambda wgt: isinstance(wgt, QMenuBar), widgets)
    )[0]
    print("Adding Menu")
    scripts_menu = mocha_menubar.addMenu(
        "Scripts"
    )  # create a new Scripts menu option

    actions_dict = {
        "Frame Jump": (scripts_menu, frame_jump),
        "Surface to Spline": (scripts_menu, set_surface),
        "Randomise Matte Colors": (scripts_menu, random_colors),
        "Shade Mattes By Layer Order": (scripts_menu, shade_mattes),
        "Prepend Selected Layer Names": (scripts_menu, layer_label),
        "Copy Selected Layers Corner Pin to Clipboard (Nuke)": (
            scripts_menu,
            copy_multiple_corner_pin,
        ),
    }

    for key, value in list(actions_dict.items()):
        action = QAction(key, value[0])
        action.triggered.connect(value[1])
        value[0].addAction(action)


add_scripts_menu()
