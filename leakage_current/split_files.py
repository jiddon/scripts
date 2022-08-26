import csv

def split_files(filename):
    nf = None
    with open(filename, "r") as f:
        for line in f:
            if "ATLPIX" in line:
                if nf:
                    nf.close()
                rodname_start = line.find("LI")
                rodname = line[rodname_start:].strip()
                print(f"found rod: {rodname}")
                assert rodname
                nf = open("./"+rodname+".csv", 'w')
                writer = csv.writer(nf)
            else:
                cols = line.split()
                date = cols[0].replace(".","")[2:]
                time = cols[1]
                value = float(cols[2])
                writer.writerow([date, time, value])

if __name__=="__main__":
    split_files("ibl_high_leakage.txt")
            
