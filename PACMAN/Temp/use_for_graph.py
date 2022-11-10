import numpy as np
import matplotlib.pyplot as plt
with open(r"graphbuilderforall.txt", 'r') as fp:
    lines = len(fp.readlines())
    print('Total Number of lines:', lines)
with open(r"graphbuilderforall.txt", 'r') as fp1:
    strlines = fp1.readlines()
# y = []
y = [float(i.replace("\n", "")) for i in strlines]
x = np.arange(1, lines+1, 1)
print(x)
print(len(y))
plt.plot(x, y)
plt.show()