from __future__ import annotations

import telnetlib

from st2actions.runners.pythonrunner import Action  # type: ignore


class CheckLoginAction(Action):  # type: ignore
    def run(
        self, hostname: str, port: int, user: str, password: str
    ) -> tuple[bool, str]:
        """
        Check login by using telnet

        Parameters
        ----------
        hostname : str
            A host name to log in to
        port : int
            A telnet port number to log in to
        user : str
            A user name to log in to
        password : str
            A password for user to log in to

        Returns
        -------
        tuple[bool, str]
            Boolean, Message for successful login or not
        """
        with telnetlib.Telnet(hostname, port) as tn:
            # Try to login
            tn.read_until(b"Username:")
            tn.write(user.encode("ascii") + b"\n")
            tn.read_until(b"Password:")
            tn.write(password.encode("ascii") + b"\n")

            # Check login has succeeded
            # succeeded:
            #   - 1: When ">" appears at the prompt
            #   - 0: When "Login incorrect" appears at the prompt
            succeeded, _, _ = tn.expect(
                [b"^Login incorrect$", b">$"], timeout=5
            )

            if succeeded == 1:
                return True, "Login succeeded"
            else:
                return False, "Login failed"
