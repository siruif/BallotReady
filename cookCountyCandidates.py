import csv

PARTIES_OF_INTEREST = {"REP":0, "GRN":0, "IND":0, "DEM":0, "LIB":0}
SINGLE_CANDIDATES = ["Daniel William Lipinski", ]

def create_candidate_party_dict():
	candidate_party_dict = dict()
	#{"A": "GRN", "B": "DEM"}
	with open("data/Election_Results_Cook_County.csv") as csvfile:
		csvfile.readline() #skip header
		reader = csv.reader(csvfile, delimiter=',')
		new_race = False
		for row in reader:
			#print(row)
			if not is_white_line(row) and not is_header_line(row) and not is_invalid_line(row):
				candidate_name = row[0]
				party = row[1]
				if party in PARTIES_OF_INTEREST:
					candidate_party_dict[candidate_name] = party
					PARTIES_OF_INTEREST[party] += 1
	#print(candidate_party_dict)
	return candidate_party_dict		
	

def is_white_line(row):
	return row[0] == "" and row[1] == "" and row[2] == ""

def is_header_line(row):
	return (row[1].lower() == "vote for 1" or row[1].lower() == "vote for 2" or \
		row[1].lower() == "vote for 3" or row[1].lower() == "vote for") or (row[0].lower() == "candidate" and \
	row[1].lower() == "party")

def is_invalid_line(row):
	return (row[0].lower() == "yes" or row[0].lower() == "no")


if __name__ == "__main__":
	create_candidate_party_dict()