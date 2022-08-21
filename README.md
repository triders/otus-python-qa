# Homework for online course [Python QA Engineer from OTUS](https://otus.ru/lessons/avtomatizaciya-web-testirovaniya/)

## 1. UI tests for opencart

Example command:

```
pytest --browser_name=chrome --bv=102.0 --base_url=http://192.168.1.1:8081 --username=admin --password=secure123 --executor=192.168.1.1 --vnc page_objects_and_tests_for_opencart

```

1. `pytest` arguments
   1. `-m=smoke` run only smoke tests
   2. `--base_url=http://192.168.1.1:8081` URL to running opencart (How-to setup in p.3 below)
   2. `--username=SOME_USERNAME --password=SOME_PASSWORD` Get (or set up your own) Opencart ADMIN creds
      from `opencart_ui_tests/opencart_docker/docker-compose.yml`
   3. `--browser_name=chrome` select browser name
   4. `--executor`
      1. `--executor=local` to run locally (ensure you have Browser and corresponding Driver)
      2. `--executor={REMOTE_EXECUTOR_IP}` to run via Selenoid, arguments:
         1. `--vnc` capture [UI of tests execution](https://aerokube.com/selenoid-ui/latest/)
         2. `--bv` select browser version
         3. `--videos` save UI of tests execution to files
   5. `-n=4` run tests in parallel, e.g. 4 threads
2. Selenoid setup
   1. Prepare Selenoid via [Configuration Manager](https://aerokube.com/cm/latest/):
   2. `./cm selenoid start --vnc`
   3. `./cm selenoid-ui start`
3. OpenCart setup
   1. specify your local IP and Admin creds
      in `opencart_ui_tests/opencart_docker/docker-compose.yml`
   2. `cd opencart_ui_tests/opencart_docker`
   3. `docker compose up -d`
4. Allure reports
   1. install Allure locally
   2. run `allure generate`

## 2. Parser for `access.log` file

Format must be the following:

`'91.113.11.120 - - [24/Sep/2019:21:16:13 +0200] "GET /apple-touch-icon-120x120-precomposed.png HTTP/1.1" 404 246 "-" "MobileSafari/604.1 CFNetwork/978.0.7 Darwin/18.7.0" 6203'`

1. Analyze the exact file: `python3 access_log_parser.py --f /path/to/access.log`
2. Or analyze all _*.log_ files in the entire directory: `--d /path/to/logs_directory`
3. (optional) `--n=10` Specify how many top elements to show in stats (N ip with most requests, N longest requests
   duration). Default is `3`
4. (optional) `--v` Print the execution progress in stdout. Default is `False`

Results will be written in the file `result_access_log_stats.json` (in the directory of the script)


## 3. API DDT tests
_Run API DDT tests via Docker_
1. `docker build -t tests_api:1.0 ./api_data_driven_tests`
2. `docker run --rm tests_api:1.0`
   OR better option is to run in parallel:
    `docker run --rm tests_api:1.0 pytest -n 5` 


## 4. Socket: simple HTTP server

0. `cd /linux/sockets_hw`
1. SERVER
   - `python3 socket_server.py {BACKLOG}` start a localhost server. You can type a number of backlog connections server
     will listen to (default is 10).
2. CURL
   - `curl 127.0.0.1:PORT`
3. Open in Browser
   - `http://127.0.0.1:PORT/`
4. BONUS: CLIENT script
   - `python3 socket_client.py {SERVER_PORT}`
      - Type a request to server in the HTTP format, e.g.:
        `GET /?status=500 HTTP/1.1\r\nHeader one: one\r\nHeader two: two\r\nContent-Type: text/html\r\n\r\n`
      - OR Type `'path:path/to/file'` to send an HTTP request from a text file (see/use the examples at ./http_requests
        folder)

## _requirements: selenium + pytest-failed-screenshots issue_

`pytest-failed-screenshot` package should not be in `requirements.txt` bacause it causes several issues:

1. pip issue: infinite package dependency resolving
2. ` ModuleNotFoundError: No module named 'selenium'` error in tests execution

How to install requirements and make sure screenshots on failure work:

```
python3 -m venv venv
. venv/bin/activate
pip install pip -U
pip install -r requirements.txt
deactivate
. venv/bin/activate
pip install pytest-failed-screenshot
pip install selenium==4.1.3
```
