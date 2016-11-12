import requests
from datetime import datetime
from getpass import getpass

def parse_date(d):
	return datetime.strptime(d,"%Y-%m-%dT%H:%M:%SZ")

class Turnaround(object):
	def __init__(self, owner, repo, user, password):
		url = 'https://api.github.com/repos/{}/{}/issues?state=closed'
		self.pulls = requests.get(
			url.format(owner,repo),
			auth=(user,password)
		).json()

	def collect_turnaround_times_by_user(self):
		tabula = {}
		for pull in self.pulls:
			if pull['closed_at']:
				login = pull['user']['login']
				turnaround = parse_date(pull['closed_at']) \
					- parse_date(pull['created_at'])
				tabula[login] = tabula.get(login,[]) + [
					turnaround.total_seconds() / (3600 * 24)
				]
		return tabula

	def report(self):
		tabula = self.collect_turnaround_times_by_user()
		print('{:<15} {:3} {:3} {:3}'.format('user','pulls', 'avg (days)', 'max (days)'))
		for user, times in tabula.items():
			avgt = round(sum(times)/len(times))
			maxt = round(max(times))

			print('{:<15} {:5} {:10} {:10}'.format(user,len(times), avgt, maxt))

def main():
	Turnaround(
		input("Repo owner:"),
		input("Repo name:"),
		input("Your username:"),
		getpass("Password:")
	).report()

if __name__ == '__main__':
	main()