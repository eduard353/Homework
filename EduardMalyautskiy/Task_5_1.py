with open("../data/unsorted_names.txt", 'r') as rf:
    names = sorted(rf.readlines())
with open("../data/sorted_names.txt", 'w') as wf:
    wf.writelines(names)
