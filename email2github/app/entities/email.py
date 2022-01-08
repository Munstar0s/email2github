# -*- encoding: UTF-8 -*-

# Standard imports
import re

from dataclasses import dataclass
from typing      import List

# Third party imports
from github import NamedUser

# Application imports

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@dataclass
class Email(object):
    address: str
    user   : NamedUser = None

    @classmethod
    def load_from_file(self, path: str) -> List:
        with open(path) as file:
            emails = self.load(file.read().splitlines())

        return emails

    @classmethod
    def load_from_string(self, string: str) -> List:
        return self.load(string.split(","))

    @classmethod
    def load(self, emails: List) -> List:
        return [Email(e) for e in list(filter(lambda e: re.fullmatch(EMAIL_REGEX, e), emails))]

    def resolved(self) -> bool:
        return self.user is not None

    def name(self):
        if self.user:
            return self.user.name

        return None

    def username(self):
        if self.user:
            return self.user.login

        return None

    def profile_url(self):
        if self.user:
            return self.user.html_url

        return None

    # XXX Improve me
    def as_headers(self):
        return ["Email", "Username", "Name", "Profile"]

    def to_list(self):
        return [self.address, self.username(), self.name(), self.profile_url()]
