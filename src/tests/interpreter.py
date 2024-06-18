import os, subprocess
from typing import Tuple


def interpret(code: str) -> Tuple[int, bytes, bytes]:
    source_file = "tmp.c"
    executable_file = "./tmp"

    with open(source_file, "w") as f:
        f.write(code)

    command = [
        "gcc",
        # "clang",
        # "tcc",
        "-Wall",
        "-Wextra",
        "-pedantic",
        "-Werror",
        "-fsanitize=address",
        "-fsanitize=undefined",
        "-std=c99",
        "-lm",
        source_file,
        "-o",
        executable_file,
    ]

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if stdout:
        print("stdout:")
        print(stdout.decode("utf-8"))
        print()

    if stderr:
        print("stderr:")
        print(stderr.decode("utf-8"))
        print()

    assert (
        process.returncode == 0
    ), f"Compilation failed with exit code {process.returncode}"

    process = subprocess.Popen(
        executable_file,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Can write stuff to stdin for more interoperability if needed
    # process.stdin.write("Hello, World!")

    stdout, stderr = process.communicate()

    if stdout:
        print("stdout:")
        print(stdout.decode("utf-8"))
        print()

    if stderr:
        print("stderr:")
        print(stderr.decode("utf-8"))
        print()

    os.remove(source_file)
    os.remove(executable_file)

    # TODO
    # wrap returncode in Value object
    return process.returncode, stdout, stderr


def interpret_statements(code: str) -> Tuple[int, bytes, bytes]:
    main_code = (
        """
    int main(){
        %s
    }
    """
        % code
    )

    return interpret(main_code)
