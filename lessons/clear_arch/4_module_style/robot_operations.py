def perform_command(cmd: str, *args) -> None:
    prefix = cmd
    postfix = (" " + ", ".join([str(a) for a in args])) if args else ""
    print(prefix, postfix)
