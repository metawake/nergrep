import typer


def main(name: str = "Alex"):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
    print("==== END of execution ====")
