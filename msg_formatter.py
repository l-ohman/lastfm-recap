import json

## Converts weekly track chart response into discord message
def format():
    with open("example.json", "r") as res:
        data = json.load(res)
        tracklist = data["weeklytrackchart"]["track"][:5]
        for track in tracklist:
            print(track)
            print("\n")

format()
