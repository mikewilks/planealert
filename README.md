Simple python script that consumes the output of [readsb](https://github.com/wiedehopf/readsb) via a url and alerts if a particular aircraft is seen within a specified number of miles.

Parameters are loaded from params.json in the same directory as the script.

Alerting uses [Apprise](https://github.com/caronc/apprise) and the url in the parameters file is in [Apprive format](https://github.com/caronc/apprise/wiki).




