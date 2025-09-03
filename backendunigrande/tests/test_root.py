def test_root_returns_hello(test_app):
    response = test_app.get("/")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    assert response.status_code == 200
    assert response.json() == {"Hello": "API está ativa no ambiente;"}
