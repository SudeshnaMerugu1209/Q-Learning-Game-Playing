import os
file1 = open("ApproxQLearningVisitedStates.txt", "r")
check_for_max_number_of_states_visited = file1.readlines()
file1.close()
res = [eval(i) for i in check_for_max_number_of_states_visited]
print(max(res))