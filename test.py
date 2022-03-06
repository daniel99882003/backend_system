
teacher_list = [{'tid': 1, 'tname': '黃大狗', 'cname': '天才4班'},
 {'tid': 1, 'tname': '黃大狗', 'cname': '天才3班'},
 {'tid': 1, 'tname': '黃大狗', 'cname': '天才2班'},
 {'tid': 1, 'tname': '黃大狗', 'cname': '天才1班'},
 {'tid': 2, 'tname': '李小貓', 'cname': '天才3班'},
 {'tid': 2, 'tname': '李小貓', 'cname': '天才2班'},
 {'tid': 3, 'tname': '豬胖胖', 'cname': '天才4班'},
 {'tid': 4, 'tname': '掐掐丟', 'cname': '天才11班'}]

result = {}

for row in teacher_list:
    tid = row['tid']
    if tid in result:
        result[tid]['cname'].append(row['cname'])
    else:
        result[tid] = {'tid': row['tid'], 'tname': row['tname'], 'cname': [row['cname'], ]}
print(result)
