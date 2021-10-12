# Windscribe
A python wrapper library for Windscribe CLI

This is based on [anton.alvariumsoft/python-windscribe-cli-wapper](https://gitlab.com/anton.alvariumsoft/python-windscribe-cli-wapper)

This was tested with Windscribe CLI v1.4  
Note: Sometimes Windscribe CLI has errors with its commands, I can't fix this

#### Requirements
- [git](https://git-scm.com/)
- [poetry](https://python-poetry.org/)

#### Install
```
$ git clone https://github.com/ShayBox/Windscribe.git
$ cd Windscribe
$ poetry build
$ pip install dist/Windscribe-0.1.0.tar.gz --user
```

#### Usage

```py
import Windscribe

status = Windscribe.status()
print(status)

account = Windscribe.account()
print(account)

Windscribe.connect("Vice")

Windscribe.firewall()
Windscribe.firewall("auto")

Windscribe.lanbypass()
Windscribe.lanbypass("on")

locations = Windscribe.locations()
print(locations)
```