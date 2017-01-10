# wio_sensors

Pull down sensor data from the [Wio](http://iot.seeed.cc/) iOT devices and write them out to [Initial State](https://www.initialstate.com/)
which does some pretty awesome visualisation of the sensor data. You can learn more about
[connecting things up to Initial State](http://blog.initialstate.com/review-wio-link).

## Requirements

* [Initial State python module](http://support.initialstate.com/knowledgebase/articles/590085-how-to-stream-events-in-python)
* Initial State account
* Wio Link or Node devices
* Wio account
* API pages for your Wio devices with the device token and API endpoints for the attached bits

## Configuration


At the shell set the keys for Initial State:
```shell
export IS_BUCKET_KEY=<Your Initial State bucket key>
export IS_ACCESS_KEY=<Your Initial State access key>
```

Move `wios_example.json` to `wios.json` and edit it to reflect the devices you have attached to your Wios.

Not run `get_wio.py` and it'll start polling the devices and sending data into Initial State.