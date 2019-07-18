def test_site_map(client):
    response = client.get("/site-map")
    print(response)
