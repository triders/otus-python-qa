import re

RE_REQUEST_BY_METHOD = r'(POST|GET|PUT|DELETE|HEAD|CONNECT|OPTIONS|TRACE|PATCH)'
RE_IP_ADDRESS = r'(\d{1,3}\.){3}\d{1,3}'


def get_total_lines_in_file(path_to_file) -> int:
    num_lines = sum(1 for line in open(path_to_file))
    return num_lines


def count_requests_by_methods(path_to_logfile) -> list:
    methods_count = {"POST": 0, "GET": 0, "PUT": 0, "DELETE": 0, "HEAD": 0,
                     "CONNECT": 0, "OPTIONS": 0, "TRACE": 0, "PATCH": 0}
    with open(path_to_logfile, "r") as log:
        for line in log:
            match = re.search(RE_REQUEST_BY_METHOD, line)
            methods_count[match.group(0)] += 1
    methods_count = sorted(methods_count.items(), key=lambda t: -t[1])
    return methods_count


def get_top_three_ips(path_to_logfile) -> list:
    # get all ip addresses (with duplicates)
    with open(path_to_logfile, "r") as log:
        ip_list = []
        for line in log:
            ip = re.match(RE_IP_ADDRESS, line)
            ip_list.append(ip.group(0))

    # count requests for each ip
    ip_requests = {ip: 0 for ip in set(ip_list)}
    for ip in ip_list:
        ip_requests[ip] += 1

    # sort and get top 3
    ip_requests_sorted = sorted(ip_requests.items(), key=lambda t: -t[1])
    top_three_ips = ip_requests_sorted[:3]
    return top_three_ips


if __name__ == "__main__":
    print(count_requests_by_methods("access_100_head_and_tail.log"))
