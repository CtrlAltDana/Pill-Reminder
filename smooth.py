def smooth(value, smoothed_value, alpha):
    return  alpha * value + (1-alpha) * smoothed_value