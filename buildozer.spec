[app]
title = Vision
package.name = vision
package.domain = org.local
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,ini
version = 0.1.0
requirements = python3,kivy,opencv-python,Pillow,numpy,bcrypt,face_recognition,dlib
orientation = portrait
fullscreen = 0

android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.ndk = 25b
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 0
