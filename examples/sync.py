import lastfm


client = lastfm.SyncClient("api_key_here")

user = client.fetch_user("crygup")

print(user.playcount)
