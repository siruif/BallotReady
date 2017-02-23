import csv
from cookCountyCandidates import create_candidate_party_dict

IDENTITY = 3
CANDIDATE = 12
CITY = 14
ZIP = 34

PARTY_OF_INTEREST = "REP"
#PARTY_OF_INTEREST = "DEM"

SINGLE_CANDIDATE_RACE = {"Daniel William Lipinski", "Luis V. Gutierrez", "Antonio ''Tony'' Munoz", \
"Omar Aquino", "Kimberly A. Lightford", "Patricia Van Pelt", "Heather A. Steans", \
"Ira I. Silverstein", "John G. Mulroe", "Martin A. Sandoval", "Kwame Raoul", \
"Emil Jones III", "Jacqueline ''Jacqui'' Collins", "Donne E. Trotter", \
"Michael E. Hastings", "Iris Y. Martinez", "Toi W. Hutchinson", "Christine Radogno", \
"Daniel J. Burke", "Theresa Mah", "Luis Arroyo", "Cynthia Soto", "Juliana Strantton", \
"Sonya Marie Harper", "Emanuel ''Chris'' Welch", "La Shawn K. Ford", "Arthur Turner", \
"Gregory Harris", "Lou Lang", "Laura Fine", "Robert Martwick", "Silvana Tabares", \
"Michael J. Madigan", "Michael J. Zalewski", "Barbara Flynn Currie", "Christian L. Mitchell", \
"Monique D. Davis", "Robert ''Bob'' Rita", "Thaddeus Jones", "William ''Will'' Davis", \
"Mary E. Flowers", "Andre Thapedi", "Marcus C. Evans, Jr.", "Elgie R. Sims, Jr.", \
"Kelly M. Burke", "Margo McDermed", "Al Riley", "Will Guzzardi", "Jamie M. Andrade, Jr.", \
"Anna Moeller", "Patricia R. ''Patti'' Bellock", "Mike Fortner", "Nick Sauer", "David McSweeney", \
"David Harris", "Tom Morrison", "Elaine Nekritz", "Camille Lilly", "Anthony DeLuca", \
"Jim Durkin", "Karen A. Yarbrough", "Michael Cabonargi", "Eileen O'Neill Burke", \
"Bertina E. Lampkin", "John Fitzgerald Lyke, Jr.", "Rossana Patricia Fernandez", \
"Alison C. Conlon", "Aleksandra ''Alex'' Gillespie", "Carolyn J. Gallagher", \
"Mary Kathleen McHugh", "Brendan A. O'Brien", "Maureen O'Donoghue Hannon", \
"Susana L. Ortiz", "Daniel Patrick Duffy", "Patrick Joseph Powers", "Jesse Outlaw", \
"Rhonda Crawford", "D. Renee Jackson", "Edward J. King", "Leonard Murray", \
"Fredderena M. Lyle", "Daryl Jones", "Eulalia De La Rosa", "Richard C. Cooke", \
"Anna Loftus", "Marianne Jackson", "Patricia 'Pat' S. Spratt", "Jerry Esrig", \
"Eve Marie Reilly", "Catherine Ann Schneider", "William B. Sullivan", \
"Matthew Link"}

def construct_zip_sets(county):
	zip_set = set()
	with open("data/CookCountyZip.csv") as csvfile:
		csvfile.readline()
		spamreader = csv.reader(csvfile, delimiter = ',')
		for row in spamreader:
			try:
				zipcode = int(row[0])
				city_name = row[1]
				county_name = row[2]
				if county_name == county:
					zip_set.add(zipcode)
			except:
				continue

	return zip_set

def construct_chicago_users():
	chicago_users = set()
	zip_set = construct_zip_sets("Cook")
	#print("There are", len(zip_set), "zip codes in Cook County")
	with open("data/with_header.csv") as csvfile:
		csvfile.readline()
		#identity idx 3
		#candidate idx 12
		spamreader = csv.reader(csvfile, delimiter = ',')
		for row in spamreader:
			try:
				identity = row[IDENTITY]
				city = row[CITY].lower()
				zipcode = int(row[ZIP])
				candidate = row[CANDIDATE]
				if zipcode in zip_set:
					chicago_users.add(identity)
				
			except:
				continue
	
	return chicago_users

def build_user_saves_from_raw(multiple_candidates_race):
	user_dict = dict()
	candidate_party_dict = create_candidate_party_dict()
	chicago_users = construct_chicago_users()
	print("there are ", len(chicago_users), " users in chicago")
	#key is candidate name and value is party

	with open("data/with_header.csv") as csvfile:
		csvfile.readline()
		#identity idx 3
		#candidate idx 12
		spamreader = csv.reader(csvfile, delimiter = ',')
		for row in spamreader:
			try:
				identity = row[IDENTITY]
				candidate = row[CANDIDATE]
				city = row[CITY].lower()
				
				if (identity != "") and (candidate != "") and (identity in chicago_users)\
				and (candidate in candidate_party_dict):

					if multiple_candidates_race and candidate in SINGLE_CANDIDATE_RACE:
						continue

					party = candidate_party_dict[candidate]
						
					if identity not in user_dict:
						user_dict[identity] = dict()

					if party in user_dict[identity]:
						user_dict[identity][party] += 1
					else:
						user_dict[identity][party] = 1

			except:
				continue
	#print(user_dict)
	total_saves = 0
	for user in user_dict:
		for party in user_dict[user]:
			total_saves += user_dict[user][party]
	print("Total saves:", total_saves)
	print(len(user_dict))
	print(total_saves/len(user_dict))

	return user_dict

def build_partisan_breakdown_by_user(multiple_candidates_race):
	user_dict = build_user_saves_from_raw(multiple_candidates_race)
	
	#{u1:{"DEM":8, 'GRN': 12, 'LIB': 9, 'REP': 14}, u2:{"DEM":9}}
	
	partisan_breakdown_by_user = dict()

	for user in user_dict:
		total_saves = 0
		for party in user_dict[user]:
			total_saves += user_dict[user][party]
		
		if total_saves != 0:
			partisan_breakdown_by_user[user] = dict()
		
			interest_percent = round((user_dict[user].get(PARTY_OF_INTEREST,0)/total_saves),1)
			partisan_breakdown_by_user[user][PARTY_OF_INTEREST] = interest_percent
			#partisan_breakdown_by_user[user]["OTHERS"] = 1 - interest_percent
			partisan_breakdown_by_user[user]["NO_RACES"] = total_saves
	#print(partisan_breakdown_by_user)
	return partisan_breakdown_by_user

def build_partisan_breakdown(multiple_candidates_race):
	partisan_breakdown_by_user = build_partisan_breakdown_by_user(multiple_candidates_race)
	#{'u1': {'DEM': 1.0, 'GRN': 0.0}, "u1": {"DEM": 0.8, "GRN": 0.2}}

	breakdown_dict = dict()

	for user in partisan_breakdown_by_user:
		interest_percent = partisan_breakdown_by_user[user][PARTY_OF_INTEREST]
		total_saves = partisan_breakdown_by_user[user]["NO_RACES"]
		if total_saves >= 3:
			total_saves = "More than three"
		
		if interest_percent in breakdown_dict:
			breakdown_dict[interest_percent]["COUNT"] += 1
			if total_saves in breakdown_dict[interest_percent]["NO_RACES"]:
				breakdown_dict[interest_percent]["NO_RACES"][total_saves] += 1
			else:
				breakdown_dict[interest_percent]["NO_RACES"][total_saves] = 1

		else:
			breakdown_dict[interest_percent] = dict()
			breakdown_dict[interest_percent]["COUNT"] = 1
			breakdown_dict[interest_percent]["NO_RACES"] = dict()
			breakdown_dict[interest_percent]["NO_RACES"][total_saves] = 1
	print(breakdown_dict)
		
if __name__ == "__main__":
	#construct_chicago_users()
	build_partisan_breakdown(multiple_candidates_race = True)
	#construct_zip_sets("Cook")


#for each user, indicator varialble of all saves are from the same party
