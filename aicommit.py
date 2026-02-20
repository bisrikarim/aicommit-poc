import subprocess
import urllib.request
import json
import sys

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:3b"

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def get_staged_diff():
    return run(["git", "diff", "--staged"])

def get_staged_files():
    return run(["git", "diff", "--staged", "--name-only"])

def generate_commit_message(diff, files):
    prompt = "You are an expert developer. Generate a git commit message.\nRules:\n- Conventional Commits format: <type>(<scope>): <description>\n- Types: feat, fix, docs, style, refactor, test, chore\n- Under 72 characters\n- Return ONLY the commit message, no explanation\n\nFiles:\n" + files + "\n\nDiff:\n" + diff[:4000]
    payload = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False}).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
            return data["message"]["content"].strip()
    except Exception as e:
        print("Erreur Ollama: " + str(e))
        sys.exit(1)

def do_commit(message):
    result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
    print(result.stdout if result.returncode == 0 else result.stderr)

def main():
    print("Analyse des changements stages...\n")
    diff = get_staged_diff()
    files = get_staged_files()
    if not diff:
        print("Aucun changement stage. Faites 'git add' d'abord.")
        sys.exit(0)
    print("Fichiers: " + files + "\n")
    print("Generation du message avec Ollama (qwen2.5-coder)...\n")
    message = generate_commit_message(diff, files)
    print("Message suggere: " + message + "\n")
    choice = input("Que faire ? [O]k / [E]diter / [A]nnuler : ").strip().lower()
    if choice in ("o", "oui", "y", "yes", ""):
        do_commit(message)
    elif choice in ("e", "edit"):
        edited = input("Nouveau message : ").strip()
        do_commit(edited if edited else message)
    else:
        print("Commit annule.")

main()
