<h1 align="center">email2github</h1>
<p align="center">Identify Github accounts associated with email addresses</p>
<p align="center">
  <a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.8-green.svg" /></a>
  <a target="_blank" href="LICENSE" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>
  <a target="_blank" href="https://github.com/s0md3v/Zen/releases" title="Latest release"><img src="https://img.shields.io/github/v/release/h51un6/email2github.svg" /></a>
</p>

## Installation

```
# Clone the repo
$ git clone https://github.com/h51un6/email2github.git

# Change the working directory
$ cd email2github

# Create and activate a virtual environment (optional step)
$ python3 -m venv venv
$ . venv/bin/activate

# Install the requirements
$ pip install -r requirements.txt
```

This tool uses the Github API. Please create a personal access token by following [this documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). The scope of the token must include "repo" and "delete_repo", as the tool will create and delete fake private repositories.

## Usage

```
$ python email2github search --help
Usage: python -m email2github search [OPTIONS] EMAILS

  Search email addresses on Github

  This command try to resolve email addresses to Github accounts with various
  techniques, from the most simple to the most intrusive.

  Email addresses could be set from a file or from a comma-separated list.

Options:
  -o, --output PATH  Save the results as CSV in a file
  -q, --quiet        Suppress helping messages
  --help             Show this message and exit.
```

## Examples

| Description             | Command                                    |
|-------------------------|--------------------------------------------|
| Search a single email   | `python email2github search EMAIL`         |
| Search from a file      | `python email2github search FILEPATH`      |
| Search a list of emails | `python email2github search EMAIL1,EMAIL2` |


## Techniques

| Technique           | Description                                                       | Scope        |
|---------------------|-------------------------------------------------------------------|--------------|
| Search in emails    | Use the Github's users search endpoint to search account by email | Public email |
| Create fake commits | Create fake commits with arbitrary email. GitHub automatically resolves the emails to a GitHub accounts associated with them. | Public, private, primary and secondary email |

## Inspiration

Thanks to the antnks' [enumerate Github users](https://github.com/antnks/enumerate-github-users) POC.
