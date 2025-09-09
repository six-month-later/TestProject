import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.parametrize("num1,num2,expected_result",[
    ("1", "2", 3),
    ("5", "-3", 2),
    ("1000000000", "100000000", 1100000000),
    ("354", "-454", -100),
    ("0", "0", 0),
    ("1", "1", 2),
    ("5", "0", 5),
    ("0", "5", 5),
    ("0", "-23", -23),
])
def test_calculate_pozitive_scenarios(num1, num2, expected_result):
    response = client.post("/tasks/calculate", params={"num1": num1, "num2": num2}
    )

    assert response.status_code == 200
    assert response.json() == {"result": expected_result} 


@pytest.mark.parametrize("invalid_input", [
    {"num1": "abc", "num2": "3"},
    {"num1": "5", "num2": "def"},
    {"num1": "5"},
    {"num2": "3"},
    {},
])
def test_calculate_invalid_inputs(invalid_input):
    response = client.post("/tasks/calculate", params=invalid_input)
    assert response.status_code == 422


def test_calculate_valid_numbers():
    response = client.post(
        "/tasks/calculate", params={"num1": 5, "num2": 3}
    )

    assert response.status_code == 200
    assert response.json() == {"result": 8}
