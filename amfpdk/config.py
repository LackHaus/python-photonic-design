"""Store configuration for AMF pdk module."""

__all__ = ["PATH"]

import pathlib

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
cwd_config = cwd / "config.yml"

home_config = home / ".config" / "amfpdk.yml"
config_dir = home / ".config"
config_dir.mkdir(exist_ok=True)
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent


class Path:
    module = module_path
    repo = repo_path
    gds_amf_bb = module_path / "gds" / "amf_bb"
    gds_siepiclib = module_path / "gds" / "siepic_lib"
    lyp = module_path / "klayout" / "tech" / "klayout_Layers_AMF.lyp"
    lyt = module_path / "klayout" / "tech" / "AMF.lyt"
    tech = module_path / "klayout" / "tech"
    layer_yaml = module_path / "layers.yaml"


PATH = Path()

if __name__ == "__main__":
    print(PATH)
