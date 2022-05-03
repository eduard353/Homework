def get_top_performers(file_path, number_of_top_students=5):
    students_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines()[1:]:
            l = line.replace('\n', '').split(sep=',')
            l.reverse()
            l[0] = float(l[0])
            students_list.append(tuple(l))
    students_list.sort(reverse=True)

    return [student[2] for student in students_list[:number_of_top_students]]


def desc_by_age(file_path):
    sort_list = []
    with open(file_path, 'r') as f:
        headers = f.readline()
        for line in f.readlines()[1:]:
            l = line.split(sep=',')
            l[1] = int(l[1])
            sort_list.append(tuple([l[1], l[0], l[2]]))
    sort_list.sort(reverse=True)

    new_file_path = '/'.join(file_path.split('/')[:-1]) + '/desc_by_age_' + file_path.split('/')[-1]
    with open(new_file_path, 'w') as f:
        f.write(headers)
        for line in sort_list:
            f.write(line[1] + ',' + str(line[0]) + ',' + line[2])


print(get_top_performers("../data/students.csv"))
desc_by_age("../data/students.csv")
