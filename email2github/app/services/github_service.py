# -*- encoding: UTF-8 -*-

# Standard imports
from os          import path, makedirs
from dataclasses import dataclass

# Third party imports
import json

from github                 import Github, AuthenticatedUser
from github.GithubException import BadCredentialsException
from rich.prompt            import Prompt

# Application imports
from app.entities.email import Email
from app.logger             import console

# Singleton

AUTH_FILE         = "tmp/auth.json"
LOGIN_AUTH_METHOD = "login"
TOKEN_AUTH_METHOD = "token"

@dataclass
class GithubService:
    github: Github            = None
    user  : AuthenticatedUser = None

    def configurated(self):
        return path.isfile(AUTH_FILE)

    def authenticated(self):
        return bool(self.user)

    async def configure(self) -> bool:
        directory = path.dirname(AUTH_FILE)

        if directory and not path.isdir(directory) and makedirs(directory) and not path.isdir(directory):
            makedirs(directory)

        method = Prompt.ask("Choice your authentication method",
                            choices=[LOGIN_AUTH_METHOD, TOKEN_AUTH_METHOD],
                            default=TOKEN_AUTH_METHOD)

        if LOGIN_AUTH_METHOD == method:
            login    = Prompt.ask("Enter your login")
            password = Prompt.ask("Enter your password", password=True)
            auth     = { "login": login, "password": password }
        else:
            token    = Prompt.ask("Enter your token", password=True)
            auth     = { "token": token }

        auth["method"] = method

        with open(AUTH_FILE, "w") as file:
            file.write(json.dumps(auth))

        return True

    async def authenticate(self) -> bool:
        if not self.configurated():
            return False

        with open(AUTH_FILE) as file:
            login_or_token = json.loads(file.read())

        try:
            self.github = Github(login_or_token.get(login_or_token.get("method")))
            self.user   = self.github.get_user()

            self.user.login

        # Update ???
        except BadCredentialsException as exception:
            # console.print("[red]{message}".format(message=exception.data.get("message")))
            return False

        return True

    async def search_email(self, email: Email):
        if not self.authenticated():
            await self.authenticate()

        users = self.github.search_users("{} in:email".format(email.address))

        for user in users:
            email.user = user
            return True

        return False

    async def create_repository(self, name, *, private=False):
        if not self.authenticated():
            await self.authenticate()

        return self.user.create_repo(name, private=private)

    async def get_repo(self, name: str):
        if not self.authenticated():
            await self.authenticate()

        return self.user.get_repo(name)
        # return self.github.get_repo(name)
