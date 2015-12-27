# -*- coding: utf-8 -*-

import os
import json
import sh
import subprocess
from jinja2 import Environment, FileSystemLoader, Template

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

def create_contributions_data(json_data):
    total_contributions = 0
    contributions_list = []
    contrib_dict = {}

    for repo in json_data["repos"]:
        print ("Processing: ", repo["name"])
        wd = repos_path + "/" + repo["name"]

        for ea in json_data["emails"]:
            print (" Checking for: " + ea)

            output = subprocess.check_output(['git', 'log', '--pretty=format:"%ae%n%s"', "--shortstat", "--author=" + ea], cwd=wd)
            output = output.decode("utf-8")

            if len(output) > 0:
                commits = output.split("\n\n")

                print (" %d contributions found" %len(commits))

                for commit in commits:
                    lines = commit.splitlines()
                    contrib_dict = {
                        "email": ea,
                        "repo": repo["name"],
                        "summary": lines[1]
                    }
                    contributions_list.append(contrib_dict)
    return contributions_list


# START
with open("repos.json") as data_file:
    data = json.load(data_file)

working_directory = os.getcwd()
repos_path = os.path.join(working_directory, 'repos')
if not os.path.isdir(repos_path):
    os.mkdir(repos_path)

get_newest_repos(data)

contrib_list = create_contributions_data(data)

print ("\nTotal contributions: ", len(contrib_list))

#jinja_env = Environment(loader = FileSystemLoader(working_directory + '/templates'))
#template = jinja_env.get_template('t.html')

template_file = open(os.path.join(working_directory, 'templates', 't2.html'))
template = Template(template_file.read())
output = template.render(contributions=contrib_list)
template_file.close()

#print(output)

output_file = open('output.html','w')
output_file.write(output)
output_file.close()
print ("HTML file written to: output.html")
