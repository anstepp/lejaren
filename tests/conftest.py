import pytest

@pytest.fixture(scope="session")
def shared_output_dir(tmp_path_factory):
    # mktemp creates the actual directory structure
    base_dir = tmp_path_factory.mktemp("artifacts")
    return base_dir