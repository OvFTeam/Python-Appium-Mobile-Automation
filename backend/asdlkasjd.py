import time

total_wait_time = float(input("time: "))

num_steps = 10

wait_time_per_step = total_wait_time / num_steps
for i in range(num_steps):
    print("step ", i)
    time.sleep(wait_time_per_step)
