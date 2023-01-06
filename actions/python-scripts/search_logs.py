from __future__ import annotations

import datetime
import re

from lib.datetime import get_current_datetime, parse_datetime
from lib.eapi import execute_commands
from lib.typeddicts import StructuredLog
from st2actions.runners.pythonrunner import Action  # type: ignore


class SearchLogsAction(Action):  # type: ignore
    def __parse_logs(self, logs: str, fqdn: str) -> list[StructuredLog]:
        """
        Parse a show logging result and return structured logs

        Parameters
        ----------
        logs : str
            A Result of show logging
        fqdn : str
            A fqdn of the target device
            (used as a delimiter for splitting one log line)

        Returns
        -------
        list[StructuredLog]
            A list of structured log dictionaries
            - datetime: '2022-12-11T23:45:13+09:00'
              fqdn: cEOS-1
              message: 'Stp: %SPANTREE-6-STABLE_CHANGE:
                        Stp state is now not stable'
        """
        parsed_logs: list[StructuredLog] = []

        for result in logs.splitlines():
            if fqdn in result:
                datetime_str, message = result.split(fqdn)

                datetime_str = datetime_str.rstrip()
                message = message.lstrip()

                datetime = parse_datetime(datetime_str, "%b %d %H:%M:%S")

                parsed_logs.append(
                    {
                        "datetime": datetime,
                        "fqdn": fqdn,
                        "message": message,
                    }
                )

        return parsed_logs

    def __filter_logs(
        self,
        structured_logs: list[StructuredLog],
        filter_pattern: str,
        filter_start_datetime_str: str | None,
        filter_end_datetime_str: str | None,
    ) -> list[StructuredLog]:
        """
        Return logs matching the string and datetime from the structured logs

        Parameters
        ----------
        structured_logs : list[StructuredLog]
            A list of Structured log dictionaries
        filter_pattern : str
            A regex pattern to filter logs
        filter_start_datetime: str | None
            description: Start datetime to filter logs
            (10 mins before current datetime if not specified)
        filter_end_datetime: str | None
            End datetime to filter logs
            (10 mins after start datetime if not specified)

        Returns
        -------
        list[StructuredLog]
            A list of matched structured log dictionaries
            - datetime: '2022-12-11T23:45:13+09:00'
              fqdn: cEOS-1
              message: 'Ebra: %LINEPROTO-5-UPDOWN: Line protocol on
                        Interface Ethernet1, changed state to up'
        """
        filtered_logs = list(
            filter(
                lambda log: re.search(filter_pattern, log["message"]),
                structured_logs,
            )
        )

        if filter_start_datetime_str:
            filter_start_datetime = parse_datetime(
                filter_start_datetime_str, "%Y/%m/%d %H:%M:%S %z"
            )
        else:
            filter_start_datetime = (
                get_current_datetime() - datetime.timedelta(minutes=10)
            )

        if filter_end_datetime_str:
            filter_end_datetime = parse_datetime(
                filter_end_datetime_str, "%Y/%m/%d %H:%M:%S %z"
            )
        else:
            filter_end_datetime = filter_start_datetime + datetime.timedelta(
                minutes=10
            )

        filtered_logs = list(
            filter(
                lambda log: filter_start_datetime <= log["datetime"]
                and filter_end_datetime >= log["datetime"],
                filtered_logs,
            )
        )

        return filtered_logs

    def __change_log_format(self, structured_logs: list[StructuredLog]) -> str:
        """
        Convert a list of structured logs
        to a newline-delimited logs strings and return

        Parameters
        ----------
        structured_logs : list[StructuredLog]
            A list of Structured log dictionaries

        Returns
        -------
        str
            a newline-delimited logs strings
            '2022-12-08 01:29:59+09:19 cEOS-1 Ebra: %LINEPROTO-5-UPDOWN:
             Line protocol on Interface Ethernet1, changed state to down'
        """
        string_logs = "\n".join(
            [" ".join(map(str, log.values())) for log in structured_logs]
        )

        return string_logs

    def run(
        self,
        hostname: str,
        port: int,
        user: str,
        password: str,
        format: str,
        filter_pattern: str,
        filter_start_datetime: str | None = None,
        filter_end_datetime: str | None = None,
    ) -> tuple[bool, list[StructuredLog] | str]:
        """
        Parameters
        ----------
        hostname : str
            A hostname where logs are searched
        port : int
            A port number to access eAPI
        user : str
            An user name to access eAPI
        password : str
            A password to access eAPI
        format: str
            A format in returning logs
        filter_pattern : str
            A regex pattern to filter logs
        filter_start_datetime: Union[str, None]
            Start datetime to filter logs
            (10 mins before current datetime if not specified)
            2022/12/19 00:00:00 +0900
        filter_end_datetime: Union[str, None]
            End datetime to filter logs
            (10 mins after start datetime if not specified)
            2022/12/19 00:10:00 +0900

        Returns
        -------
        tuple[bool, list[StructuredLog] | str]
            Boolean for successful search or not,
            Dict or String for results of searched logs
        """
        logs = execute_commands(
            hostname, port, user, password, "text", ["show logging"]
        )[0]["output"]

        fqdn = execute_commands(
            hostname, port, user, password, "json", ["show hostname"]
        )[0]["fqdn"]

        parsed_logs = self.__parse_logs(logs, fqdn)

        filtered_logs = self.__filter_logs(
            parsed_logs,
            filter_pattern,
            filter_start_datetime,
            filter_end_datetime,
        )

        searched_logs: list[StructuredLog] | str
        if format == "string":
            searched_logs = self.__change_log_format(filtered_logs)
        else:
            searched_logs = filtered_logs

        return True, searched_logs
