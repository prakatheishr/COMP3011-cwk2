def print_success(message):
    print(f"[SUCCESS] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

def run_shell():
    while True:
        command = input("> ").strip()

        if command == "exit":
            print_info("Exiting...")
            break

        elif command == "build":
            print_info("Building index...")

        elif command == "load":
            print_info("Loading index...")

        elif command.startswith("print "):
            word = command[6:].strip()
            print_info(f"Printing results for: {word}")

        elif command.startswith("find "):
            query = command[5:].strip()
            print_info(f"Searching for: {query}")

        else:
            print_error("Invalid command")