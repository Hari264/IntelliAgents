import glob, re

pattern = re.compile(r"^(title):\s+(?![\"'])(.*: .*)$", re.M)
changed = []
for p in glob.glob("data/docs/**/*.md", recursive=True):
    text = open(p, encoding="utf-8").read()
    head_end = text.find("\n---", 3)                 # end of the YAML header
    head, rest = text[:head_end], text[head_end:]
    new_head = pattern.sub(lambda m: f'{m.group(1)}: "{m.group(2).strip()}"', head)
    if new_head != head:
        open(p, "w", encoding="utf-8").write(new_head + rest)
        changed.append(p)
print(len(changed), "files fixed:")
for p in changed: print(" -", p)