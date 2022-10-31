import fire
import csv

def split_files(filename):
    nf = None
    new_paths = []
    with open(filename, "r") as f:
        for line in f:
            if "ATLPIX" in line:
                if nf:
                    nf.close()
                rodname_start = line.find("LI")
                rodname = line[rodname_start:].strip() # rodname includes measurable
                print(f"found rod: {rodname}")
                assert rodname
                new_f = "./dcs_csv/"+rodname+".csv"
                new_paths.append(new_f)
                nf = open(new_f, 'w')
                writer = csv.writer(nf)
            else:
                cols = line.split()
                date = cols[0].replace(".","")[2:]
                time = cols[1]
                value = float(cols[2])
                #writer.writerow([date, value])
                writer.writerow([date, time, value])
    print(f"\nsplit DCS file into:")
    return new_paths

def daily_avg(filename):
    nf = None
    new_f = filename.replace(".csv", "_daily.csv")
    mean = 0
    with open(filename, "r") as f:
        nf = open(new_f, 'w')
        writer = csv.writer(nf)
        prev_date = None
        n = 0
        for line in f:
            cols = line
            date = cols[0].replace(".","")[2:]
            value = float(cols[1])
            if prev_date == None or prev_date == date:
                mean += value
            else:
                mean = mean / n
                n = 0
                writer.writerow([date, value])
            prev_date = date
            n += 1            
    return new_f

if __name__=="__main__":
    fire.Fire(split_files)
    
            
