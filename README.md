<div align="center">

## README Obfuscator 🛡️

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

<h6>A tool to obfuscate GitHub README files by injecting invisible characters and HTML noise, 
  
  making copying difficult while keeping the rendered output unchanged.</h6>

</div>

## Features
- Obfuscates text using zero-width characters.
- Keeps visual appearance unchanged in Markdown renderers.
- Preserves code blocks, links, and images.
- Injects random hidden HTML snippets.
- Lightweight and easy-to-use.

## Installation & Usage

### Install
```sh
git clone https://github.com/zebbern/readme-obfuscator.git
cd readme-obfuscator
```

### Run the script
```sh
python3 obfuscate.py readme.md obfuscated_readme.md
```

## 🛠 How It Works
```
This script reads a Markdown file (e.g. a GitHub README.md)
and injects a huge amount of "waste" (random invisible characters)
into its text so that if someone copy‐pastes the content they get extra junk.
Waste is interleaved only into "normal text" (excluding code blocks,
links/images/HTML tags and key Markdown structural markers) so that the rendered
output on GitHub remains unchanged.

Special notes:
    • Horizontal rules (lines with 3+ dashes) are preserved and isolated.
    • Waste is injected in high amounts (20–50 random invisible characters per non‐whitespace character).
    • Multiple hidden HTML snippet blocks with randomized attribute values are appended.
    • Additionally, a fixed snippet block (with provided values) is appended.
    • Extra random attributes (such as id, data-rand, alt, target, aria-label, viewBox, version)
      are added to nearly every HTML element to obfuscate the source.
    • The waste characters include a diverse mix of Unicode control characters and zero‐width joiners/non‐joiners.
      (Note: The right‐to‐left mark, which flips characters, has been removed.)
```

🚀 **Protect your README today!**
