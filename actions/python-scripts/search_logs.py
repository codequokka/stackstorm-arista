import datetime

from lib.execute_commands import execute_commands
from lib.parse_datetime import get_current_datetime, parse_datetime
from st2actions.runners.pythonrunner import Action


class SearchLogsAction(Action):
    def __init__(self, config):
        self.config = config

    def __parse_log(self, results, fqdn):
        parsed_logs = []

        for result in results.splitlines():
            if fqdn in result:
                datetime, message = result.split(fqdn)

                datetime = datetime.rstrip()
                message = message.lstrip()

                datetime = parse_datetime(datetime)

                parsed_logs.append(
                    {"datetime": datetime, "fqdn": fqdn, "message": message}
                )

        return parsed_logs

    def __filter_log(self, parsed_logs, pattern):
        filtered_logs = list(
            filter(lambda log: pattern in log["message"], parsed_logs)
        )

        current_datetime = get_current_datetime()
        target_datetime = current_datetime - datetime.timedelta(days=1)
        filtered_logs = list(
            filter(
                lambda log: target_datetime <= log["datetime"], filtered_logs
            )
        )

        return filtered_logs

    def run(self, hostname, port, user, password, pattern):
        """
        Parameters
        ----------
        hostname : str
            A host name to execute commands
        port : iromt
            A port number for eAPI access
        user : str
            A user name for eAPI access
        password : str
            A password for eAPI access
        format : str
            A format for returning result
        commands : list[str]
            The Commands are executed
        pattern : str
            A string to filter logs

        Returns
        -------
        list[dict]
            Boolean for successful execution or not
            List for execution result
        """
        results = execute_commands(
            hostname, port, user, password, "text", ["show logging"]
        )[0]["output"]

        fqdn = execute_commands(
            hostname, port, user, password, "json", ["show hostname"]
        )[0]["fqdn"]

        parsed_logs = self.__parse_log(results, fqdn)

        filtered_logs = self.__filter_log(parsed_logs, pattern)

        return True, filtered_logs
