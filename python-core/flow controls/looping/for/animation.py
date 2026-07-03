import os
import time

frames = [

r"""
   [■]
  /|█|\
   / \
""",

r"""
   [■]
  /|█|
   /\/
""",

r"""
   [■]
   |█|\
  / \
""",

r"""
   [■]
  \|█|/
    |\
""",

r"""
   [■]
  /|█|\
  /  \
""",

]

WIDTH = 70

while True:
    for x in range(WIDTH):
        os.system("cls" if os.name == "nt" else "clear")


        print("\033[96m")  # Cyan

        print("\n" * 8)

        frame = frames[x % len(frames)]

        for line in frame.splitlines():
            print(" " * x + line)

        print(" " * (x-2) + "⚡" if x > 2 else "")
        print("\033[0m")

        time.sleep(0.05)