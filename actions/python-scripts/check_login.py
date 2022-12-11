import telnetlib

from st2actions.runners.pythonrunner import Action


class CheckLoginAction(Action):
    def run(self, hostname, port, user, password):
        """Check login by using telnet

        Parameters
        ----------
        hostname : str
            A host name to log in to
        port : int
            A port number to log in to
        user : str
            A user name to log in to
        password : str
            A password to log in to

        Returns
        -------
        tuple[bool, str]
            Boolean for successful login or not
            Message for successful login or not
        """
        with telnetlib.Telnet(hostname, port) as tn:

            # Try to login
            tn.read_until(b"Username:")
            tn.write(user.encode("ascii") + b"\n")
            tn.read_until(b"Password:")
            tn.write(password.encode("ascii") + b"\n")

            # Check login has succeeded
            succeeded, _, _ = tn.expect(
                [b">$", b"^Login incorrect$"], timeout=5
            )

            if succeeded == 0:
                return True, "Login succeeded"
            else:
                return False, "Login failed"
