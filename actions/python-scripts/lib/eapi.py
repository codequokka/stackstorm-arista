from __future__ import annotations

import json
import sys
from typing import Any

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


def execute_commands(
    hostname: str,
    port: int,
    user: str,
    password: str,
    format: str,
    commands: list[str],
) -> list[dict[str, str | Any]]:  # TODO: Use TypedDict
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
    commands : list[str]
        Commands to be executed on the host

    Returns
    -------
    list[dict[str, str | Any]]
        List for results of executed commands
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

    if "error" not in response.keys():
        return response["result"]
    else:
        print(response, file=sys.stderr)
        raise Exception("Commands execution failed")
