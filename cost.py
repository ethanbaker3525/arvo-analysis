import common

average_time = sum([sum(times) / len(times) for times in common.runtimes.values()]) / len(common.runtimes)
print(f"Average time to run image: {average_time} seconds")
print(f"Predicted time to run all images: {average_time * len(common.dh_cases) / 60 / 60} hours")

#print(f": {total_size} bytes (~{(total_size / (1024 ** 4)):.2f} TB)")