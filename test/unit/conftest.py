import pytest

# The scope of this conftest.py is everything in the same directory. So test_playground can use the
# fixture defined below without any explicit import statements
@pytest.fixture()
def the_number_seven():
    return 7
