"""write xsection script for KLayout plugin.

https://gdsfactory.github.io/klayout_pyxs/DocGrow.html

TODO
"""

from __future__ import annotations

import pathlib

from gdsfactory.typings import LayerMap

from amfpdk.layer_map import LAYER
from amfpdk.layer_stack import LayerStackParameters

nm = 1e-3


def layer_to_string(layer: tuple[int, int]) -> str:
    return f"{layer[0]}/{layer[1]}"


def get_klayout_pyxs(lsp: LayerStackParameters, lm: LayerMap) -> str:
    """Returns klayout_pyxs plugin script to show chip cross-section in klayout.

    https://gdsfactory.github.io/klayout_pyxs/DocGrow.html

    """
    return """
    """


if __name__ == "__main__":
    script = get_klayout_pyxs(LayerStackParameters(), LAYER)
    script_path = pathlib.Path(__file__).parent.absolute() / "cross_section.pyxs"
    script_path.write_text(script)
