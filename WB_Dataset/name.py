out_file = open("output.csv", "a+")
with open('india87.cfm', "r+") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]
        arr = line.split(" ")
        print(len(arr))
        cnt = 0
        for x in arr:
            if cnt == 227:
                out_file.write("\n")
                cnt = 0
            out_file.write(x+",")
            #print(cnt)
            cnt = cnt+1
    f.close()
out_file.close()