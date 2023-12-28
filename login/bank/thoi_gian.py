import time

for_total_time = 10

start_time = time.time()


def chuc_nang_gi_do():
    num_steps = 5

    print("Buoc1")

    elapsed_time = time.time() - start_time
    if elapsed_time < for_total_time:
        remaining_wait_time = for_total_time - elapsed_time
    else:
        remaining_wait_time = 0

    if remaining_wait_time > 0:
        wait_time_per_step = remaining_wait_time / (num_steps - 1)
        time.sleep(wait_time_per_step)

    print("Buoc2")

    elapsed_time = time.time() - start_time
    if elapsed_time < for_total_time:
        remaining_wait_time = for_total_time - elapsed_time
    else:
        remaining_wait_time = 0

    if remaining_wait_time > 0:
        wait_time_per_step = remaining_wait_time / (num_steps - 2)
        time.sleep(wait_time_per_step)

    print("Buoc3")

    elapsed_time = time.time() - start_time
    if elapsed_time < for_total_time:
        remaining_wait_time = for_total_time - elapsed_time
    else:
        remaining_wait_time = 0

    if remaining_wait_time > 0:
        wait_time_per_step = remaining_wait_time / (num_steps - 3)
        time.sleep(wait_time_per_step)

    print("Buoc4")

    elapsed_time = time.time() - start_time
    if elapsed_time < for_total_time:
        remaining_wait_time = for_total_time - elapsed_time
    else:
        remaining_wait_time = 0

    if remaining_wait_time > 0:
        wait_time_per_step = remaining_wait_time / (num_steps - 4)
        time.sleep(wait_time_per_step)

    print("Buoc5")


chuc_nang_gi_do()
print(round(time.time() - start_time))
