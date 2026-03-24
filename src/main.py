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
            if index is None:
                print_error("No index loaded. Run 'build' or 'load' first.")
                continue

        elif command.startswith("find "):
            query = command[5:].strip()
            print_info(f"Searching for: {query}")

        else:
            print_error("Invalid command")