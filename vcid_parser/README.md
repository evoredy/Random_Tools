# Welcome to a VCID Parser v0.0.1a

Thid is a simple tool that takes ingests a serial log file from a modem and extracts the caller id
information when in AT+VCID=1 (human readable CID command for) mode. It then converts every message/packet 
into a JSON bucket. With the increase of scam phone calls, a more conveneient solution is needed to track,
review and batch report large groups of numbers to phone carriers for their incident response or other teams. 

To run and/or compile, you will need
* [python3]
* [log data]
* [modem with callerID support]
* [terminal emulator with logging]

## Getting started

To run (if no output is entered, the script will print to screen)
```
$ python3 vcidlog2json.py term_log.txt [output.json]
```

Notes and Errata:

```
Written completely with GPT4 prompts after about 5 iterations over 30 minutes
```

Sample output:

```
{
    "packet_number": 9,
    "DATE": "0709",
    "TIME": "2334",
    "NMBR": "5555551231",
    "NAME": "Name Unavailabl"
}
```

## Changelog v0.0.1a
```
  - initial release
```

## Known Issues
```
  - STDOUT is not formatted the same way as the JSON (which is correctly formated)
  - TODO: test with multiple modems
  - TODO: publish to internal subscriber API
```
