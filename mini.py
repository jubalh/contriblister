from json import load
from sh import cd, git
from string import join, split
from subprocess import check_output
from os import mkdir
from os.path import isdir
from sys import exit

contributions = {}
unprocessable = []

if not isdir('/tmp/contriblister'):
    try:
        mkdir('/tmp/contriblister')
    except:
        print('ERROR: Could not create directory in /tmp. Exiting.')
        exit(1)

try:
    conf = open('repos.json', 'r')
except:
    print('ERROR: Could not open configuration file. Exiting.')
    exit(1)
else:
    try:
        data = load(conf)
    except:
        print('ERROR: Could not load data from configuration file. Exiting.')
        exit(1)
    else:
        for repo in data['repos']:
            repo_name = split(repo['url'], '/')[-1]

            if repo['vcs'] not in ['git']:
                print('ERROR: The VCS (%s) of repository %s is not supportet, yet. Continuing.' % (repo['vcs'], repo_name))
                unprocessable.append(repo_name)
                continue

            repo_dir = '/tmp/contriblister/%s' % repo_name

            try:
                if isdir(repo_dir):
                    cd(repo_dir)
                    git('pull')
                else:
                    git('clone', repo['url'], repo_dir)
                    cd(repo_dir)
            except:
                print('ERROR: Could not clone/pull repository %s. Continuing.' % repo_name)
                unprocessable.append(repo_name)
                continue

            try:
                log = check_output(['git', 'log', '--pretty=format:"%ae"', '--shortstat'], cwd=repo_dir).decode('utf-8')
            except:
                print('ERROR: Could not fetch log of repository %s. Continuing.' % repo_name)
                unprocessable.append(repo_name)
                continue
            else:
                contributions[repo_name] = 0

                for ma in data['mail-addresses']:
                    contributions[repo_name] += log.count(ma)

        try:
            html_file = open('/tmp/contriblister/contributions.html', 'w')
            html_file.truncate()
        except:
            print('ERROR: Could not open htlm-file. Skipping.')
        else:
            html_file.write('<table><thead><th># Commits</th><th>Name</th></thead><tbody>')

            for repo in contributions.iterkeys():
                html_file.write('<tr><td>%d</td><td>%s</td></tr>' % (contributions[repo], repo))

            html_file.write('</tbody></table>')
        finally:
            print('\n#Commits   Name')
            for repo in contributions.iterkeys():
                print('%8d   %s' % (contributions[repo], repo))
            if len(unprocessable) > 0:
                print('\nUnprocessable repositories: %s' % ', '.join(unprocessable))
            print('')
