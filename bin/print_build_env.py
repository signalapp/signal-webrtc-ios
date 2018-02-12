#!/usr/bin/env python

from string import Template
import subprocess
import os
import re
import contextlib

##
# Prints some details about the current build environment.
#
# Example Usage:
#   ./print_build_env.py
#

BIN_DIR = os.path.dirname(__file__)
webrtc_src_dir = os.path.join(BIN_DIR, '../webrtc/src')

@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)

def determine_git_branch(directory):
    with pushd(directory):
        git_branch_output = subprocess.check_output(["git", "branch"])
        git_branch = [line.replace("* ", "") for line in git_branch_output.split("\n") if re.search("^\*", line)][0]
        return git_branch

def determine_git_sha(directory):
    with pushd(directory):
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip("\n")

def get_build_details():
    template = Template("""## WebRTC Build Details

To track down potential future issues, we log some of our build environment details.

webrtc git branch:
$webrtc_git_branch

webrtc git sha:
$webrtc_git_sha

build_script git sha:
$build_script_git_sha

xcodebuild -version:
$xcode_version

xcode-select -p:
$xcode_path

gcc -v:
$gcc_version

osx_version_details:
$osx_version_details

hostname:
$hostname
""")

    webrtc_git_branch = determine_git_branch(webrtc_src_dir)
    webrtc_git_sha = determine_git_sha(webrtc_src_dir)
    build_script_git_sha = determine_git_sha("./")
    xcode_version = subprocess.check_output(["xcodebuild", "-version"]).strip("\n")
    xcode_path = subprocess.check_output(["xcode-select", "-p"]).strip("\n")
    gcc_version = subprocess.check_output(["gcc", "-v"], stderr=subprocess.STDOUT).strip("\n")
    osx_version_details = subprocess.check_output(["sw_vers"]).strip("\n")
    hostname = subprocess.check_output(["hostname"]).strip("\n")

    details = template.substitute(
            webrtc_git_branch = webrtc_git_branch,
            webrtc_git_sha = webrtc_git_sha,
            build_script_git_sha = build_script_git_sha,
            xcode_version = xcode_version,
            xcode_path = xcode_path,
            gcc_version = gcc_version,
            osx_version_details = osx_version_details,
            hostname = hostname
    )

    return details

def main():
    print(get_build_details())

if __name__ == "__main__":
    main()
