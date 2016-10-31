# python_latest_scan_issues

<b> Description </b>

This program archives the latest scan issues for all active servers and deactivated servers that were last seen 24 hours ago.

<b> Prerequisities: </b>

1. cloudpassage sdk (install via pip install cloudpassage)

2. Populate the following values in portal.yml (located in configs directory)

  * key_id, secret_key pair (This is your halo portal api_keys)

  * last_24_hours (True/False): include servers that were deactivated for less than 24 hours

<b> Dependencies: </b>

1. Python 2.7.10
2. cloudpassage python package
3. dateutil.parser (install via pip install python-dateutil)
4. logbook (install via pip install logbook)

<b> To use: </b>

```
python latest_scan_issues.py
```
