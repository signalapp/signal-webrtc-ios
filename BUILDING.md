### Building WebRTC

A prebuilt version of WebRTC.framework resides in the Signal Carthage submodule
However, if you'd like to build it from source, with our modifications see below.

These instructions are derived from the WebRTC documentation:

https://webrtc.org/native-code/ios/

Initial Setup for first time building WebRTC.framework

## Installation prerequisites

### Apple Dev Tools

**Note** currently building WebRTC requires Xcode9+

### Install depot tools

    cd <somewhere>
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    cd depot_tools
    export PATH=<somewhere>/depot_tools:"$PATH"

## Fetch WebRTC source

    git clone https://github.com/WhisperSignal/signal-webrtc-ios
    cd signal-webrtc-ios

    # Fetch the webrtc src root plus our shared patches
    git submodule update --init

    # Install webrtc submodules specified in DEPS
    cd webrtc
    gclient sync

## Updating WebRTC.framework (optional)

This section is only required if you want to use a newer version.
based on: https://www.chromium.org/developers/how-tos/get-the-code/working-with-release-branches

    # This process dirties the working directory. Start from a pristine
    # clean webrtc dir.
    ../../bin/clean_webrtc.py

    # Make sure you are in 'signal-webrtc-ios/webrtc/src'.
    #
    # The first time your run this might take a while because it fetches
    # an extra 1/2 GB or so of branch commits.
    gclient sync --with_branch_heads

    # You may have to explicitly 'git fetch origin' to pull branch-heads/
    git fetch

    # List available branch heads
    git branch -a

    # Checkout the branch 'src' tree.
    git checkout branch-heads/$LATEST_STABLE_RELEASE_NUMBER

    # Checkout all the submodules at their branch DEPS revisions.
    gclient sync --jobs 16

    # Apply Signal Patches
    ../../bin/apply_signal_patches

## Building WebRTC.framework

Finally. Why we're all here.

    # the webrtc project includes a script to build a fat framework for arm/arm64/i386/x86_64
    # NOTE: the i386 build is currently broken, so you can't run iPhone5 simulators
    tools_webrtc/ios/build_ios_libs.sh

    # If you get errors about missing build tools, like 'gn', you may be
    # able to install them with the following (then go back to "Building
    # WebRTC.framework" step:
    gclient runhooks

# Integrate into Signal

    # Remove the existing directory to make sure any obsolete files are removed
    rm -r $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS/WebRTC.framework

    # move the WebRTC.framework into Signal-iOS's Carthage directory
    mv out_ios_libs/WebRTC.framework $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS/

    # Make sure we add any new files, since we gitignore *
    cd $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS
    git add -f WebRTC.framework

