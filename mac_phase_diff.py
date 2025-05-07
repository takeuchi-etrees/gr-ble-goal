import sys

def read_single(filename):
    total = []
    phase_diff = 0

    with open(filename) as f:
        line = f.readline()
        while line:
            row = eval(line.rstrip())
            if row[0] == "MAC":
                out = [row[2], row[1], phase_diff]
                total.append(out)
            else:
                phase_diff = row[1]

            line = f.readline()

        total = sorted(total, key=lambda x: (x[1], x[0]))

        # output
        for row in total:
            print(row)
            
if __name__ == '__main__':
    args = sys.argv
    read_single(args[1])
