from datetime import date, datetime,timedelta, time
from configparser import ConfigParser
from os.path import exists
##Make sure to update config.ini file with correct file locations and record ID

def generateFile(input_file,output_dir,cmp_id,prefix_skip_list=[],expire_lag=52):
    active_prefix_set = set([])
    list_stats={
        "bs_skip": 0,
        "dup_skip": 0,
        "expire_skip": 0,
        "list_skip": 0,
        "total":0
    }
    today = date.today()
    expire_date = datetime.combine(today - timedelta(weeks=expire_lag), time(0, 0, 0, 0))  #Expire any prefix that was sunset more than 52 weeks ago.
    expire_date=expire_date.replace(day=1)
    output_file = output_dir+"BC_import_" + expire_date.strftime('%Y%m%d')+"_"+today.strftime('%Y%m%d')+".epicimport"

    print("Output File: ", output_file)
    try:
        ipfile = open(input_file,"r")
    except Exception as e:
        print("\nInput file {0} could not be opened: {1}".format(input_file, e))
        return None
    try:
        opfile = open(output_file,'w')
    except Exception as e:
        print("\nOutput file {0} could not be opened: {1}".format(output_file, e))
        return None
    if not cmp_id:
        print("CMP ID was not specified")
        exit(-1)
    print("1,",cmp_id,file=opfile,sep='')   #Set import record to Blue Card component
    print("20,1/1/1900",file=opfile,sep='') #Set contact to component contact
    print("30,2",file=opfile,sep='') #Set component type to 'procedure'
    for cnt,line in enumerate(ipfile):
        ok = False
        values = line.rstrip().split("|")
        try:
            prefix = values[0]
            type = values[2]
            from_date = values[4]
            to_date = values[5]
        except Exception as e:
            print("Line is not in expected format of ""prefix|unused|type|from_date|to_date.")
            print("Line {0}: {1}".format(cnt+1,line))
            exit(-1)
        list_stats['total']+=1
        if not prefix or len(prefix) != 3:  #Skip lines if no 3 character prefix is present
            continue
        if prefix in prefix_skip_list:
            print(prefix, type, from_date, to_date, " **SKIPPED - IGNORE LIST**", end="\n")
            list_stats['list_skip']+=1
        if type != 'C':   #only look at prefixes for Blue Cross
            print(prefix, type, from_date, to_date, " **SKIPPED - BLUE SHIELD**", end="\n")
            list_stats['bs_skip']+=1
            continue
        if to_date == "99999999":    #handle unexpired prefixes
            to_date = "21991231"     #Good for the next century
        if expire_date < datetime.strptime(to_date,'%Y%m%d'):
            ok = True
        if ok:
            if prefix in active_prefix_set:
                print(prefix, type, from_date, to_date, " **SKIPPED - ALREADY IN SET**", end="\n")
                list_stats['dup_skip']+=1
            else:
                active_prefix_set.add(prefix)
                print(prefix,type,from_date,to_date,end="\n")
                print("1100",prefix, sep=",", file=opfile)   #Output prefix to import file
        else:
            print(prefix, type, from_date, to_date," **SKIPPED - EXPIRED**", end="\n")
            list_stats['expire_skip']+=1
    print_stats(len(active_prefix_set),list_stats)
    return output_file


def print_stats(active_prefix_cnt,list_stats):
    print("")
    print("Prefix Lines Reviewed: ",'%20s' % list_stats['total'])
    print("Skipped Ignore List Count:",'%17s' % list_stats['list_skip'])
    print("Skipped Blue Shield Prefix Count:", '%10s' % list_stats['bs_skip'])
    print("Skipped Expired Prefix Count:", '%14s' % list_stats['expire_skip'])
    print("Skipped Duplicate Prefix Count:", '%12s' % list_stats['dup_skip'])
    print("Import Prefix Count: ", '%22s' % active_prefix_cnt)



def createConfig() -> None:
    config_object = ConfigParser()
    config_object['Default'] = {
    "input_dir": r'C:/Output/BlueCard/        #Directory where Blue Shield file is located',
    "cmp_id": '973        #CMP record ID to use for import to Epic (Record will be overridden)',
    "output_dir": r'C:/Output/BlueCard/        #Directory for output of import file',
    "prefix_skip": '        #Comma delimited list of prefixes to skip over',
    "expire_lag:": '52        #Number of weeks to continue using prefix after its expiration date'
    }

    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    print('A new config.ini file has been created in the root directory of this script. Please update the file prior to running the script again.')
    exit(-2)


def readConfig(config='Default'):
    if not exists('config.ini'):
        print("Creating config.ini file")
        createConfig()
    config_object = ConfigParser(inline_comment_prefixes="#")
    config_object.read("config.ini")
    config_object = config_object[config]
    return config_object

if __name__=="__main__":
    config = readConfig('Default')
    input_dir = config['input_dir']
    if len(input_dir)>0 and input_dir[-1] != "/":
        input_dir+="/"
    cmp_id = config['cmp_id']
    input_file = input('Filename:')
    if not input_file:
        print("No input file specified.")
        exit(0)
    input_fullpath_file=input_dir+input_file
    output_dir = config['output_dir']
    if len(output_dir)>0 and output_dir[-1] != "/":
        output_dir += "/"
    output_file = generateFile(input_fullpath_file,output_dir,cmp_id)
    if output_file:
        print("Epic Import File Generated At: ",output_file)
    else:
        print("Epic Import File failed to generate.")