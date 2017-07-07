### Building WebRTC

A prebuilt version of WebRTC.framework resides in the Signal Carthage submodule
However, if you'd like to build it from source, with our modifications see below.

These instructions are derived from the WebRTC documentation:

https://webrtc.org/native-code/ios/

Initial Setup for first time building WebRTC.framework

    # 1. Installation prerequisites

    # depot tools
    cd <somewhere>
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    cd depot_tools
    export PATH=<somewhere>/depot_tools:"$PATH"

    # 2. Fetch webrtc source
    cd signal-webrtc-ios
    mkdir webrtc
    cd webrtc
    fetch --nohooks webrtc_ios

The remaining steps must occur every time you're building/updating WebRTC.framework

    # 3. Point to appropriate release
    #
    # based on:
    #    https://www.chromium.org/developers/how-tos/get-the-code/working-with-release-branches

    # Make sure you are in 'webrtc/src'.
    #
    # This part should only need to be done once, but it won't hurt to
    # repeat it.  The first time might take a while because it fetches
    # an extra 1/2 GB or so of branch commits.
    gclient sync --with_branch_heads

    # You may have to explicitly 'git fetch origin' to pull branch-heads/
    git fetch

    # Checkout the branch 'src' tree.
    git checkout branch-heads/$LATEST_STABLE_RELEASE_NUMBER

    # Checkout all the submodules at their branch DEPS revisions.
    gclient sync --jobs 16

    # 4. Apply Signal Patches
    # NOTE: If you've previosly applied the patches, they won't apply
    # cleanly. Start from a pristine clean webrtc dir.
    ../../bin/apply-signal-patches

    # 5. Build WebRTC.framework
    # Finally. Why we're all here.
    tools-webrtc/ios/build_ios_libs.sh

    # If you get errors about missing build tools, like 'gn', you may be
    # able to install them with the following (then go back to "Build
    # WebRTC.framework" step:
    gclient runhooks

    # 6. Move the WebRTC.framework into Signal-iOS's Carthage directory
    rm -r $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS/WebRTC.framework
    mv out_ios_libs/WebRTC.framework $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS/

    # Make sure we add any new files, since we gitignore *
    cd $SIGNAL_IOS_REPO_ROOT/Carthage/Build/iOS
    git add -f WebRTC.framework

