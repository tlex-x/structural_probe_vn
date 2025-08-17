import sys

if len(sys.argv) != 2:
    print("Usage: python convert_conll_to_raw.py <input_file.conllu>", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]

buf = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            # End of sentence
            if buf:
                print(" ".join(buf))
                buf = []
        elif not line.startswith("#"):
            # Token lines: ID, FORM, ...
            cols = line.split("\t")
            if len(cols) >= 2:
                buf.append(cols[1])

# Print last sentence if file doesn’t end with a blank line
if buf:
    print(" ".join(buf))
