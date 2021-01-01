a = [1, -3, 2, 1,-1]
#a = [-2, 3 ,2,-1]
start = 0
end = 0
max_subarray = [a[0]]
glob_max_subarr = [a[0]]
global_sum = sum(max_subarray)
for i in range(1, len(a)):
    local_max = max(sum(max_subarray)+a[i], a[i])
    if a[i] > sum(max_subarray)+a[i]:
        max_subarray = [a[i]]
    else:
        max_subarray.append(a[i])

    if local_max > global_sum:
        global_sum = local_max
        glob_max_subarr = max_subarray.copy()
print(global_sum)
print(glob_max_subarr)
