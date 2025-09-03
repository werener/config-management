import os, sys, re, platform

CURRENT_SYSTEM = platform.system()


def handle_args():
    args = sys.argv
    path_to_app = args[0]
    paths = {"VFS": "", "script": ""}

    for (i, arg) in enumerate(args):
        if arg.startswith('--'):
            match arg.removeprefix("--"):
                case "script":
                    try:
                        paths["script"] = f"{args[i+1]}"
                    except:
                        raise Exception("Empty arguments for flag '--script'")
                case "vfs" | "vfs-path" | "path-to-vfs":
                    try:
                        paths["VFS"] = f'{args[i + 1]}'
                    except:
                        raise Exception(f"Empty arguments for flag {arg}")
    if not paths["VFS"]:
        raise Exception("Path to VFS wasn't provided")
    else:
        return paths
            


if __name__ == '__main__':
    handle_args()