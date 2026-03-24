def print_success(message):
    print(f"[SUCCESS] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

index = None

def run_shell():
    while True:
        command = input("> ").strip()
        
        if not command:
            continue

        if command == "exit":
            print_info("Exiting...")
            break

        elif command == "build":
            print_info("Building index...")
            # index = build_index(...)
            index = {}  # placeholder
            print_success("Index built")

        elif command == "load":
            print_info("Loading index...")
            index = {}  # placeholder
            print_success("Index loaded")

        elif command.startswith("print "):
            word = command[6:].strip()
            if not word:
                print_error("Please provide a word to print")
                continue

        elif command.startswith("find "):
            query = command[5:].strip()
            if not query:
                print_error("Query cannot be empty")
                continue

        else:
            print_error("Invalid command")


if __name__ == "__main__":
    run_shell()