# -*- coding: utf-8 -*-

import os
import json
import sh
import subprocess
#from collections import namedtuple
from jinja2 import Environment, FileSystemLoader, Template

#Contribution = namedtuple('Contribution', ['email', 'insertions', 'deletions'])

def get_newest_repos(json_data):
    for repo in json_data["repos"]:
        sh.cd(repos_path)
        current_repo_path = os.path.join(repos_path, repo["name"])

        if os.path.isdir(current_repo_path):
            print("Updating " + repo["name"])
            sh.cd(current_repo_path)
            sh.git("pull")
        else:
            print("Cloning " + repo["name"])
            sh.git("clone", repo["url"], repo["name"])
    sh.cd(working_directory)
    print ("")


def count_overall_contributions(json_data):
    total_contributions = 0
    for repo in json_data["repos"]:
        print ("Processing: ", repo["name"])
        wd = repos_path + "/" + repo["name"]

        output = subprocess.check_output(['git', 'log', '--pretty=format:"%ae - %s"', "--shortstat"], cwd=wd)
        output = output.decode("utf-8")

        for ea in json_data["emails"]:
            print (" Checking for: " + ea)
            contributions = str.count(output, ea)
            print (" %d contributions found" %contributions)
            total_contributions += contributions
    return total_contributions

with open("repos.json") as data_file:
    data = json.load(data_file)


working_directory = os.getcwd()
repos_path = os.path.join(working_directory, 'repos')
if not os.path.isdir(repos_path):
    os.mkdir(repos_path)

get_newest_repos(data)

contributions_count = count_overall_contributions(data)

#jinja_env = Environment(loader = FileSystemLoader(working_directory + '/templates'))
#template = jinja_env.get_template('t.html')
template_file = open(os.path.join(working_directory, 'templates', 't.html'))
template = Template(template_file.read())
output = template.render(a_var=contributions_count)
template_file.close()
print(output)

output_file = open('output.html','w')
output_file.write(output)
output_file.close()

print ("\nTotal contributions: ", contributions_count)
