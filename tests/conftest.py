import json
from dataclasses import dataclass

import pytest

from pysecuresettings.domain.model import Secret


class CustomSecretEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return {"secret": obj.get_secret()}
        except AttributeError:
            return super().default(obj)


@dataclass
class DBPassword:
    password: Secret


@pytest.fixture(scope="module")
def get_db_password_dataclass():
    return DBPassword(password=Secret(description="User Password").create("awesome_pass"))


@pytest.fixture(scope="function")
def get_secret_object():
    return Secret(description="User Password").create("awesome_pass")


@pytest.fixture(scope="module")
def get_secret_class():
    return Secret


@pytest.fixture(scope="module")
def get_custom_secret_encoder():
    return CustomSecretEncoder
