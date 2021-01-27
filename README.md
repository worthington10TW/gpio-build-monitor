# Build monitor

Now the world is remote, do you struggle to keep track of you builds?

Do you want to decouple your build monitor from your machine?

Get yourself a raspberry pi, some LEDs and clone this repo!

## To run

- Setup `make setup`
- Test `make test`
- Debug `make debug`
- Publish `make publish`
- Install `make install-monitor`

## Install

To install directly from github:

### Latest

`pip3 install git+https://github.com/worthington10TW/gpio-build-monitor#egg=monitor`

### Run on your raspberry pi 

When running on your machine the mock GPIO board is used, this is disabled when running optimized.

First make sure the module is installed.

Install the GPIO package `pip3 install Rpi.GPIO`

Then run the module.

`python3 -O -m monitor -conf integrations.json`

## Signals

- Blue light: Fetching data
- Green light: **All** builds pass
- Red light: **Any** builds fail
- Yellow pulse: **Any** builds are running

## Setup

Example setup can be found here: `src/integrations.json`

Config is passed using the `-conf` argument variable

```json
{
    "poll_in_seconds": 30,
    "integrations": [
            {
                "type": "",
                "username": "",
                "repo": "",
                "excluded_workflows": [ "" ]
            }
        ]
}
```

### Current integrations

- CircleCI
- GitHub Actions
  
Personal API tokens are read from environment variables

```shell
export GITHUB_TOKEN=<TOKEN>
export CIRCLE_CI_TOKEN<TOKEN>
```

## Pin setup

- Pin constants can be found in `src/gpio/constants.py`

## Shopping list

[Raspberry Pi Zero](https://thepihut.com/products/raspberry-pi-zero-w?src=raspberrypi)
[SD card](https://www.amazon.co.uk/Kingston-microSD-SDCS2-Adapter-Included/dp/B07YGZ7FY7/)
[Resistor kit](https://thepihut.com/products/ultimate-resistor-kit)
[LED kit](https://thepihut.com/products/ultimate-5mm-led-kit)
[Cables](https://thepihut.com/products/thepihuts-jumper-bumper-pack-120pcs-dupont-wire)
[Breadboard](https://thepihut.com/products/raspberry-pi-breadboard-half-size)
[Shrink cables](https://thepihut.com/products/multi-colored-heat-shrink-pack-3-32-1-8-3-16-diameters)

[Anti-static band](https://www.amazon.co.uk/gp/product/B07TGD5CD8/)
[Rubber mat](https://www.amazon.co.uk/gp/product/B075D9R8PZ/)
[Soldering iron](https://www.amazon.co.uk/gp/product/B07X3CZ3FJ/)
[Multimeter](https://www.amazon.co.uk/gp/product/B01N35ZVKY/)

[Frame](https://www.ikea.com/gb/en/p/ribba-frame-white-80378423/)

## TODO

- [ ] Feedback when connection is unsuccessful.
- [ ] Allow multiple access tokens for integrations.
- [ ] Allow default pin overrides
- [ ] Enhanced CLI functionality, possibly with click



