import os
import subprocess
import shlex

def print_help():
    print("\n📘 Διαθέσιμες εντολές:")
    print("  help           Εμφανίζει αυτή τη βοήθεια")
    print("  exit / quit    Κλείνει το shell")
    print("  cd <φάκελος>   Αλλάζει τρέχοντα φάκελο")
    print("  [εντολή]       Τρέχει εντολές Linux (π.χ. ls, pwd, echo)")
    print("  [εντολή1] | [εντολή2]     Pipe (π.χ. ls | grep py)")
    print("  [εντολή] > αρχείο.txt     Redirection (π.χ. echo test > out.txt)\n")

def get_prompt():
    current_dir = os.getcwd()
    home = os.path.expanduser("~")
    if current_dir.startswith(home):
        current_dir = current_dir.replace(home, "~", 1)

    prompt_color = "\033[92m"  # Πράσινο
    reset_color = "\033[0m"
    return f"{prompt_color}myshell [{current_dir}]> {reset_color}"

def execute_command(command):
    try:
        if "|" in command:
            # Pipe: ls | grep py
            parts = [shlex.split(p.strip()) for p in command.split("|")]
            p1 = subprocess.Popen(parts[0], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(parts[1], stdin=p1.stdout)
            p1.stdout.close()
            p2.communicate()
        elif ">" in command:
            # Redirection: echo hi > out.txt
            parts = command.split(">")
            cmd = shlex.split(parts[0].strip())
            filename = parts[1].strip()
            with open(filename, "w") as f:
                subprocess.run(cmd, stdout=f)
        else:
            # Κανονική εντολή
            args = shlex.split(command)
            subprocess.run(args)
    except FileNotFoundError:
        print("❌ Λάθος εντολή: δεν βρέθηκε")
    except Exception as e:
        print(f"⚠️ Σφάλμα: {e}")

def main():
    print("Καλωσήρθες στο myshell!")
    print("Πληκτρολόγησε 'help' για οδηγίες.\n")

    while True:
        try:
            command = input(get_prompt()).strip()

            if not command:
                continue

            if command in ["exit", "quit"]:
                print("👋 Έξοδος από το shell.")
                break

            if command == "help":
                print_help()
                continue

            if command.startswith("cd"):
                args = shlex.split(command)
                try:
                    os.chdir(args[1])
                except IndexError:
                    print("cd: χρειάζεται path")
                except FileNotFoundError:
                    print(f"cd: δεν υπάρχει ο φάκελος '{args[1]}'")
                continue

            execute_command(command)

        except KeyboardInterrupt:
            print("\n(Χρησιμοποίησε 'exit' για να κλείσεις το shell)")

if __name__ == "__main__":
    main()