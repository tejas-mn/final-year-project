def test_home_page(client):
    response = client.get("/")
    print(response)
    assert b'<title>Home</title>' in response.data
    
def test_app(client):
    response = client.get("/")
    assert response.status_code == 200
    