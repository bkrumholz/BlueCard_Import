from datetime import date, datetime,timedelta, time

def generateFile(input_file,output_dir,prefix_skip_list=[],cmg_id='973'):
    active_prefix_set = set([])
    bs_skip = 0
    dup_skip = 0
    expire_skip = 0
    list_skip = 0
    today = date.today()
    expire_date = datetime.combine(today - timedelta(weeks=52), time(0, 0, 0, 0))  #Expire any prefix that was sunset more than 52 weeks ago.
    expire_date=expire_date.replace(day=1)
    output_file = output_dir+"BC_import_" + expire_date.strftime('%Y%m%d')+"_"+today.strftime('%Y%m%d')+".txt"

    print("Output File: ", output_file)

    try:
        opfile = open(output_file,'w')
    except Exception as e:
        print("Output file {0} could not be opened: {1}".format(output_file, e))
        return None
    try:
        ipfile = open(input_file,"r")
    except Exception as e:
        print("Input file {0} could not be opened: {1}".format_map(input_file, e))
        return None
    print("1,",cmg_id,file=opfile)   #Set import record to Blue Card component
    print("20,1/1/1900",file=opfile) #Set contact to component contact
    for line in ipfile:
        ok = False
        values = line.rstrip().split("|")
        prefix = values[0]
        type = values[2]
        from_date = values[4]
        to_date = values[5]
        if prefix in prefix_skip_list:
            print(prefix, type, from_date, to_date, " **SKIPPED - IGNORE LIST**", end="\n")
            list_skip+=1
        if type != 'C':   #only look at prefixes for Blue Cross
            print(prefix, type, from_date, to_date, " **SKIPPED - BLUE SHIELD**", end="\n")
            bs_skip+=1
            continue
        if to_date == "99999999":    #handle unexpired prefixes
            to_date = "21991231"     #Good for the next century
        if expire_date < datetime.strptime(to_date,'%Y%m%d'):
            ok = True
        if ok:
            if prefix in active_prefix_set:
                print(prefix, type, from_date, to_date, " **SKIPPED - ALREADY IN SET**", end="\n")
                dup_skip+=1
            else:
                active_prefix_set.add(prefix)
                print(prefix,type,from_date,to_date,end="\n")
                print("1100",prefix, sep=",", file=opfile)
        else:
            print(prefix, type, from_date, to_date," **SKIPPED - EXPIRED**", end="\n")
            expire_skip
    print("PREFIX COUNT: ",len(active_prefix_set))
    return output_file


def print_stats(active_prefix_cnt,expire_skip):
    pass

if __name__=="__main__":
    input_dir = r'C:/Output/BlueCard/'  #Hardcode directory for ease of use
    cmg_id = '973'  #Hardcode component used to contain prefix list
    input_file = input('Filename:')
    input_fullpath_file=input_dir+input_file
    output_dir = r'C:/Output/BlueCard/'
    output_file=generateFile(input_fullpath_file,output_dir,cmg_id)
    print("File sent to: ",output_file)

