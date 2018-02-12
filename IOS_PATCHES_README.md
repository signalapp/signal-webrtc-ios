Patches required to build webrtc for Signal on iOS

## Current Patches

### patch file: ios-patches/004_metalkit_aspect_fill.diff

The MetalKit backed video renderer is currently hardcoded to AspectFit,
which causes letterboxing for our fullscreen video preview. This fix was
suggested on the mailing list, and may be unnecessary in future
versions.

https://groups.google.com/forum/#!searchin/discuss-webrtc/RTCMTLVideoView%7Csort:relevance/discuss-webrtc/Fn4Q0dUranY/1YZApRVWAwAJ

### patch file:   ios-patches/003_support_ios8.diff

In M58 WebRTC introduced MetalKit backed rendering, which enables a
higher-performance (lower power consumption) video renderer. However,
MetalKit isn't available on iOS8 and since WebRTC doesn't officially
support iOS8, we were crashing on launch.

Changes to support iOS8 include:
 - Having a runtime check to see if MetalKit is available before
   instantiating anything from MetalKit.
 - Ensure the MetalKit dylib is loaded "weakly" be specifying iOS8 as the minimum
   deployment target.
 - Adding "@availability" checks as necessary to satisfy the compiler
   after changing the minimum deployment target.

## Retired Patches

### patch file: 002_issue2832803002_20001.diff

There is a build error when building Signal-iOS because some of the
headers referenced in the frameworks public headers are themselves, not
public.

Read more at:
https://codereview.webrtc.org/2832803002

This is fixed in WebRTC master and this patch can be removed in WebRTC
version >= 60

### patch file:   ios-patches/001_issue2833833002_1_10001.diff

There is an error when building WebRTC.framework in XCode 8.3. This
should be resolved in WebRTC version >=60. At which point we should
remove the patch.

Patch downloaded from:
https://codereview.chromium.org/2833833002

Read more at:
https://bugs.chromium.org/p/webrtc/issues/detail?id=7481
https://chromium.googlesource.com/chromium/src/+/b1eb09e2deb0335502f6b744a902dd0251a209f3

