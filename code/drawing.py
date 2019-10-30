# -*- coding: utf-8 -*-
import random
import sys
import name_extractor

# Assumtion: no duplicate names in the list
def draw(name_list):
	n_prize = 5
	n_total = len(name_list)

	if n_total < n_prize:
		print("The total number of participants is less than the number of prizes to draw. Exit.")
		sys.exit(1)

	print("********************************")
	print("\n\n\n***【荒野小包】我开箱，你抽奖！***\n*** 获奖的是观众是---- ".decode('utf-8').encode('utf-8'))
	raw_input("")
	random_numbers = random.sample(range(0, n_total), n_prize)
	for i in random_numbers:
		print("  " + name_list[i])
		
	print("*** 恭喜以上获奖者！小包会B站私信大家的，请注意查收！***".decode('utf-8').encode('utf-8'))

def main():
	name_list = name_extractor.get_final_names()
	draw(name_list)

if __name__ == "__main__":
	main()