import pytest
import app as app_module
from app import app

@pytest.fixture
def client():
    """Create a test client with a clean app state"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_game_state():
    """Reset game state before each test"""
    app_module.stuff = 0
    app_module.upgrades[0]['currentCost'] = 10
    app_module.upgrades[0]['power'] = 1
    app_module.upgrades[1]['currentCost'] = 100
    app_module.upgrades[1]['power'] = 0

def test_click_button(client):
    """Test that clicking the button increases stuff"""
    response = client.post('/click')
    assert response.status_code == 200
    data = response.get_json()
    assert data['stuff'] == 1  # click power is 1

def test_buy_upgrade_0_less_than_cost(client):
    """Test buying upgrade 0 when stuff is less than cost"""
    # upgrade 0 costs 10, we have 0
    response = client.post('/buy/0')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False
    assert data['stuff'] == 0

def test_buy_upgrade_0_equal_to_cost(client):
    """Test buying upgrade 0 when stuff equals cost"""
    # Set stuff to 10 (the cost of upgrade 0)
    app_module.stuff = 10
    
    response = client.post('/buy/0')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['stuff'] == 0  # 10 - 10 = 0

def test_buy_upgrade_0_greater_than_cost(client):
    """Test buying upgrade 0 when stuff is greater than cost"""
    # Set stuff to 20 (greater than cost of 10)
    app_module.stuff = 20
    
    response = client.post('/buy/0')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['stuff'] == 10  # 20 - 10 = 10

    # Check upgrade fields are updated
    assert data['upgrades'][0]['power'] == 6  # one purchase adds powerMultiplier 5
    assert data['upgrades'][0]['currentCost'] == pytest.approx(12.0)  # 10 * 1.2

def test_buy_upgrade_1_less_than_cost(client):
    """Test buying upgrade 1 when stuff is less than cost"""
    # upgrade 1 costs 100, we have 0
    response = client.post('/buy/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is False
    assert data['stuff'] == 0

def test_buy_upgrade_1_equal_to_cost(client):
    """Test buying upgrade 1 when stuff equals cost"""
    # Set stuff to 100 (the cost of upgrade 1)
    app_module.stuff = 100
    
    response = client.post('/buy/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['stuff'] == 0  # 100 - 100 = 0

def test_buy_upgrade_1_greater_than_cost(client):
    """Test buying upgrade 1 when stuff is greater than cost"""
    # Set stuff to 200 (greater than cost of 100)
    app_module.stuff = 200
    
    response = client.post('/buy/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['stuff'] == 100  # 200 - 100 = 100

def test_victory_logic(client):
    """Check that /won returns won status correctly"""
    # initial state should not be won
    response = client.get('/won')
    assert response.status_code == 200
    data = response.get_json()
    assert data['won'] is False

    # force a win state
    app_module.stuff = 1000000
    response = client.get('/won')
    assert response.status_code == 200
    data = response.get_json()
    assert data['won'] is True
    assert data['stuff'] == 1000000