# -*- encoding: UTF-8 -*-

# Standard imports
from os          import path, getcwd
from dataclasses import dataclass

# Third party imports
from git     import Repo, TagReference
from git.exc import GitCommandError

# Application imports
from app.logger import console

VERSION_FILE = "VERSION"
ROOT_DIR     = getcwd()

@dataclass
class Version:
    name : str
    tag  : TagReference = None
    major: int          = 0
    minor: int          = 0
    micro: int          = 0

    def __post_init__(self):
        t = self.name.split(".")

        if 0 < len(t):
            self.major = t[0]

        if 1 < len(t):
            self.minor = t[1]

        if 2 < len(t):
            self.micro = t[2]

    def __eq__(self, other):
        return ((self.major, self.minor, self.micro) == (other.major, other.minor, other.micro))

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        return ((self.major, self.minor, self.micro) <= (other.major, other.minor, other.micro))

    def __lt__(self, other):
        return ((self.major, self.minor, self.micro) < (other.major, other.minor, other.micro))

    def __gt__(self, other):
        return ((self.major, self.minor, self.micro) > (other.major, other.minor, other.micro))

    def __ge__(self, other):
        return ((self.major, self.minor, self.micro) >= (other.major, other.minor, other.micro))

    def __repr__(self):
        return "%s.%s.%s" % (self.major, self.minor, self.micro)

@dataclass
class Updater:
    repository     : Repo    = None
    current_version: Version = None
    latest_version : Version = None

    def __post_init__(self):
        if not path.isdir(path.abspath(path.join(ROOT_DIR, ".git"))):
            return False

        self.repository = Repo.init(".")

    async def check_for_update(self) -> bool:
        if not self.repository:
            return False

        with open(path.abspath(path.join(ROOT_DIR, VERSION_FILE))) as file:
            self.current_version = Version(file.read().strip())

        try:
            [remote.fetch() for remote in self.repository.remotes]
        except GitCommandError:
            console.print("[red]Unable to reach the remote repository")
            exit(1)

        tags                = sorted(self.repository.tags, key=lambda t: t.commit.committed_datetime)
        newest_tag          = tags[-1]
        self.latest_version = Version(newest_tag.name, newest_tag)

        return self.current_version < self.latest_version

    async def download(self):
        if not self.repository:
            console.print("Unable to update: this is not a Git repository")
            exit(1)

        console.print("Checking for update…")

        if not await self.check_for_update():
            console.print("Done! This tool is up to date :)")
            exit(0)

        console.print("Downloading the new release…")

        for remote in self.repository.remotes:
            remote.pull()

        self.repository.git.checkout(self.latest_version.tag.commit)
        console.print("")
        console.print("Done! This tool is now up to date!")

    async def stop(self):
        pass
