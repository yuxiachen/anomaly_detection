from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import sys
import numpy

from detector import Detector


def main():
	#check if the run.sh is in correct form
	if len(sys.argv) != 4:
		print('Usage: <scrip_name> <file path to batch log> <file path to stream log>', 
			'<file path to output')
		return
	batch_log = sys.argv[1]
	stream_log = sys.argv[2]
	output_log = sys.argv[3]

	with open(batch_log, 'r') as batch:
		batch_lines = batch.readlines()

	# check the validity of batch_log
	assert len(batch_lines) >= 1, (
		'Unexpected number of batch lines: {}'.format(len(batch_lines)))

	# get the #degree and #tracked_number from the first line of input
	fl_json = json.loads(batch_lines[0])
	D = int(fl_json['D'])
	T = int(fl_json['T'])

	detector = Detector(batch_lines[1:], D, T)
	print('Detector initialized.')

	output = open(output_log, 'w')

	cnt = 0
	#read the record in stream_log line-in-line
	for cur_ln in open(stream_log, 'r'):
		cur_ln = cur_ln.strip()
		cnt += 1
		if not cur_ln:
			continue

		if cnt % 100 == 0:
			# print log every 10 lines
			print('Processed {} lines..'.format(cnt))

		info = json.loads(cur_ln)
		ret = detector.process_event(info)

		if ret is None:
			continue
			
		assert info['event_type'] == 'purchase', (
			'Unexpected event_type: {}'.format(info['event_type']))
		#if the input is a purchase record from the stream_log, get the return value
		#from the detector
		amount, mean, std = ret
		#check if the input purchase is an anomaly
		if numpy.abs(amount - mean) >= std * 3:
			output_ln = '{}, "mean": "{:.2f}", "sd": "{:.2f}"}}\n'.format(cur_ln[:-1], mean, std)
			output.write(output_ln)
			output.flush()

	output.close()


if __name__ == '__main__':
	main()




