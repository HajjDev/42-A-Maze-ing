# This script does not check for errors or malformed files.
# It only validates that neighbooring cells sharing a wall have
#  both the correct encoding.
# Usage: python3 output_validator.py output_maze.txt

import sys

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <output_file>")
    sys.exit(1)

g = []
for line in open(sys.argv[1]):
    if line.strip() == '':
        break
    g.append([int(c, 16) for c in line.strip(' \t\n\r')])

# for r in range(len(g)):
#     for c in range(len(g[0])):
#         v = g[r][c]
#         if not all([(r < 1 or v & 1 == (g[r-1][c] >> 2) & 1),
#                     (c >= len(g[0])-1 or (v >> 1) & 1 == (g[r][c+1] >> 3) & 1),
#                     (r >= len(g)-1 or (v >> 2) & 1 == g[r+1][c] & 1),
#                     (c < 1 or (v >> 3) & 1 == (g[r][c-1] >> 1) & 1)]):
#             print(f'Wrong encoding for ({c},{r})')
for r in range(len(g)):
    for c in range(len(g[0])):
        v = g[r][c]
        # Comparaison avec le voisin du dessus (r-1)
        # Mon North (bit 3) doit être égal au South (bit 1) du voisin du haut
        if r > 0:
            if (v >> 3) & 1 != (g[r-1][c] >> 1) & 1:
                print(f'Error North/South at ({c},{r}) and ({c},{r-1})')
        
        # Comparaison avec le voisin de droite (c+1)
        # Mon East (bit 2) doit être égal au West (bit 0) du voisin de droite
        if c < len(g[0]) - 1:
            if (v >> 2) & 1 != (g[r][c+1] & 1):
                print(f'Error East/West at ({c},{r}) and ({c+1},{r})')