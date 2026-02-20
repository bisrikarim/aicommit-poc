# aicommit-poc

A simple Python script that generates git commit messages using AI — running 100% locally with [Ollama](https://ollama.com).

Inspired by [aicommits](https://github.com/Nutlope/aicommits).

## Requirements

- Python 3
- Git
- [Ollama](https://ollama.com) installed

## Setup

```bash
ollama pull qwen2.5-coder:3b
```

## Usage

```bash
git add <files>
python aicommit.py
```

The script will suggest a commit message in [Conventional Commits](https://conventionalcommits.org/) format. You can accept, edit, or cancel.

## Example

```
Analysing staged changes...
Files: hello.py

Generating commit message...
Suggested: feat(hello.py): add greet function

What to do? [O]k / [E]dit / [C]ancel: o
[master 7c8e828] feat(hello.py): add greet function
```

## License

MIT
