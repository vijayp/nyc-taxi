import json
import md5

#make hashes
def baseN(num,b,numerals="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

cksum_number_map = {}
def add(s):
    cksum_number_map[md5.md5(s).hexdigest().upper()] = s
# http://www.nyc.gov/html/tlc_medallion_info/html/tlc_lookup.shtml
#The correct formats are:
#one number, one letter, two numbers. For example: 5X55
#two letters, three numbers. For example: XX555
#three letters, three numbers. For example: XXX555
for i in range(1000):
    for j in range(26**3):
        istr = str(i)
        alpha_string = baseN(j,26)
        if len(alpha_string) == 1:
            add(istr[0] + alpha_string + istr[1:])
        else:
            add(alpha_string + istr)
for i in range(int(6e6)):
    cksum_number_map[md5.md5('%0.6d' % i).hexdigest().upper()] = str(i)
for i in range(5000000, 5900000):
    cksum_number_map[md5.md5('%0.7d' % i).hexdigest().upper()] = str(i)


json.dump(cksum_number_map, open('rainbow.json', 'w'))
