#!/usr/bin/env python

# Attempts to reverse any Signal specific modifications to webrtc.
# If our patches change, this may have to be revisted in the future.
#
# Example Usage:
#
#     ./clean_webrtc.py
#

import os
import subprocess
import contextlib

@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)

BIN_DIR = os.path.dirname(__file__)

def make_pristine(path, ignore_failures = False):
    print("Cleaning %s" % path)
    if not os.path.exists(path):
        if ignore_failures:
            print("path=%s does not exist, but that's OK" % path)
            return
        else:
          raise RuntimeError("path=%s does not exist" % path)

    with pushd(path):
		subprocess.check_output(["git", "clean", "-dfx"])
		subprocess.check_output(["git", "stash"])

def main():
    webrtc_src_dir = os.path.join(BIN_DIR, "../webrtc/src")

    # This directory moved, so it might need to be cleaned before updating, but
    # it won't be expected to exist in the future.
    legacy_sdk_dir = os.path.join(webrtc_src_dir, "webrtc", "sdk")
    make_pristine(legacy_sdk_dir, ignore_failures = True)

    sdk_dir = os.path.join(webrtc_src_dir, "sdk")
    make_pristine(sdk_dir)

    tools_dir = os.path.join(webrtc_src_dir, "tools_webrtc")
    make_pristine(tools_dir)

    third_party_dir = os.path.join(webrtc_src_dir, "third_party", "opus")
    make_pristine(third_party_dir)

if __name__ == "__main__":
    main()

