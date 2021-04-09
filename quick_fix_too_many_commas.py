"""
Fixes the extra commas in some of the regions in the Russian data.
"""

file = open("data/2018-Russia-election-data.csv", "r", encoding="utf-8")
TEXT = ""
for line in file:
    if len(line.split(",")) == 5:
        last_char_index = line.rfind(",")
        new_line = line[:last_char_index] + "" + line[last_char_index + 1:]
        TEXT += new_line
    else:
        TEXT += line
file.close()
x = open("data/2018-Russia-election-data.csv", "w", encoding="utf-8")
x.writelines(TEXT)
x.close()
