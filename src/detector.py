from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import numpy

from social_network import SocialNetwork

class Detector(object):
	def __init__(self, json_line, degree, num_tracked):
		self.degree = degree
		self.num_tracked = num_tracked
		self.counter = 0
		self.social_network = SocialNetwork()
		# initial the detector with the input batch_log
		for ln in json_line:
			info = json.loads(ln)
			self.process_event(info, is_init=True)

	def process_event(self, info, is_init=False):
		# use the counter to stamp the input order of the events
		self.counter = self.counter + 1
		event_type = info['event_type']
		# update social network if event type is befriend or unfriend
		if event_type in ['befriend', 'unfriend']:
			id1 = info['id1']
			id2 = info['id2']
			self.social_network.update_network(event_type == 'befriend', id1, id2)
			return None
		# update user map and purchase history if event type is purchase
		elif event_type == 'purchase':
			user_id = info['id']
			self.social_network.add_user(user_id)
			timestamp = info['timestamp']
			amount = float(info['amount'])
			self.social_network.update_purchase(
				user_id, timestamp, amount, self.counter, self.num_tracked)
			if is_init:
				return None

			# get all the purchase history of the social network of user with 'user_id'
			purchase_history = self.social_network.get_tracked_purchases(
				user_id, self.degree, self.num_tracked)
			
			if len(purchase_history) <= 2:
				return None
			# calculate the mean and standard deviation by numpy
			mean = numpy.mean(purchase_history)
			std = numpy.std(purchase_history)

			return (amount, mean, std)
		else:
			raise ValueError('Unexpected event_type: {}'.format(event_type))






