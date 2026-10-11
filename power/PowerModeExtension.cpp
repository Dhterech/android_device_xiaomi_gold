/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <dirent.h>
#include <fcntl.h>
#include <linux/input.h>
#include <sys/ioctl.h>
#include <unistd.h>

#include <memory>
#include <string>

#include <aidl/android/hardware/power/BnPower.h>
#include <android-base/logging.h>
#include <android-base/unique_fd.h>

namespace aidl::google::hardware::power::impl::pixel {

using ::aidl::android::hardware::power::Mode;

namespace {

constexpr char kInputDir[] = "/dev/input";

// Xiaomi touch drivers switch double tap to wake when one of these values is
// written to their input device as an EV_SYN/SYN_CONFIG event. Both drivers
// gold is built with take it: FocalTech ("fts_ts") and Goodix ("goodix_ts").
constexpr int32_t kWakeupModeOff = 4;
constexpr int32_t kWakeupModeOn = 5;

bool IsTouchscreen(int fd) {
    char name[80] = {};
    if (ioctl(fd, EVIOCGNAME(sizeof(name) - 1), name) < 0) {
        return false;
    }
    const std::string device(name);
    return device == "fts_ts" || device == "goodix_ts";
}

void SetDoubleTapToWake(bool enabled) {
    std::unique_ptr<DIR, int (*)(DIR*)> dir(opendir(kInputDir), closedir);
    if (!dir) {
        PLOG(ERROR) << "Cannot open " << kInputDir;
        return;
    }

    bool found = false;
    while (const dirent* entry = readdir(dir.get())) {
        if (entry->d_type != DT_CHR) {
            continue;
        }
        const std::string path = std::string(kInputDir) + "/" + entry->d_name;
        ::android::base::unique_fd fd(open(path.c_str(), O_RDWR | O_CLOEXEC));
        if (fd < 0 || !IsTouchscreen(fd.get())) {
            continue;
        }
        found = true;

        input_event event{};
        event.type = EV_SYN;
        event.code = SYN_CONFIG;
        event.value = enabled ? kWakeupModeOn : kWakeupModeOff;
        if (TEMP_FAILURE_RETRY(write(fd.get(), &event, sizeof(event))) != sizeof(event)) {
            PLOG(ERROR) << "Cannot switch double tap to wake on " << path;
        }
    }
    if (!found) {
        LOG(WARNING) << "No known touchscreen to switch double tap to wake on";
    }
}

}  // namespace

bool isDeviceSpecificModeSupported(Mode type, bool* _aidl_return) {
    if (type == Mode::DOUBLE_TAP_TO_WAKE) {
        *_aidl_return = true;
        return true;
    }
    return false;
}

bool setDeviceSpecificMode(Mode type, bool enabled) {
    if (type == Mode::DOUBLE_TAP_TO_WAKE) {
        SetDoubleTapToWake(enabled);
        return true;
    }
    return false;
}

}  // namespace aidl::google::hardware::power::impl::pixel
