import re
from collections import Counter

sentence = "Hello welcome to Cathay 60th year anniversary"
sentence = sentence.upper()

filtered_chars = re.findall(r'[A-Z0-9]', sentence)
char_count = Counter(filtered_chars)

for char, count in sorted(char_count.items()):
    print(f"{char}: {count}")