# -*- encoding: UTF-8 -*-

# Standard imports
from dataclasses import dataclass
from shutil      import rmtree
from time        import time
from os          import path

# Third party imports
from github import Repository as GithubRepository
from git    import Repo

# Application imports
from app.services.github_service import GithubService

TEMP_FOLDER = "tmp"

@dataclass
class Repository(object):
    name       : str              = None
    remote_repo: GithubRepository = None
    local_repo : Repo             = None

    def __post_init__(self):
        if not self.name:
            self.name = str(int(time()))

    async def create(self) -> bool:
        self.remote_repo = await GithubService().create_repository(self.name, private=True)
        self.local_repo  = Repo.clone_from(self.remote_repo.ssh_url,
                                          "{dir}/{file}".format(dir=TEMP_FOLDER, file=self.name))

        return True

    async def delete(self) -> bool:
        if self.local_repo:
            rmtree(self.local_repo.working_dir)

        if self.remote_repo:
            self.remote_repo.delete()

        return True

    def config(self, *, name: str, email: str):
        self.local_repo.config_writer("repository").set_value("user", "name", name).release()
        self.local_repo.config_writer("repository").set_value("user", "email", email).release()

    def add(self, *, filename: str, content: str):
        with open(path.join(self.local_repo.working_dir, filename), "w") as file:
            file.write(content)

        self.local_repo.index.add(filename)

    def commit(self, message: str):
        self.local_repo.index.commit(message)

    async def push(self, remote: str = "origin"):
        self.local_repo.remote(name=remote).push()

    def commits(self):
        return self.remote_repo.get_commits()
