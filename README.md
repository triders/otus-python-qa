# otus-python-qa

Homework for online course Python QA Engineer from OTUS
https://otus.ru/lessons/avtomatizaciya-web-testirovaniya/

### Parser for `access.log` file. How-to:

Format must be the following:

`'91.113.11.120 - - [24/Sep/2019:21:16:13 +0200] "GET /apple-touch-icon-120x120-precomposed.png HTTP/1.1" 404 246 "-" "MobileSafari/604.1 CFNetwork/978.0.7 Darwin/18.7.0" 6203'`

1. Analyze the exact file: `python3 access_log_parser.py --f access.log`
2. Or analyze all _*.log_ files in the entire directory: `--d /Users/UserName/path/to/logs`
3. (optional) `--n=10` Specify how many top elements to show in stats (N ip with most requests, N longest requests duration). Default is `3`
4. (optional) `--v=True` Print the execution progress in stdout. Default is `False`

Results will be written in the file `result_access_log_stats.json` (in the directory of the script)
