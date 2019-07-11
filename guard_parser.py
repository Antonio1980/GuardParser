import os
import re
import datetime


def parse_file(log_file_path):
    regex = r'''(?P<timestamp>[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9])'''

    with open(log_file_path, "r") as file:
        match_dict = {}
        for line in file:
            for match in re.finditer(regex, line, re.S):
                timestamp = match.group()
                if match.string.split()[2] == "Guard" and match.string.split()[3][1:] not in match_dict.keys():
                    guard_number = match.string.split()[3][1:]
                    match_dict[guard_number] = {}
                    match_dict[guard_number]["start"] = []
                    match_dict[guard_number]["total"] = float()
                elif match.string.split()[2] == "Guard" and match.string.split()[3][1] in match_dict.keys():
                    continue
                if match.string.split()[2] == "falls":
                    start_sleep = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
                    match_dict[guard_number]["start"].append(str(start_sleep.time()))
                if match.string.split()[2] == "wakes":
                    stop_sleep = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
                    delta_ = stop_sleep - start_sleep
                    match_dict[guard_number]["total"] += delta_.total_seconds()
        return match_dict


def who_sleep(dict_):
    return sorted(dict_.items(), key=lambda line: line[1]["total"])[-1]


def find_sleep(list_times):
    counter = 0
    num = list_times[0]

    for i in list_times:
        curr_frequency = list_times.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i

    return num


def print_result(guard_number, time_sleep):
    print(f"“Guard {guard_number} is most likely to be asleep in {time_sleep}”")


if __name__ == '__main__':
    file_ = os.path.join("activity/activity.log")
    file_parsed = parse_file(file_)
    guard = who_sleep(file_parsed)
    guard_num = guard[0]
    starts = guard[1]["start"]
    start = find_sleep(starts)
    print_result(guard_num, start)
