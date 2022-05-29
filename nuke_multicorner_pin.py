from mocha.exporters import AbstractTrackingDataExporter
from mocha_common_tools import get_selected_layers
from PySide2.QtCore import QByteArray


class NukeMultiCornerPin(AbstractTrackingDataExporter):
    def __init__(self):
        super(NukeMultiCornerPin, self).__init__(
            "Nuke MultiCorner Pin (*.nk)", "", number_of_data_streams=1
        )
        self.nuke_exporter = (
            AbstractTrackingDataExporter.registered_exporters()[
                "Nuke Corner Pin (*.nk)"
            ]
        )

    def error_string(self):
        return ""

    def do_export(
        self, project, layer, tracking_file_path, time, view, options
    ):

        layers = get_selected_layers()
        output = QByteArray()
        for lay in layers:
            # name = lay.get_name()
            result = self.nuke_exporter.do_export(
                project, lay, tracking_file_path, time, view, options
            )
            output.append(list(result.values())[0])

        if not tracking_file_path:
            tracking_file_path = "NONE"
        else:
          if not tracking_file_path.lower().endswith(".nk"):
            tracking_file_path += ".nk"
        return {
            tracking_file_path: output
        }
