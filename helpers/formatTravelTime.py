def format_travel_time(total_minutes):
    if isinstance(total_minutes, str): return total_minutes
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if hours > 0:
        if minutes == 0:
            return f"{hours} hr{'s' if hours > 1 else ''}"
        return f"{hours} hr{'s' if hours > 1 else ''} {minutes} mins"
    else:
        return f"{minutes} mins"