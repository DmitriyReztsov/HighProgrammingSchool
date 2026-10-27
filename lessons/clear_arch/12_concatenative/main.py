from cleaner_api import api


def streaming_generator():
    stream_string = "100 move -90 turn soap set start 50 move stop"
    for inp in stream_string.split():
        yield inp


def main():
    state = None
    for inp in streaming_generator():
        state = api(inp, state)


if __name__ == "__main__":
    main()