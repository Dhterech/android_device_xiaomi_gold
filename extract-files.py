#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/gold',
    'hardware/mediatek',
    'hardware/xiaomi',
]

blob_fixups: blob_fixups_user_type = {
    'vendor/bin/hw/android.hardware.security.keymint@1.0-service.mitee': blob_fixup()
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    'vendor/etc/init/android.hardware.media.c2@1.2-mediatek-64b.rc': blob_fixup()
        .regex_replace('mediatek', 'mediatek-64b'),
}  # fmt: skip

module = ExtractUtilsModule(
    'gold',
    'xiaomi',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
