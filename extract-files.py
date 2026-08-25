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
#    'hardware/mediatek/libaedv',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]

blob_fixups: blob_fixups_user_type = {
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek', 'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    ('vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron', 'vendor/lib64/libnvram.so', 'vendor/lib64/libsysenv.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/bin/hw/android.hardware.security.keymint@1.0-service.mitee': blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so')
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so', 'android.hardware.security.keymint-V3-ndk.so')
        .replace_needed('android.hardware.security.sharedsecret-V1-ndk_platform.so', 'android.hardware.security.sharedsecret-V1-ndk.so')
        .replace_needed('android.hardware.security.secureclock-V1-ndk_platform.so', 'android.hardware.security.secureclock-V1-ndk.so'),
    'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    #('vendor/bin/mnld', 'vendor/lib64/libcam.utils.sensorprovider.so', 'vendor/lib64/libaalservice.so'): blob_fixup()
    #    .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib64/libcam.utils.sensorprovider.so',
        'vendor/lib64/libaalservice.so',
    ): blob_fixup()
        .replace_needed(
            'android.frameworks.sensorservice-V1-ndk.so',
            'android.frameworks.sensorservice-V1-ndk-vendor-compat.so',
        )
        .replace_needed(
            'android.hardware.sensors-V2-ndk.so',
            'android.hardware.sensors-V2-ndk-vendor-compat.so',
        )
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/android.frameworks.sensorservice-V1-ndk-vendor-compat.so': blob_fixup()
        .replace_needed(
            'android.hardware.sensors-V2-ndk.so',
            'android.hardware.sensors-V2-ndk-vendor-compat.so',
        ),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/libgoodixhwfingerprint.so': blob_fixup()
        .replace_needed('libvendor.xiaomi.hardware.fx.tunnel@1.0.so', 'vendor.xiaomi.hardware.fx.tunnel@1.0.so'),
    ('vendor/lib64/libcam.hal3a.v3.so', 'vendor/lib64/hw/hwcomposer.mtk_common.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    'vendor/lib64/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    (
        "vendor/lib64/libteei_daemon_vfs.so",
        "vendor/lib64/lib3a.flash.so",
        "vendor/lib64/libaaa_ltm.so",
        "vendor/lib64/lib3a.ae.stat.so",
        "vendor/lib64/lib3a.sensors.color.so",
        "vendor/lib64/lib3a.sensors.flicker.so",
    ): blob_fixup()
        .add_needed("liblog.so"),
    'vendor/lib/libvcodec_oal.so': blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),

    # From device_xiaomi_duchamp
        'vendor/lib64/libmtkcam_hal_aidl_common.so': blob_fixup()
        .replace_needed('android.hardware.camera.common-V2-ndk.so', 'android.hardware.camera.common-V1-ndk.so'),

    # From android_device_motorola_mt6768-common
    (
        'vendor/bin/hw/android.hardware.graphics.allocator-V2-service-mediatek',
        'vendor/lib64/egl/libGLES_mali.so',
        'vendor/lib64/hw/android.hardware.graphics.allocator-V2-mediatek.so',
        'vendor/lib64/hw/mapper.mediatek.so',
        'vendor/lib64/libcodec2_fsr.so',
        'vendor/lib64/libgpud.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
        'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),

    # From device_xiaomi_duchamp, adapted because we V5 - V7
        ('vendor/lib64/libmtkcam_grallocutils.so',
     'vendor/lib64/libmtkcam_grallocutils_aidlv1helper.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    
    ('vendor/lib/libcodec2_fsr.so',
    'vendor/lib/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
    'vendor/lib/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
    'vendor/lib64/egl/libGLES_mali.so',
    'vendor/lib64/libcodec2_fsr.so',
    'vendor/lib64/libgpud.so',
    'vendor/lib64/libmtkcam_grallocutils.so',
    'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
    'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
    'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so'): blob_fixup()
            .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    #    .replace_needed('libui.so', 'libui-v34.so'),

    # From android_device_xiaomi_rosemary
    ('vendor/lib64/libMiVideoFilter.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

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
