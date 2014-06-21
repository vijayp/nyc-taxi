#!/usr/bin/python                                                                                                                 
#medallion,hack_license,vendor_id,rate_code,store_and_fwd_flag,pickup_datetime,dropoff_datetime,passenger_count,trip_time_in_secs 
#89D227B655E5C82AECF13C3F540D4CF4,BA96DE419E711691B9445D6A6307C170,CMT,1,N,2013-01-01 15:11:48,2013-01-01 15:18:10,4,382,1.00,-73\
.978165,40.757977,-73.989838,40.751171                                                                                            

from mrjob.job import MRJob
from mrjob.job import MRStep
import re
import md5


class MRHackLicences(MRJob):
    def mapper_init(self):
        self.cksum_number_map = {}
        for i in range(int(6e5)):
            self.cksum_number_map[md5.md5('%d' % i).hexdigest().upper()] = i
    def mapper(self, _, line):
        data = line.split(',')
        hack_no = self.cksum_number_map.get(data[1])
        if hack_no:
            yield(str(hack_no), None)
    def combiner(self, key, value):
        yield(key, None)
    def reducer(self, key, value):
        yield(key, None)

if __name__ == '__main__':
    MRHackLicences.run()
