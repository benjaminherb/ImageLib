import numpy as np


def generate_gradient(width=256, height=256, start_value=[0, 0, 0],
                      end_value=[255, 255, 255], step=[1, 1, 1], step_size=1):
    arr = np.zeros((height, width, 3), dtype=np.uint8)

    if type(start_value) != list:
        start_value = [start_value, start_value, start_value]

    if type(end_value) != list:
        end_value = [end_value, end_value, end_value]

    if type(step) != list:
        step = [step, step, step]

    print(f"Generating Pattern in {width}x{height} ({step_size}px steps)\n"
          f"Values from {start_value} to {end_value} in {step} steps")

    x = 0
    current_value = start_value.copy()
    while x + step_size <= width:
        arr[:, x:x + step_size] = current_value
        x += step_size
        for c in range(3):
            current_value[c] = current_value[c] + step[c]
            if (end_value[c] >= start_value[c] and current_value[c] >= end_value[c]) \
                    or (end_value[c] < start_value[c] and current_value[c] <= end_value[c]):
                current_value[c] = end_value[c]
        if current_value == end_value:
            break

    if x + step_size < width:
        arr[:, x:x + step_size] = end_value
        arr[:, x + step_size:] = [0, 0, 0]
    else:
        arr[:, x:] = end_value
    return arr
