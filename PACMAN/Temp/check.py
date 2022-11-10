from collections import Counter
file = open('count_file.txt')
arr = set()
content = file.readlines()
x = len(content)
visited_states_all = []
for i in range(0, x-8, 8):
    visited_states_all.append(tuple(content[i:i+8]))
    arr.add(tuple(content[i:i+8]))

d = Counter(visited_states_all)
arr_count = []
for i in arr:
    arr_count.append(d[i])
arr = list(arr)
file1 = open('count_sort_file.txt', "a")
for i in range(len(arr_count)):
    file1.write("State: ")
    file1.write("\n")
    file1.write(str(arr[i][0]))
    file1.write(str(arr[i][1]))
    file1.write(str(arr[i][2]))
    file1.write(str(arr[i][3]))
    file1.write(str(arr[i][4]))
    file1.write(str(arr[i][5]))
    file1.write(str(arr[i][6]))
    file1.write(str(arr[i][7]))
    file1.write("\n")
    # file1.write("\n")
    file1.write("Count: ")
    file1.write("\n")
    file1.write(str(arr_count[i]))
    file1.write("\n")
    file1.write("\n")
file1.close()




