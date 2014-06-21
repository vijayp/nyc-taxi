#!/usr/bin/python                                                                                                                 
#medallion,hack_license,vendor_id,rate_code,store_and_fwd_flag,pickup_datetime,dropoff_datetime,passenger_count,trip_time_in_secs 
#89D227B655E5C82AECF13C3F540D4CF4,BA96DE419E711691B9445D6A6307C170,CMT,1,N,2013-01-01 15:11:48,2013-01-01 15:18:10,4,382,1.00,-73\
.978165,40.757977,-73.989838,40.751171                                                                                            

from mrjob.job import MRJob
from mrjob.job import MRStep
import re
import md5

def baseN(num,b,numerals="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

class MRMedallionNumbers(MRJob):

    def mapper_init(self):
        self.cksum_number_map = {}
        def add(s):
            self.cksum_number_map[md5.md5(s).hexdigest().upper()] = s
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
            
    def mapper(self, _, line):
        data = line.split(',')
        hack_no = self.cksum_number_map.get(data[0])
        if hack_no:
            yield(str(hack_no), None)
    def combiner(self, key, value):
        yield(key, None)
    def reducer(self, key, value):
        yield(key, None)

if __name__ == '__main__':
    MRMedallionNumbers.run()
