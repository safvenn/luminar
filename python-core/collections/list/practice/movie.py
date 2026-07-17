# ---

# 2. Favorite Movies 🎬

# Task:
# Given list = ["Inception", "Titanic", "Avatar", "Interstellar", "Joker"]

# Add one new movie.

# Remove one movie you no longer like.

# Insert a new movie in between.

# Show final list.


# Sample Execution:

# Original List: ['Inception', 'Titanic', 'Avatar', 'Interstellar', 'Joker']
# After adding: ['Inception', 'Titanic', 'Avatar', 'Interstellar', 'Joker', 'Oppenheimer']
# After removing 'Titanic': ['Inception', 'Avatar', 'Interstellar', 'Joker', 'Oppenheimer']
# After inserting 'Shutter Island' at position 2: ['Inception', 'Avatar', 'Shutter Island', 'Interstellar', 'Joker', 'Oppenheimer']

# Expected Output:

# Updated Movie List: ['Inception', 'Avatar', 'Shutter Island', 'Interstellar', 'Joker', 'Oppenheimer']


# ---

movies=["Inception", "Titanic", "Avatar", "Interstellar", "Joker"]

movies.append("Openhimer")
movies.remove("Inception")
movies.insert(2,"shutter island")

print(movies)