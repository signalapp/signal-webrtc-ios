ROOT_DIR=./
WEBRTC_SRC_DIR=webrtc/src
BUILD_ARTIFACTS_DIR=./Builds/Build

default: full_build

full_build: clean sync update_tools archive
fast_build: clean sync archive

clean:
	bin/clean_webrtc.py

patch:
	bin/apply_signal_patches

sync:
	cd $(WEBRTC_SRC_DIR) && \
		gclient sync --jobs 16

# This step can be really slow, as it downloads a ton of resources into the
# webrtc/src directory. Subsequent calls are quick, so long as you don't blow
# away the downloaded resources. Thus our `make clean` attempts to only clean
# things that are changed by our build process, at the expense of some robustness
update_tools:
	cd $(WEBRTC_SRC_DIR) && \
		gclient runhooks --jobs 16

build: 
	$(WEBRTC_SRC_DIR)/tools_webrtc/ios/build_ios_libs.sh

log_build_env:
	bin/print_build_env.py > webrtc/src/out_ios_libs/WebRTC.framework/build_env.txt

archive: patch build log_build_env 
	rm -fr $(BUILD_ARTIFACTS_DIR)/WebRTC.framework && \
	mv $(WEBRTC_SRC_DIR)/out_ios_libs/WebRTC.framework $(BUILD_ARTIFACTS_DIR)
