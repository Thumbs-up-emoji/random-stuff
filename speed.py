import timeit

start1 = timeit.default_timer()
print("too slow lmao")
# Your code here
start2 = timeit.default_timer()
end = timeit.default_timer()
print(f"Time elapsed in initial printing: {end - start2}"+f"\nTime elapsed in timing: {start2 - start1}"+f"\nTime elapsed in total: {end - start1}")