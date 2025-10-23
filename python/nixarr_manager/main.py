import os
import sys
import shutil

from enum import Enum, auto


try:
    import pwd
except ImportError:
    pwd = None


EXPECTED_USER = "starr"
CUTOFF_DISK_USAGE = 0.80


class SyncType(Enum):
    full = auto()
    movies_only = auto()
    shows_only = auto()


"""
health:
  check disk usage

get current sync status -> sync -> delete synced content
"""


def get_current_username() -> str:
    match sys.platform:
        case "win32":
            user = os.environ.get("USERNAME")

            if user is not None:
                return user

            raise ValueError("Couldn't find username")

        case "linux":
            user = os.environ.get("USER")

            if user is not None:
                return user

            # should be there on linux
            assert pwd is not None, "missing pwd on linux somehow"
            return pwd.getpwuid(os.getuid()).pw_name  # type: ignore (.getpwuid not on windows but we check platform above)
        case _:
            raise NotImplementedError()


def get_disk_usage() -> float:
    usage = shutil.disk_usage("/")
    return usage.used / usage.total


def get_sync_status(): ...


def run_sync(sync_type: SyncType = SyncType.full) -> bool:
    if (current_username := get_current_username()) != EXPECTED_USER:
        raise RuntimeError(f'Running as wrong user "{current_username}" insted of expected user "{EXPECTED_USER}"')

    match sync_type:
        case SyncType.full:
            command = "sync"
        case SyncType.movies_only:
            command = "sync-movies"
        case SyncType.shows_only:
            command = "sync-tv"
        case _:
            raise RuntimeError(f"Unhandled sync type {sync_type}")
        
    return os.system(f"cd ~ && just {command}") == 0


def remove_synced_content(): ...


def main():
    disk_usage = get_disk_usage()

    if disk_usage > CUTOFF_DISK_USAGE:
        # turn off download client
        ...

    run_sync()


if __name__ == "__main__":
    main()
