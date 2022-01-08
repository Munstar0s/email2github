# -*- encoding: UTF-8 -*-

# Standard imports
import csv

from os          import path, makedirs
from typing      import List
from dataclasses import dataclass, field

# Third party imports
from rich.table import Table

# Application imports
from app.logger             import console

from app.installer      import Installer
from app.updater        import Updater

from app.entities.email import Email

from app.services.github_service import GithubService

from app.techniques.fake_commits import FakeCommits
from app.techniques.users_search import UsersSearch

@dataclass
class Resolver:
    output    : str
    quiet     : bool
    techniques: List = field(default_factory=list)

    async def run(self, emails: List):
        installer     = Installer()
        updater       = Updater()

        console.quiet = self.quiet

        if await updater.check_for_update():
            console.print("A new version is available. To update, run `python email2github update`")

        if not await installer.check():
            await installer.run()

            if not await installer.check():
                console.print("[red]Installation fail")
                exit(1)

        users_search_technique = UsersSearch()
        fake_commits_technique = FakeCommits()

        self.techniques.append(users_search_technique)
        self.techniques.append(fake_commits_technique)

        users_search_technique.set_next(fake_commits_technique)

        with console.status("Loading email addresses…") as status:
            if not (emails := Email.load_from_file(emails) if path.isfile(emails) else Email.load_from_string(emails)):
                console.print("[red]  No correct email address has been set. Please check your input.")
                exit(1)

            console.print("{:<40s} {:<10s}".format("Loading email addresses:", "done"))

        await users_search_technique.resolve(emails)

        if self.output:
            with console.status("Saving results in a file…"):
                directory = path.dirname(self.output)

                if directory and not path.isdir(directory) and makedirs(directory) and not path.isdir(directory):
                    makedirs(directory)

                with open(self.output, "w") as file:
                    writer = csv.writer(file)
                    writer.writerow(emails[0].as_headers())

                    for email in emails:
                        writer.writerow(email.to_list())

            console.print("{:<40s} {:<10s}".format("Saving results in a file:", "done"))

        console.print("")
        console.print("Done!")
        console.print("")

        table = Table()

        [table.add_column(header)        for header in emails[0].as_headers()]
        [table.add_row(*email.to_list()) for email in emails]

        console.print(table)
        console.print("")

    async def stop(self):
        [await technique.clean() for technique in self.techniques]
