import time

# open a file with a name of statistics+timestamp.csv

file=open('./statistics'+str(int(time.time()))+'.csv','w')
file.write('1,1\n')
file.write('2,2\n')
file.write('1,1\n')
file.write('3,3\n')
file.write('1,1\n')
file.close()