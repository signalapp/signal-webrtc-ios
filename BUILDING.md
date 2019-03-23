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

    git clone https://github.com/signalapp/signal-webrtc-ios
    cd signal-webrtc-ios

    # Fetch the webrtc src root plus our shared patches
    git submodule update --init

    # Install webrtc submodules specified in DEPS
    cd webrtc
    gclient sync

    # This process dirties the working directory. If this is your first build,
    # you can skip this step. Otherwise we want to make sure we start from a
    # pristine webrtc dir.
    ../bin/clean_webrtc.py

## Updating WebRTC.framework (optional)

This section is only required if you want to use a newer version.
based on: https://www.chromium.org/developers/how-tos/get-the-code/working-with-release-branches

    # Make sure you are in 'signal-webrtc-ios/webrtc/src'.

    # The first time your run this might take a while because it fetches
    # an extra 1/2 GB or so of branch commits.
    gclient sync --with_branch_heads

    # OPTIONAL: If that failed, try repeating after running fetch
    git fetch
    gclient sync --with_branch_heads

    # List available branch heads
    git branch -a

    # Checkout the branch 'src' tree.
    # You can find a list of release notes here: https://webrtc.org/release-notes/
    git checkout branch-heads/$LATEST_STABLE_RELEASE_NUMBER

    # Checkout all the submodules at their branch DEPS revisions.
    gclient sync --jobs 16

    # Clean up anything that's since been removed from upstream.
    git clean -df

## Building WebRTC.framework

Finally. Why we're all here.

    # Apply Signal Patches
    ../../bin/apply_signal_patches

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

    # Move the WebRTC.framework into Signal-iOS's Carthage directory. We don't actually
    # use Carthage to build WebRTC, but we use some Carthage scripts to prepare the library
    # for distribution.
    mv out_ios_libs/WebRTC.framework $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS/

    # Make sure we add any new files, since we gitignore *
    cd $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS
    git add -f WebRTC.framework

