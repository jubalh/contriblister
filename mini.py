import os
import json
import sh
import subprocess

def get_newest_repos():
    for repo in data["repos"]:
        if os.path.isdir(repo["name"]):
            print("Updating " + repo["name"])
            sh.cd(startpath + "/" + repo["name"])
            sh.git("pull")
            sh.cd(startpath)
        else:
            print("Cloning " + repo["name"])
            sh.git("clone", repo["url"], repo["name"])
    print ""

def search_occurence(buf, searchterm, pos):
    contributions = 0
    pos = buf.find(searchterm, pos)
    if pos >= 0:
        pos2 = buf.find(" ", pos)
        if pos2 >= 0:
            contributions += 1
            contributions += search_occurence(buf, searchterm, pos2)
            return contributions
    return 0

def count_contributions():
    total_contributions = 0
    for repo in data["repos"]:
        print "Processing: ", repo["name"]
        wd = startpath + "/" + repo["name"]

        output = subprocess.check_output(['git', 'log', '--pretty=format:"%ae - %s"', "--shortstat"], cwd=wd)
        output = output.decode("utf-8")

        for ea in data["emails"]:
            print (" Checking for: " + ea)
            contributions = search_occurence(output, ea, 0)
            print (" %d contributions found" %contributions)
            total_contributions += contributions
    return total_contributions


with open("repos.json") as data_file:
    data = json.load(data_file)

startpath = os.getcwd()

get_newest_repos()

contributions = count_contributions()

print "\nTotal contributions: ", contributions
