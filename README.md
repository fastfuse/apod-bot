### NASA APOD telegram bot


Run as [service](http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/):

```sh
$> sudo systemctl start/restart apod.service

```

Check logs:

```sh
$> sudo journalctl -f -u apod.service
```
