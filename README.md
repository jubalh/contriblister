# contributions lister #

We will need python 2 and:

```
pip install sh
pip install gitpython
```

## Goal ##
Started as a simple cli program to list contributions.

Now the goal is to create a python script that will read a json file containing repo urls and emails, and create a simple HTML file with an overview of contributions.
Then users can easily embed this file in their website.
It's kind of similar to ohloh/openhub and github resume. But gives the user more control. ohloh doesnt trigger projects regularly and is annoying. github resume only scans projects on github. also the user can decide on the style using templates for the generated HTML file.
