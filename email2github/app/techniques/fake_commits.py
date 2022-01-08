# -*- encoding: UTF-8 -*-

# Standard imports
from dataclasses import dataclass
from typing      import List

# Third party imports

# Application imports
from app.logger                          import console
from app.techniques.abstract_handler import AbstractHandler
from app.entities.repository         import Repository

class FakeCommits(AbstractHandler):
    """This technique creates a temporary private Git repository, add fake commits
    with arbitrary email addresses and it push them on a remote repository.

    On Github, emails are automatically resolved to Github accounts associated with them.
    """

    repository: Repository = None

    async def resolve(self, emails: List) -> List:
        self.repository = Repository()

        console.print("Spoofing email addresses…")
        await self.repository.create()
        console.print("{:<40s} {:<10s}".format("Initializing a fake Git repository:", "done"))

        with console.status("Spoofing email addresses…") as status:
            for email in emails:
                self.repository.config(name=email.address, email=email.address)
                self.repository.add(filename="{}.txt".format(email.address), content=email.address)

                self.repository.commit(email.address)

            console.print("{:<40s} {:<10s}".format("Creating fake commits:", "done"))

        await self.repository.push()
        console.print("{:<40s} {:<10s}".format("Pushing commits to Github:", "done"))

        with console.status("Spoofing email addresses…") as status:
            for commit in self.repository.commits():
                if not commit.author:
                    continue

                for email in emails:
                    if commit.commit.message == email.address:
                        email.user = commit.author
                        break

            console.print("{:<40s} {:<10s}".format("Resolving email addresses:", "done"))

        await self.clean()

        if need_to_be_resolved := list(filter(lambda email: not email.resolved(), emails)):
            return await super().resolve(need_to_be_resolved)

    async def clean(self):
        await self.repository.delete()
        console.print("{:<40s} {:<10s}".format("Cleaning up the fake repository:", "done"))
