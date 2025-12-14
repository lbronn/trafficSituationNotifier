def parse_duration(duration_str):
    if not duration_str: return 0
    return int(duration_str.replace("s", "")) // 60