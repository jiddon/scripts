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
                writer.writerow([date, time, value])
    print(f"\nsplit DCS file into:")
    return new_paths

if __name__=="__main__":
    fire.Fire(split_files)
    
            
