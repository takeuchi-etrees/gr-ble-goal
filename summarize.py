import sys

def read_single(filename):
    total = []

    mac_trans_time = {}
    
    with open(filename) as f:
        line = f.readline()
        while line:
            if line[0:3] == "MAC":
                l = line.rstrip('\n')[4:]
                ll = ["MAC"] + eval(l) + [0, 0]
                ll[-3] = 0
                total.append(ll)
            else:
                l = line.rstrip('\n')[9:]
                ll = ["in_range"] + eval(l) + [0, 0]
                total.append(ll)
                ll[-3] = 0

            line = f.readline()
            line = f.readline()

        total = sorted(total, key=lambda x: (x[2], -ord(x[0][0])))

        total_len = len(total)
        # MAC
        for row_num in range(total_len):
            row = total[row_num]
            try:
                prev_row = total[row_num - 1]
                next_row = total[row_num + 1]
            except IndexError:
                pass
            
            if row[0] == 'MAC':
                if row[1] in mac_trans_time:
                    row[3] = row[2] - mac_trans_time[row[1]]
                    if prev_row[0] == 'in_range':
                            row[4] = row[2] - prev_row[2]
                            row[5] = next_row[2] - row[2]
                mac_trans_time[row[1]] = row[2]

        # output
        for row in total:
            print(row)
            
if __name__ == '__main__':
    args = sys.argv
    read_single(args[1])
