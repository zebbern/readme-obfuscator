#!/usr/bin/env python3
import re
import random
import string
import argparse

# --- Configuration ---
# Expanded list of invisible waste characters (with RTL mark removed)
WASTE_ENTITIES = [
    "&#8203;",      # Zero Width Space (decimal)
    "&#x200B;",     # Zero Width Space (hex)
    "\u200B",       # Zero Width Space (native)
    "\u200C",       # Zero Width Non-Joiner
    "\u200D",       # Zero Width Joiner
    "\u200E",       # Left-to-Right Mark
    "\u2060",       # Word Joiner
    "\ufeff",       # Zero Width No-Break Space (BOM)
    "&#8204;",      # Alternate Zero Width Non-Joiner
    "&#8205;",      # Alternate Zero Width Joiner
    "&#8206;",      # Alternate Left-to-Right Mark
    "&#8288;"       # Word Joiner (decimal)
]

def generate_waste():
    """
    Returns a random string of invisible waste characters.
    The count is chosen randomly between 20 and 50.
    """
    count = random.randint(20, 50)
    return ''.join(random.choice(WASTE_ENTITIES) for _ in range(count))

def insert_waste_in_segment(segment):
    """
    Inserts a random waste string after every non-whitespace character in the segment.
    Whitespace characters are preserved so that layout remains intact.
    """
    new_seg = ""
    for char in segment:
        new_seg += char
        if not char.isspace():
            new_seg += generate_waste()
    return new_seg

def inject_waste_everywhere(text):
    """
    Inserts a random waste string after every single character in the text.
    This version does NOT skip whitespace.
    """
    new_text = ""
    for char in text:
        new_text += char + generate_waste()
    return new_text

# Patterns for "protected" segments that should not be wasteified:
#   • Markdown links/images: [alt text](URL)
#   • Inline code: `code`
#   • Raw HTML tags: <tag ...>
PROTECTED_REGEX = re.compile(r"^(\[.*?\]\(.*?\)|<[^>]+>|`[^`]+`)$", re.DOTALL)

def process_text(text):
    """
    Processes a chunk of text (outside code blocks) by splitting it into
    protected segments (links, inline code, HTML tags) and unprotected text.
    Waste is inserted only into unprotected parts.
    """
    split_pattern = r"(\[.*?\]\(.*?\)|<[^>]+>|`[^`]+`)"
    parts = re.split(split_pattern, text)
    new_text = ""
    for part in parts:
        if PROTECTED_REGEX.fullmatch(part):
            new_text += part
        else:
            new_text += insert_waste_in_segment(part)
    return new_text

def process_line(line):
    """
    Processes a single line (outside code blocks). If the line begins with a Markdown
    marker (headers, list bullets, etc.), only the content following the marker is processed.
    """
    marker_match = re.match(r'^(\s*(?:[#>*+\-]|\d+\.)\s+)(.*)', line)
    if marker_match:
        prefix, content = marker_match.groups()
        return prefix + process_text(content)
    else:
        return process_text(line)

def random_string(length):
    """
    Returns a random alphanumeric string of the specified length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_snippet():
    """
    Returns a hidden HTML snippet block with randomized values and extra random attributes.
    Structure:
      <!-- RANDOM_COMMENT -->
      <td align="center" id="{random}" data-rand="{random}">
      <div class="wrap-KuXm" data-wrap-wmU="{RANDOM8}" target="_blank" aria-label="smt{random}">
      <span class="hidden-zmao" data-hidden-NNu="{RANDOM8}" viewBox="smt{random}" version="smt{random}">
      </span>
    """
    comment = random_string(21)
    div_val = random_string(8)
    span_val = random_string(8)
    td_extra = f' id="{random_string(10)}" data-rand="{random_string(10)}"'
    div_extra = f' target="_blank" aria-label="smt{random_string(3)}"'
    span_extra = f' viewBox="smt{random_string(4)}" version="smt{random_string(3)}"'
    snippet = (
        "\n" +
        f"<!-- {comment} -->\n" +
        f"<td align=\"center\"{td_extra}>\n" +
        f"<div class=\"wrap-KuXm\" data-wrap-wmU=\"{div_val}\"{div_extra}>\n" +
        f"<span class=\"hidden-zmao\" data-hidden-NNu=\"{span_val}\"{span_extra}>\n" +
        "</span>\n"
    )
    return snippet

def fixed_snippet():
    """
    Returns a fixed HTML snippet block with provided values and extra random attributes.
    Structure:
      <td align="center" id="{random}" data-rand="{random}">
      <div class="wrap-KuXm" data-wrap-wmU="8SocrCdu" target="_blank" aria-label="smt{random}">
      <span class="hidden-zmao" data-hidden-NNu="P7KLkqR9" viewBox="smt{random}" version="smt{random}">
      </span>
    """
    td_extra = f' id="{random_string(10)}" data-rand="{random_string(10)}"'
    div_extra = f' target="_blank" aria-label="smt{random_string(3)}"'
    span_extra = f' viewBox="smt{random_string(4)}" version="smt{random_string(3)}"'
    return (
        "\n" +
        f"<td align=\"center\"{td_extra}>\n" +
        f"<div class=\"wrap-KuXm\" data-wrap-wmU=\"8SocrCdu\"{div_extra}>\n" +
        f"<span class=\"hidden-zmao\" data-hidden-NNu=\"P7KLkqR9\"{span_extra}>\n" +
        "</span>\n"
    )

def add_random_attributes_to_tags(text):
    """
    Finds every HTML start tag in the text and adds extra random attributes if not already present.
    For every tag, the following are added:
      - id="{random}" and data-rand="{random}"
    Additionally, for specific tags:
      - For <img>, if alt is missing, add alt="{random}"
      - For <a>, if target is missing, add target="_blank" and if aria-label is missing, add aria-label="smt{random}"
      - For <svg>, if viewBox is missing, add viewBox="smt{random}" and if version is missing, add version="smt{random}"
    """
    pattern = re.compile(r"<(\w+)([^>]*?)>")
    
    def replacer(match):
        tag = match.group(1)
        attrs = match.group(2)
        new_attrs = ""
        # Always add id and data-rand if not present.
        if 'id=' not in attrs:
            new_attrs += f' id="{random_string(10)}"'
        if 'data-rand=' not in attrs:
            new_attrs += f' data-rand="{random_string(10)}"'
        # Additional attributes for specific tags:
        if tag.lower() == "img" and "alt=" not in attrs:
            new_attrs += f' alt="{random_string(6)}"'
        if tag.lower() == "a":
            if "target=" not in attrs:
                new_attrs += ' target="_blank"'
            if "aria-label=" not in attrs:
                new_attrs += f' aria-label="smt{random_string(3)}"'
        if tag.lower() == "svg":
            if "viewBox=" not in attrs:
                new_attrs += f' viewBox="smt{random_string(4)}"'
            if "version=" not in attrs:
                new_attrs += f' version="smt{random_string(3)}"'
        return f"<{tag}{new_attrs}{attrs}>"
    
    return pattern.sub(replacer, text)

def main():
    parser = argparse.ArgumentParser(
        description="Inject waste HTML entities into a Markdown file without affecting its rendered appearance."
    )
    parser.add_argument("input_file", help="Path to the input Markdown file")
    parser.add_argument("output_file", help="Path for the output (waste‑injected) Markdown file")
    args = parser.parse_args()

    # Read the input file.
    with open(args.input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    processed_lines = []
    in_code_block = False  # Track if we're inside a triple-backtick code block.

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        # Toggle code block flag when encountering triple-backticks.
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            processed_lines.append(line)
            continue
        # If inside a code block, leave the line unmodified.
        if in_code_block:
            processed_lines.append(line)
            continue
        # Isolate horizontal rules (lines of 3+ dashes) with blank lines above and below.
        if re.fullmatch(r'\s*-{3,}\s*', line):
            if not processed_lines or processed_lines[-1].strip() != "":
                processed_lines.append("\n")
            processed_lines.append(line)
            processed_lines.append("\n")
            continue
        # Process the line normally.
        processed_lines.append(process_line(line))

    # Append extra randomized hidden HTML snippet blocks.
    NUM_SNIPPETS = 6  # Adjust as desired.
    for _ in range(NUM_SNIPPETS):
        processed_lines.append(generate_snippet())

    # Append the fixed snippet block (with provided values).
    processed_lines.append(fixed_snippet())

    # Join all lines into a final output string.
    final_output = "".join(processed_lines)
    # Post-process the final output to add extra random attributes to all HTML tags.
    final_output = add_random_attributes_to_tags(final_output)

    # Write out the new file.
    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(final_output)

if __name__ == "__main__":
    main()
