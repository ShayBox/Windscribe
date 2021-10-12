from dataclasses import dataclass
import pexpect
import re
import subprocess


class StdoutException(Exception):
    def __init__(self):
        super().__init__("Unexpected stdout line count from windscribe")


@dataclass(frozen=True)
class Status:
    pid: str
    running: bool
    uptime: str
    address: str
    connected: bool
    location: str


@dataclass(frozen=True)
class Account:
    username: str
    usage: str
    cap: str
    plan: str


@dataclass(frozen=True)
class Location:
    geo: str
    short: str
    city: str
    label: str
    pro: bool = False


def _parse_line(self, line):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    result = ansi_escape.sub("", line.decode("UTF-8").strip())
    return result


def _run(self, args):
    child = pexpect.spawn("windscribe", args)
    lines = list(map(_parse_line, child.readlines()))
    return lines


def status(self):
    lines = _run(["status"])
    if len(lines) < 3:
        print("\n".join(lines))
        raise StdoutException

    info = lines[0].split(", ")
    if len(info) < 3:
        print("\n".join(lines))
        raise StdoutException

    pid = info[0].split("windscribe -- pid: ")[1]
    running = info[1].split("status: ")[1] == "running"
    uptime = info[2].split("uptime: ")[1]
    address = lines[1].split("IP: ")[1]
    connected = lines[2] != "DISCONNECTED"
    location = lines[2].split(" -- ")[1] if connected else "N/A"

    return Status(pid, running, uptime, address, connected, location)


def account(self):
    lines = _run(["account"])
    if len(lines) < 4:
        print("\n".join(lines))
        raise StdoutException

    username = lines[1].split("Username: ")[1]
    data = lines[2].split("Data Usage: ")[1].split(" / ")
    usage = data[0]
    cap = data[1]
    plan = lines[3].split("Plan: ")[1]

    return Account(username, usage, cap, plan)


def connect(self, location):
    lines = _run(["connect", location])
    print("\n".join(lines))


def disconnect(self):
    lines = _run(["disconnect"])
    print("\n".join(lines))


def firewall(self, mode: str = None):
    if mode:
        lines = _run(["firewall", mode])
        print("\n".join(lines))
        return

    lines = _run(["firewall"])
    if len(lines) < 8:
        print("\n".join(lines))
        raise StdoutException

    return lines[2].split("Firewall mode: ")[1]


def lanbypass(self, mode: str = None):
    if mode:
        lines = _run(["lanbypass", mode])
        print("\n".join(lines))
        return

    lines = _run(["lanbypass"])
    if len(lines) < 6:
        print("\n".join(lines))
        raise StdoutException

    return lines[2].split("Default mode: ")[1]


def _parse_location(self, line):
    array = []
    for segment in filter(None, line.split("  ")):
        value = segment.strip()
        if value:
            array.append(value)

    return array


def locations(self):
    lines = _run(["locations"])
    if len(lines) < 1:
        print("\n".join(lines))
        raise StdoutException

    locations = []
    for line in lines:
        location = Location(*_parse_location(line))
        locations.append(location)

    return locations


def login(self, username: str = None, password: str = None):
    child = pexpect.spawn("windscribe", ["login"])

    logged_in = child.expect(["Windscribe Username:", "Already Logged in"])
    if logged_in == 1:
        print("Already Logged in")
        return

    if logged_in == 0:
        child.sendline(username)
        child.expect("Windscribe Password:")
        child.sendline(password)
        print("\n".join(_parse_line(line) for line in child.readlines()))
        return

    raise RuntimeError("Unexpected error")


def logout(self):
    lines = _run(["logout"])
    print("\n".join(lines))
