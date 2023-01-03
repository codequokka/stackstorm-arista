from __future__ import annotations

import json
from typing import Any

import requests
import urllib3
from st2actions.runners.pythonrunner import Action  # type: ignore
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


class ExecuteCommandsAction(Action):  # type: ignore
    def run(
        self,
        hostname: str,
        port: int,
        user: str,
        password: str,
        format: str,
        commands: list[str],
    ) -> tuple[bool, list[dict[str, Any] | str]]:  # TODO: Use TypedDict
        """
        Execute any commands via eAPI

        Parameters
        ----------
        hostname : str
            A hostname where commands are executed
        port : int
            A port number to access eAPI
        user : str
            An user name to access eAPI
        password : str
            A password to access eAPI
        format : str
            A format in returing result
        commands : tuple[bool, list[dict[str, Any] | str]]
            Commands to be executed on the host

        Returns
        -------
        tuple[bool, dict[str, Any]]
            Boolean for successful execution or not,
            Dict for results of executed commands
        """
        url = "https://{}:{}@{}:{}/command-api".format(
            user, password, hostname, port
        )
        headers = {"content-type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "method": "runCmds",
            "params": {
                "version": 1,
                "cmds": commands,
                "format": format,
                "timestamps": False,
                "autoComplete": False,
                "expandAliases": False,
                "stopOnError": True,
                "streaming": False,
                "includeErrorDetail": False,
            },
            "id": "EapiExplorer-1",
        }

        response = requests.post(
            url, data=json.dumps(payload), headers=headers, verify=False
        ).json()

        # If commands execution failed, "error" key is present in the response
        if "error" not in response.keys():
            return True, response["result"]
        else:
            return False, response
