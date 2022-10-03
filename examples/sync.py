import lastfm


client = lastfm.SyncClient("api_key_here")

oqt = client.fetch_user("oqt")

print(oqt.playcount)
