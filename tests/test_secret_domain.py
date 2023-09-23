import os

import pytest
import readonce

from pysecuresettings.domain.exceptions import FailedToLoadFromEnvVariable
from pysecuresettings.domain.model import Secret


def test_secret_created_from_value():
    secret1 = Secret().create("AWESOME1")
    secret2 = Secret().create("AWESOME2")
    assert secret1.get_secret() == "AWESOME1"
    assert secret2.get_secret() == "AWESOME2"
    with pytest.raises(readonce.UnsupportedOperationException):
        secret1.get_secret()

    with pytest.raises(readonce.UnsupportedOperationException):
        secret2.get_secret()


def test_secret_created_from_value_with_description():
    db = Secret(description="Awesome DB connection credentials").create("AWESOME1")
    aws = Secret(description="Awesome AWS credentials").create("AWESOME2")
    assert db is not aws
    assert db != aws
    assert db.get_secret() == "AWESOME1"
    assert aws.get_secret() == "AWESOME2"
    with pytest.raises(readonce.UnsupportedOperationException):
        db.get_secret()

    with pytest.raises(readonce.UnsupportedOperationException):
        aws.get_secret()


def test_secret_representation_with_description():
    db = Secret(description="Awesome DB connection credentials").create("AWESOME1")
    aws = Secret(description="Awesome AWS credentials").create("AWESOME2")
    assert db.__str__() == "<Secret> for Awesome DB connection credentials"
    assert aws.__str__() == "<Secret> for Awesome AWS credentials"
    assert db.__repr__() == "<Secret> for Awesome DB connection credentials"
    assert aws.__repr__() == "<Secret> for Awesome AWS credentials"


def test_secret_representation_without_description():
    db = Secret().create("AWESOME1")
    aws = Secret().create("AWESOME2")
    assert db.__str__() == "<Secret> for __anonymous__"
    assert aws.__str__() == "<Secret> for __anonymous__"
    assert db.__repr__() == "<Secret> for __anonymous__"
    assert aws.__repr__() == "<Secret> for __anonymous__"


def test_secret_created_from_existing_env_variables():
    os.environ["DB"] = "AWESOME1"
    os.environ["AWS"] = "AWESOME2"

    db = Secret().create_from_env("DB")
    aws = Secret().create_from_env("AWS")

    assert db is not aws
    assert db != aws
    assert db.get_secret() == "AWESOME1"
    assert aws.get_secret() == "AWESOME2"
    with pytest.raises(readonce.UnsupportedOperationException):
        db.get_secret()

    with pytest.raises(readonce.UnsupportedOperationException):
        aws.get_secret()


def test_secret_created_from_non_existing_env_variables():
    with pytest.raises(FailedToLoadFromEnvVariable):
        Secret().create_from_env("DB_")
    with pytest.raises(FailedToLoadFromEnvVariable):
        Secret().create_from_env("AWS_")
