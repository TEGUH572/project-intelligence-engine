from pathlib import Path


def get_projects():
    print("\n===== BATCH SCANNER =====")
    print("1. Input Manual")
    print("2. Load dari file")
    print()

    choice = input("Pilih : ").strip()

    if choice == "1":
        return manual_input()

    elif choice == "2":
        return load_file()

    else:
        print("Pilihan tidak valid.")
        return []


def manual_input():

    print("\nMasukkan daftar project")
    print("Ketik 'selesai' jika selesai.\n")

    projects = []

    while True:

        project = input("Project : ").strip()

        if not project:
            continue

        if project.lower() == "selesai":
            break

        if project not in projects:
            projects.append(project)

    return projects


def load_file():

    filename = input("\nNama file (.txt): ").strip()

    path = Path(filename)

    if not path.exists():
        print("File tidak ditemukan.")
        return []

    projects = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            project = line.strip()

            if not project:
                continue

            if project not in projects:
                projects.append(project)

    return projects