import os
import subprocess
from typing import List
from typing import Optional


class Project:
    def __init__(
            self,
            path: str,
            environment: Optional[dict] = None,
    ) -> None:
        self._path = path
        self._custom_environment = environment

    def gsub(
            self,
            nodes: Optional[List[int]] = None,
            display_output: bool = False,
            verbose: bool = False,
            environment: Optional[dict] = None,
    ) -> int:
        cmd = self.get_gsub_cmd(nodes, verbose)
        return self._execute_cmd(cmd, display_output, environment)

    def run(
            self,
            nodes: Optional[List[int]] = None,
            display_output: bool = False,
            verbose: bool = False,
            environment: Optional[dict] = None,
    ) -> int:
        return self.gsub(nodes, display_output, verbose, environment)

    def gcleanup(
            self,
            nodes: Optional[List[int]] = None,
            renumbers_nodes: bool = False,
            display_output: bool = False,
            verbose: bool = False,
            environment: Optional[dict] = None,
    ) -> int:
        cmd = self.get_gcleanup_cmd(nodes, renumbers_nodes, verbose)
        return self._execute_cmd(cmd, display_output, environment)

    def clean(
            self,
            nodes: Optional[List[int]] = None,
            renumbers_nodes: bool = False,
            display_output: bool = False,
            verbose: bool = False,
            environment: Optional[dict] = None,
    ) -> int:
        return self.gcleanup(nodes, renumbers_nodes, display_output, verbose, environment)

    def get_gcleanup_cmd(
            self,
            nodes: Optional[List[int]] = None,
            renumbers_nodes: bool = False,
            verbose: bool = False,
    ) -> str:
        verbose_str = ' -verbose' if verbose else ''
        if renumbers_nodes:
            return f'gcleanup -ren {self._path} {verbose_str}'
        scope = f'-n {self._get_nodes(nodes)} ' if nodes else ''
        command = ' '.join(['gcleanup', scope, verbose_str, self._path])
        return command

    def get_gsub_cmd(
            self,
            nodes: Optional[List[int]] = None,
            verbose: bool = False,
    ) -> str:
        scope = f'-n {self._get_nodes(nodes)}' if nodes else '-e all'
        verbose_str = ' -verbose' if verbose else ''
        command = ' '.join(['gsub', scope, verbose_str, self._path])
        return command

    def _execute_cmd(
            self,
            cmd: str,
            display_output: bool = False,
            custom_environment: Optional[dict] = None,
    ) -> int:
        custom_environment = custom_environment if custom_environment is not None else self._custom_environment
        stdout = None if display_output else subprocess.DEVNULL
        return subprocess.call([cmd], shell=True, stdout=stdout, env=custom_environment)

    @staticmethod
    def _get_nodes(nodes: List[int]) -> str:
        return ' '.join(map(str, nodes))

    def set_environment(
            self,
            tcad_path: str,
            scl_path: str,
            license_path: str,
            stdb_path: str,
    ) -> None:
        env = os.environ.copy()
        env['PATH'] = tcad_path + ':' + env['PATH']
        env['PATH'] = scl_path + ':' + env['PATH']
        env['STDB'] = stdb_path
        env['LM_LICENSE_FILE'] = license_path
        env['SNPSLMD_LICENSE_FILE'] = license_path
        self._custom_environment = env
