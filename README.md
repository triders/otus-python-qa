# Homework for online course [Python QA Engineer from OTUS](https://otus.ru/lessons/avtomatizaciya-web-testirovaniya/)

## 1. UI tests for opencart

Example command:

```
pytest --browser_name=chrome --bv=102.0 --base_url=http://192.168.1.1:8081 --username=admin --password=secure123 --executor=192.168.2.2 --vnc page_objects_and_tests_for_opencart 
```

0. Preparation
   1. Get opencart `ADMIN` creds from here https://gist.github.com/konflic/ecd93a4bf7666d97d62bcecbe2713e55)

      1. pass creads as args `--username='SOME_USERNAME''` `--password='SOME_PASSWORD''` in command line when run tests
         via `pytest`
      2. OR create `auth.py` in the `/page_objects_and_tests_for_opencart/` directory with the following structure:
      ```
      class Users:
       ADMIN = {"username": "SOME_USERNAME", "password": "SOME_PASSWORD"}
      ```

1. `pytest` arguments
   1. `--base_url=http://192.168.1.1:8081` URL to running opencart
   2. `--browser_name=chrome` select browser name
   3. `--executor`
      1. `--executor=local` to run locally
      2. `--executor={REMOTE_EXECUTOR_IP}` to run via Selenoid, arguments:
         1. `--vnc` capture [UI of execution](https://aerokube.com/selenoid-ui/latest/)
         2. `--bv` select browser version
2. Selenoid setup
   1. Prepare Selenoid via Configuration Manager:
   2. `./cm selenoid start --vnc`
   3. `./cm selenoid-ui start` (optional)
3. Allure reports
   1. install Allure
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

## 3. Socket: simple HTTP server

0. `cd /linux/sockets_hw`
1. SERVER
   1. `python3 socket_server.py {BACKLOG}` start a localhost server. You can type a number of backlog connections server
      will listen to (default is 10).
      Then copy the port number from message:
      `Hi! This is a simple HTTP server: 127.0.0.1:24895`
2. CLIENTS (You can connect several clients to the server, but they will wait in the queue and processed one after another) 
   1. `python3 socket_client.py {SERVER_PORT}` connect a client to the localhost server (type the port number)
      1. Type a request to server in the HTTP format, e.g.:
         `GET /?status=500 HTTP/1.1\r\nHeader one: one\r\nHeader two: two\r\nContent-Type: text/html\r\n\r\n
         `
      2. OR Type `'path:path/to/file'` to send an HTTP request from a text file (see/use the examples at ./http_requests
         folder)
