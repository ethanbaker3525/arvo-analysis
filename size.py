import common

total_size = sum([case["full_size"] for case in common.dh_cases]) # finding the size of the entire suite
print(f"Total space required for n132/arvo: {total_size} bytes (~{(total_size / (1024 ** 4)):.2f} TB)")
print(f"Average space required for n132/arvo: {total_size/len(common.dh_cases)} bytes (~{((total_size/len(common.dh_cases)) / (1024 ** 3)):.2f} GB)")

    