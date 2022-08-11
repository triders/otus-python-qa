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

## 3. API DDT tests
_Run API DDT tests via Docker_
1. `docker build -t tests_api:1.0 ./api_data_driven_tests`
2. `docker run --rm tests_api:1.0`
   OR better option is to run in parallel:
    `docker run --rm tests_api:1.0 pytest -n 5` 

