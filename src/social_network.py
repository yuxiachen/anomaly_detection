from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import heapq
import json

from collections import deque


class SocialNetwork(object):
	'''
	define the class of social network
	'''
	def __init__(self):
		# creat a dictionary between id and users
		self.users = {}

	def add_user(self, user_id):
		if user_id in self.users:
			return
		self.users[user_id] = Users(user_id)

	def update_network(self, befriend, id1, id2):
		self.add_user(id1)
		self.add_user(id2)
		self.users[id1].update_friend(befriend, id2)
		self.users[id2].update_friend(befriend, id1)

	def update_purchase(self, user_id, timestamp, amount, counter, num_tracked):
		self.users[user_id].add_purchase(timestamp, amount, counter, num_tracked)

	def get_tracked_purchases(self, user_id, degree, num_tracked):
		'''
		get num_tracked of purchase history within the user's network defined by degree
		'''
		id_in_degree = set([user_id])
		boundary = set([user_id])

		for i in range(degree):
			new_boundary = set()
			for boundary_id in boundary:
				user_in_boundary = self.users[boundary_id]
				for friend_id in user_in_boundary.friends:
					if friend_id in id_in_degree:
						continue
					id_in_degree.add(friend_id)
					new_boundary.add(friend_id)
			boundary = new_boundary

		id_in_degree.remove(user_id)
		
		# O(num_tracked*k) algorithm for getting the result
		k = len(id_in_degree)
		purchases_list = []
		ptr_list = []
		for user_id in id_in_degree:
			cur_purchases = list(self.users[user_id].purchases)
			purchases_list.append(cur_purchases)
			ptr_list.append(len(cur_purchases) - 1)

		
		ans_list = []
		for i in range(num_tracked):
			latest_j = None
			latest_purchase = None
			for j in range(k):
				if ptr_list[j] < 0:
					continue
				if latest_purchase is None or (
						purchases_list[j][ptr_list[j]][0:2] > latest_purchase[0:2]):
					latest_purchase = purchases_list[j][ptr_list[j]]
					latest_j = j
			if latest_j is None:
				break

			ans_list.append(latest_purchase[2])
			ptr_list[latest_j] = ptr_list[latest_j] - 1
		
		return ans_list


class Users(object):
	'''
	define the Users Class
	'''
	def __init__(self, user_id):
		self.id = user_id
		self.friends = set()
		self.purchases = deque()
	
	def update_friend(self, befriend, user_id):
		if befriend:
			self.friends.add(user_id)
		elif user_id in self.friends:
			self.friends.remove(user_id)		
	
	def add_purchase(self, timestamp, amount, counter, num_tracked):
		'''
		Make sure the purchase is ordered with smallest timestamp at left.
		'''
		if len(self.purchases) >= num_tracked:
			self.purchases.popleft()
		self.purchases.append((timestamp, counter, amount))

