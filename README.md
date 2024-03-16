# Pretix Check-in buttons on Order Page

This is a plugin for [pretix](https://github.com/pretix/pretix).

Adds check-in related buttons to the order overview page.

> [!WARNING]  
> This feature is not implemented in Pretix due to incompatibility with events using multiple check-in lists; the plugin defaults to the first list accepting the product.

This plugin situationally adds "check-in", "check-out" and "delete check-ins" buttons to the order overview page to quickly manage check-ins of your guests!

## Development setup

1.  Make sure that you have a working [pretix development
    setup](https://docs.pretix.eu/en/latest/development/setup.html).
2.  Clone this repository.
3.  Activate the virtual environment you use for pretix development.
4.  Execute `python setup.py develop` within this directory to register
    this application with pretix's plugin registry.
5.  Execute `make` within this directory to compile translations.
6.  Restart your local pretix server. You can now use the plugin from
    this repository for your events by enabling it in the 'plugins' tab
    in the settings.

This plugin has CI set up to enforce a few code style rules. To check
locally, you need these packages installed:

    pip install flake8 isort black

To check your plugin for rule violations, run:

    black --check .
    isort -c .
    flake8 .

You can auto-fix some of these issues by running:

    isort .
    black .

To automatically check for these issues before you commit, you can run
`.install-hooks`.

# License

Copyright 2024 Daniel Malik

Released under the terms of the Apache License 2.0
