from pythonosc import udp_client
from pythonosc.osc_bundle_builder import OscBundleBuilder
from pythonosc.osc_message_builder import OscMessageBuilder
from typing import List
from webcam_osc.config import CellData, OSCConfig


class OSCSender:
    _number_names = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    ]

    def __init__(self, osc_config: OSCConfig) -> None:
        self.client: udp_client.SimpleUDPClient = udp_client.SimpleUDPClient(
            osc_config.host, osc_config.port
        )

    def _num_to_name(self, n: int) -> str:
        """Converts a number (0–9) to its word representation ('zero', 'one', etc.)."""
        if 0 <= n < len(self._number_names):
            return self._number_names[n]
        return str(n)  # fallback if outside the range

    def send_grid_data(self, cells: List[CellData]) -> None:
        bundle: OscBundleBuilder = OscBundleBuilder(0)

        for cell in cells:
            row_name = self._num_to_name(cell.row)
            col_name = self._num_to_name(cell.col)
            base_address = f"/cell/{row_name}/{col_name}"

            # --- RGB components separately ---
            r_msg = OscMessageBuilder(address=f"{base_address}/r")
            r_msg.add_arg(cell.avg_red)
            bundle.add_content(r_msg.build())  # type: ignore[arg-type]

            g_msg = OscMessageBuilder(address=f"{base_address}/g")
            g_msg.add_arg(cell.avg_green)
            bundle.add_content(g_msg.build())  # type: ignore[arg-type]

            b_msg = OscMessageBuilder(address=f"{base_address}/b")
            b_msg.add_arg(cell.avg_blue)
            bundle.add_content(b_msg.build())  # type: ignore[arg-type]

            # --- Brightness ---
            brightness_msg = OscMessageBuilder(address=f"{base_address}/brightness")
            brightness_msg.add_arg(cell.brightness)
            bundle.add_content(brightness_msg.build())  # type: ignore[arg-type]

            # --- Contrast ---
            contrast_msg = OscMessageBuilder(address=f"{base_address}/contrast")
            contrast_msg.add_arg(cell.contrast)
            bundle.add_content(contrast_msg.build())  # type: ignore[arg-type]

            # --- Dominant color components separately ---
            dom_r_msg = OscMessageBuilder(address=f"{base_address}/dominant_r")
            dom_r_msg.add_arg(cell.dominant_color[0])
            bundle.add_content(dom_r_msg.build())  # type: ignore[arg-type]

            dom_g_msg = OscMessageBuilder(address=f"{base_address}/dominant_g")
            dom_g_msg.add_arg(cell.dominant_color[1])
            bundle.add_content(dom_g_msg.build())  # type: ignore[arg-type]

            dom_b_msg = OscMessageBuilder(address=f"{base_address}/dominant_b")
            dom_b_msg.add_arg(cell.dominant_color[2])
            bundle.add_content(dom_b_msg.build())  # type: ignore[arg-type]

        # Send all messages together
        self.client.send(bundle.build())
