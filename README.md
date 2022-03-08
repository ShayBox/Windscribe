# Windscribe
A python wrapper library for Windscribe CLI

This is based on [anton.alvariumsoft/python-windscribe-cli-wapper](https://gitlab.com/anton.alvariumsoft/python-windscribe-cli-wapper)

This was tested with Windscribe CLI v1.4  
Note: Sometimes Windscribe CLI has errors with its commands, I can't fix this

#### Requirements
- [git](https://git-scm.com/)

#### Install
```
$ pip install git+https://github.com/shaybox/windscribe.git
```

#### Usage

```py
import windscribe

status = windscribe.status()
print(status)

account = windscribe.account()
print(account)

windscribe.connect("Vice")

windscribe.firewall()
windscribe.firewall("auto")

windscribe.lanbypass()
windscribe.lanbypass("on")

locations = windscribe.locations()
print(locations)
```
