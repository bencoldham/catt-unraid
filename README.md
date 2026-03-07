# Cast All The Things (CATT) Bitfocus Dashboard/Site Caster

Intended to repurpose Nest Hub/Chromecast devices to dedicated virtual kiosks for Bitfocus Companion. However it can be used to continually cast any URL.

This was built because after endless amounts of trial and error, I could not reliably cast Bitfocus dashboards from Home Assistant directly. CATT in Home Assistant is notoriously hacky, especially with Supervisor given it is a managed environment.

This container aims to subvert all the strange intricacies that occur in HA casting to make Nest Hubs actually reliable as a dashboard.

My real-world testing thus far has proven a highly reliable and snappy experience compared to the Home Assistant variants I tried.

Developed for deployment as an **Unraid Docker container**, but can be containerised on any platform.

## Getting Started
#### **IMPORTANT**
### Host mode

The **Network Type** must be set to `Host`. This is required for the script to discover Chromecast devices on your local network.

### Variables
The following environment variables are required in setup:

| Key | Default | Description |
| :--- | :--- | :--- |
| `DEVICE_TO_URL` | *Required* | A comma-separated list of device IPs and their corresponding URLs. |
| `RECAST_INTERVAL` | 60| How often (in seconds) the script should check the cast, and recast if it is idle.|

`DEVICE_TO_URL` should be set as a singular string. You can chain multiple devices by separating them with a comma, in the following format:

`<device_one_ip>=<url_you_want_to_cast>, <device_two_ip>=<another_url_you_want_to_cast>,...`

For example, for a Bitfocus emulator defined in your Companion app:

`DEVICE_TO_URL` = "192.168.20.80=http://192.168.20.50:8000/emulator/12345, 192.168.20.81=http://192.168.20.50:8000/emulator/98765"

## Help
If you are unsure if your container can see your devices, or what their IP addresses are, restart the container and check the logs. 

A network scan is done on every boot:

```
Scanning Chromecasts...
192.168.20.18 - Bedroom Display - Google Inc. Google Nest Hub
192.168.20.22 - Living Display - Google Inc. Google Nest Hub
```

It is **highly recommended** that you set a static IP for your devices if not done already, as they may change.

## Authors

Ben Coldham 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project would not be possible without the great work done in: 
* [Cast All The Things
](https://github.com/skorokithakis/catt/)
* [pychromecast](https://github.com/home-assistant-libs/pychromecast)