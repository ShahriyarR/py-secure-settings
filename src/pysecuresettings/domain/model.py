import os

import icontract
from readonce import ReadOnce

from pysecuresettings.domain.exceptions import FailedToLoadFromEnvVariable


class Secret(ReadOnce):
    def __init__(self, description: str = "__anonymous__") -> None:
        super().__init__()
        self.description = description

    def create_from_env(self, key: str) -> "Secret":
        if value := os.getenv(key, None):
            self.add_secret(value)
        else:
            raise FailedToLoadFromEnvVariable("Could not find or load the given environment variable")
        return self

    @icontract.ensure(lambda self: len(self) == 1, "Failed to create secret")
    def create(self, secret: str) -> "Secret":
        self.add_secret(secret)
        return self

    def __str__(self) -> str:
        return f"<Secret> for {self.description}"

    def __repr__(self):
        return f"<Secret> for {self.description}"
