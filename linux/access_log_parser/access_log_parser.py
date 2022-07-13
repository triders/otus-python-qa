import os
import re
import json
import argparse

RE_METHOD = r'(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE|PATCH)'
RE_IP_ADDRESS = r'(\d{1,3}\.){3}\d{1,3}'
RE_URL = r'"(http[s]?:\/\/.+)" "'
RE_DATE_TIME = r'\[(.+) \+\d{4}\]'
RE_DURATION = r'\d+$'
LOG_LINE_EXAMPLE = '91.113.11.120 - - [24/Sep/2019:21:16:13 +0200] "GET /apple-touch-icon-120x120-precomposed.png ' \
                   'HTTP/1.1" 404 246 "-" "MobileSafari/604.1 CFNetwork/978.0.7 Darwin/18.7.0" 6203'

parser = argparse.ArgumentParser()
parser.add_argument('--f', dest='path_to_logfile', action='store', help='Path to logfile to be processed')
parser.add_argument('--d', dest='path_to_directory', action='store',
                    help='Path to directory with logfiles to be processed')
parser.add_argument('--n', dest='top_n', type=int, action='store', default=3,
                    help='How many top elements (ip, request duration)')
parser.add_argument('--v', dest='verbose', action='store_true', default=False,
                    help='Print execution progress in stdout')
args = parser.parse_args()


def _parse_log_line(log_line):
    """Returns dict:
    {'method': 'GET', 'url': 'https://example.com', 'ip': '91.2.11.2', 'duration': 13, 'date_time': '24/Sep/2019:21:16:13'}
    """
    method_match = re.search(RE_METHOD, log_line)
    url_match = re.search(RE_URL, log_line)  # some requests do not have URL
    ip_match = re.search(RE_IP_ADDRESS, log_line)
    duration_match = re.search(RE_DURATION, log_line)
    date_time_match = re.search(RE_DATE_TIME, log_line)

    request_data = {
        'method': method_match.group(0) if method_match else '-',
        'url': url_match.group(1) if url_match else '-',
        'ip': ip_match.group(0) if ip_match else '-',
        'duration': int(duration_match.group(0)) if duration_match else '-',
        'date_time': date_time_match.group(1) if date_time_match else '-',
    }

    return request_data


def _get_total_lines_in_file(path_to_file) -> int:
    num_lines = sum(1 for line in open(path_to_file))
    return num_lines


def _count_requests_by_methods(path_to_logfile) -> list:
    methods_count = {"POST": 0, "GET": 0, "PUT": 0, "DELETE": 0, "HEAD": 0,
                     "CONNECT": 0, "OPTIONS": 0, "TRACE": 0, "PATCH": 0}
    with open(path_to_logfile, "r") as log:
        for line in log:
            method_match = re.search(RE_METHOD, line)
            if method_match:
                methods_count[method_match.group(0)] += 1
    methods_count = sorted(methods_count.items(), key=lambda t: -t[1])
    return methods_count


def _get_top_n_ips(path_to_logfile, how_much_top_items) -> list:
    # get all ip addresses (with duplicates)
    with open(path_to_logfile, "r") as log:
        ip_list = []
        for line in log:
            ip_match = re.match(RE_IP_ADDRESS, line)
            if ip_match:
                ip_list.append(ip_match.group(0))

    # count requests for each ip
    ip_requests = {ip: 0 for ip in set(ip_list)}
    for ip in ip_list:
        ip_requests[ip] += 1

    # sort and get top N (N = how_much_top_items)
    ip_requests_sorted = sorted(ip_requests.items(), key=lambda t: -t[1])
    top_n_ips = ip_requests_sorted[:how_much_top_items]
    return top_n_ips


def _get_top_n_longest_duration_requests(path_to_logfile, how_much_top_items) -> list:
    # get all requests parsed data
    with open(path_to_logfile, "r") as log:
        requests_data = [_parse_log_line(line) for line in log]

    # sort and get top N (N = how_much_top_items)
    requests_data_sorted = sorted(requests_data, key=lambda t: -t['duration'])
    top_n_longest_duration = requests_data_sorted[:how_much_top_items]
    return top_n_longest_duration


def get_access_log_stats(path_to_logfile=None, path_to_directory=None, how_much_top_items=3, verbose=False):
    """Creates a json file with stats for a specific log file or all .log files in a directory (recursively)"""

    stats = {}
    # analyze a single file
    if path_to_logfile:
        if verbose:
            print(f"\nAnalyzing: {path_to_logfile}")
        num_lines = _get_total_lines_in_file(path_to_logfile)
        if verbose:
            print(f"\\__ Counting requests by methods...")
        methods_count = _count_requests_by_methods(path_to_logfile)
        if verbose:
            print(f"\\__ Getting top {how_much_top_items} ips with most requests count...")
        top_n_ips = _get_top_n_ips(path_to_logfile, how_much_top_items=how_much_top_items)
        if verbose:
            print(f"\\__ Getting top {how_much_top_items} longest requests...")
        top_n_duration = _get_top_n_longest_duration_requests(path_to_logfile, how_much_top_items=how_much_top_items)
        stats = {
            'requests_count': num_lines,
            'methods_count': methods_count,
            f'top_{how_much_top_items}_ips': top_n_ips,
            f'top_{how_much_top_items}_longest_duration_requests': top_n_duration,
        }

    # analyze all .log files in a directory
    if path_to_directory and not path_to_logfile:
        for log_file_i in os.listdir(path_to_directory):
            if log_file_i.endswith(".log"):
                path_to_logfile_i = os.path.join(path_to_directory, log_file_i)
                stats_i = get_access_log_stats(
                    path_to_logfile=path_to_logfile_i,
                    how_much_top_items=how_much_top_items,
                    verbose=verbose
                )
                stats.update({log_file_i: stats_i})

    # write stats to json file
    with open('result_access_log_stats.json', "w") as file:
        if verbose:
            print(f"Analyzed. Starting writing stats to file: \n"
                  f"    >>> {os.getcwd()}/result_access_log_stats.json\n")
        file.write(json.dumps(stats, indent=4))
    return stats


# run with argparse args
get_access_log_stats(path_to_logfile=args.path_to_logfile, path_to_directory=args.path_to_directory,
                     how_much_top_items=args.top_n, verbose=args.verbose)
