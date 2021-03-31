file = open("data/2018-Russia-election-data.csv", "r", encoding="utf-8")
text = ""
for line in file:
    if len(line.split(',')) == 5:
        last_char_index = line.rfind(',')
        new_line=(line[:last_char_index] + '' + line[last_char_index + 1:])
        text += new_line
    else:
        text+=(line)
x = open("data/2018-Russia-election-data.csv", "w", encoding="utf-8")
x.writelines(text)
x.close()
file.close()