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
- Inserts **invisible Unicode characters** (`​`, `‌`, `‍`, etc.).
- **Preserves Markdown formatting** for proper rendering.
- **Adds hidden HTML attributes** to further obfuscate the source.


🚀 **Protect your README today!**
