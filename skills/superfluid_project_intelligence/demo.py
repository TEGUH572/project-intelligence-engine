from skill import run


def main():

    project = input("Project Name : ").strip()

    if project:

        run(project)


if __name__ == "__main__":

    main()