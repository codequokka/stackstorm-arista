from __future__ import annotations

import napalm


def main():
    hostname = "192.168.1.129"
    port = 10443
    user = "admin"
    password = "arista"
    commands = ["show version", "show clock"]

    driver = napalm.get_network_driver("eos")
    device = driver(hostname, user, password, optional_args={"port": port})

    device.open()

    res = device.cli(commads)
    print(res)


if __name__ == "__main__":
    main()
