import sys,os,math
#import numpy as np
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def generate_score_for_lig(pose):
    sp = pose.split()
    score = int(sp[8]) + 0.5*int(sp[5])- 2*int(sp[7])-2*(float(sp[17])-18)
    scored = pose.strip() + ' ' + str(score) + '\n'
    return scored


def sort_list_by_scores(PDBid,score_name):
    unsorted = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_sort.txt','r').readlines()
    score_col = len(unsorted[1].split())-1
    data = []
    for line in unsorted:
        line = line.split()
        data.append(line)
    data.sort(key=lambda s:(float(s[score_col])),reverse=True)
    return data

def filter_list(scored_list,score_name,PDBid):
    sorted_list = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_sorted.txt','a')
    j = 1
    for i in range(len(scored_list)):
        sp = scored_list[i]
        if (sp[9] == 'In-Stock') and  sp[10] == 'good' and sp[16] == '1' and (float(sp[4]) == -1 or float(sp[4])== 0):
            line = ' '.join(sp)+'\n'
            sorted_list.write(str(j)+' '+line)
            j += 1
            

def create_new_mol2(PDBid,score_name,argv[1]):
    path = os.getcwd()+'/'+score_name+'/'
    sorted_list = open(path+PDBid+'_ligand_sorted.txt','r').readlines()
    new_mol =  open(path+PDBid+'_sorted_poses.mol2','a')
    poses_f = Poses_parser.Poses_parser(os.getcwd()+'/'+PDBid+'/'+argv[1]+'/poses.mol2')
    for line in sorted_list:
        line = line.split()
        lig = poses_f.get_lig(int(line[2])-1)
        for l in lig:
            new_mol.write(l)

        
    
def main(name, argv):
    if (len(argv) != 2):
        print_usage(name)
        return

    PDB_list = open(os.getcwd()+'/'+argv[0],'r').readlines()
    score_name = argv[1]+'_scored'
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        print PDBid
        Lig_score = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_score.txt','r').readlines()
        outfile_local = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_sort.txt','a')
        for pose in Lig_score:
            outfile_local.write(generate_score_for_lig(pose))
        outfile_local.close()

        scored_list = sort_list_by_scores(PDBid,score_name)

        filter_list(scored_list,score_name,PDBid)
                
        create_new_mol2(PDBid,score_name,argv[1])

def print_usage(name):
    print "Usage : " + name + "<list_of_folders> <run.folder (library)>"


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

