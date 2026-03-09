#!/usr/bin/env python3
"""Extract Key Study blocks from markdown into a separate file.

Stop rule:
  - Stop at ANY new Key Study heading (that signals a new study)
  - Stop at a non-study heading SHALLOWER than the current study level
  - Same-level non-study headings (e.g. ## TLDR inside ## Key Study) are kept
"""

import re

INPUT  = "TEST_chunk3_schizophrenia_criteria.md"
OUTPUT = "STUDIES_chunk3_schizophrenia_criteria.md"

STUDY_HEADING = re.compile(
    r'^(#{1,4})\s*.*?(Key Study|🔑 Study|🧪 Key Study)',
    re.IGNORECASE
)

def heading_level(line):
    m = re.match(r'^(#{1,6})\s', line)
    return len(m.group(1)) if m else 0

def is_study_heading(line):
    return bool(STUDY_HEADING.match(line))

with open(INPUT, encoding="utf-8") as f:
    lines = f.readlines()

studies = []
i = 0
while i < len(lines):
    line = lines[i]
    if is_study_heading(line):
        study_level = heading_level(line)
        block = [line]
        i += 1
        while i < len(lines):
            cur = lines[i]
            lvl = heading_level(cur)
            if lvl > 0:
                if is_study_heading(cur):
                    break  # Any new Key Study heading = new study starts
                if lvl < study_level:
                    break  # Shallower non-study section ends this study
                # Same-level or deeper non-study headings = sub-sections, keep
            block.append(cur)
            i += 1
        while block and block[-1].strip() in ('', '---'):
            block.pop()
        studies.append(''.join(block))
    else:
        i += 1

header = "# Key Studies — CIE 9990 Psychology\n\nExtracted from `TEST_chunk3_schizophrenia_criteria.md`\n\n"
separator = "\n\n---\n\n"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(header)
    f.write(separator.join(studies))
    f.write("\n")

print(f"Extracted {len(studies)} studies → {OUTPUT}")
for s in studies:
    first_line = s.split('\n')[0]
    line_count = s.count('\n')
    print(f"  {line_count:4d} lines  {first_line[:80]}")
