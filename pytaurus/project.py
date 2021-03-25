from typing import List, Optional
import subprocess


class Project:
    def __init__(self, path: str):
        self.path = path
        self.custom_env = None


    def run(self, nodes: Optional[List[int]] = None, display_output: bool = False):
        cmd = self.get_gsub_cmd(nodes)
        return self.execute_cmd(cmd, display_output)

    def clean(self, nodes: Optional[List[int]] = None, renumbers_nodes: bool = False, display_output: bool = False):
        cmd = self.get_gcleanup_cmd(nodes, renumbers_nodes)
        return self.execute_cmd(cmd, display_output)

    def get_gsub_cmd(self, nodes: Optional[List[int]] = None):
        arguments = f'-n {self.get_nodes(nodes)}' if nodes else '-e all'
        return f'gsub {arguments} {self.path}'

    def get_gcleanup_cmd(self, nodes: Optional[List[int]] = None, renumbers_nodes: bool = False):
        if renumbers_nodes:
            return f'gcleanup -ren {self.path}'
        arguments = f'-n {self.get_nodes(nodes)} ' if nodes else ''
        return f'gsub {arguments} {self.path}'

    @staticmethod
    def execute_cmd(cmd: str, display_output: bool = False, custom_environment: Optional[dict] = None):
        stdout = None if display_output else subprocess.DEVNULL
        return subprocess.call([cmd], shell=True, stdout=stdout, env=custom_environment)

    @staticmethod
    def get_nodes(nodes: List[int]) -> str:
        return ' '.join(map(str, nodes))

    def set_environment(self, tcad_path, scl_path, license_path, stdb_path):
        custom_env = os.environ.copy()
        custom_env["PATH"] = tcad_path + ":" + custom_env["PATH"]
        custom_env["PATH"] = scl_path + ":" + custom_env["PATH"]
        custom_env["STDB"] = stdb_path
        custom_env["LM_LICENSE_FILE"] = license_path
        custom_env["SNPSLMD_LICENSE_FILE"] = license_path
        self.custom_env = custom_env
