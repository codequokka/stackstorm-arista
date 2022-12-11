import json

import requests
import urllib3
from st2actions.runners.pythonrunner import Action
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)


class ExecuteCommandsAction(Action):
    def run(self, hostname, port, user, password, format, commands):
        """
        Parameters
        ----------
        hostname : str
            A host name to execute commands
        port : int
            A port number for eAPI access
        user : str
            A user name for eAPI access
        password : str
            A password for eAPI access
        format : str
            A format for returning result
        commands : list[str]
            The Commands are executed

        Returns
        -------
        tuple[bool, list]
            Boolean for successful execution or not
            List for execution result
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
            return True, response["result"]
        else:
            return True, response
