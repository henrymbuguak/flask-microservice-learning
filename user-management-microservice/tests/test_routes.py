def test_register_user(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'test@example.com'

def test_login_user(client):
    # Register a user first
    register_response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert register_response.status_code == 201  # Ensure registration is successful

    # Test login with correct credentials
    login_response = client.post('/api/login', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert login_response.status_code == 200  # Ensure login is successful
    assert 'access_token' in login_response.json  # Ensure access_token is present

    # Test login with incorrect credentials
    failed_login_response = client.post('/api/login', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    assert failed_login_response.status_code == 401  # Ensure login fails
    assert 'error' in failed_login_response.json  # Ensure error message is present

def test_protected_route(client):
    # Register a new user
    client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })

    # Log in to get a JWT token
    login_response = client.post('/api/login', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    })

    assert login_response.status_code == 200  # Ensure login is successful

    # Extract the access token
    token = login_response.get_json().get("access_token")
    assert token is not None  # Ensure token was returned

    # Include the token in the Authorization header
    headers = {"Authorization": f"Bearer {token}"}

    # Correct route: "/api/protected"
    response = client.get('/api/protected', headers=headers)
    assert response.status_code == 200  # Should return 200 if authorized
    assert 'message' in response.get_json()  # Ensure response contains a message

    assert 'message' in response.get_json()  # Ensure response contains a message
