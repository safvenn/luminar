# 6. Music Playlist 🎧

# Given:
# playlist = ["song1", "song2", "song3"]

# Steps:

# Add "intro_song" at the top.

# Remove "song2".

# Add "outro_song" at the end.


# Expected Output:

# Final Playlist: ['intro_song', 'song1', 'song3', 'outro_song']


# ---


playlist = ["song1", "song2", "song3"]

playlist.insert(0,"Intro_song")
playlist.remove('song2')
playlist.append("outro_song")

print(playlist)
