import subprocess
import sys


def run(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)


def main() -> None:
    run(["python", "src/load/postgres.py"])
    run([
        "python",
        "src/transform/ssh_auth.py",
    ])

    run([
        "docker",
        "compose",
        "exec",
        "-T",
        "postgres",
        "psql",
        "-U",
        "security",
        "-d",
        "security_platform",
        "-f",
        "/dev/stdin",
    ])


if __name__ == "__main__":
    main()
