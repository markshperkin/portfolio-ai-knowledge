# CameraXApp — Overview

## What It Is

An **Android camera and image-editing app** built in Kotlin. Lets users capture photos and videos, pick images from the device gallery, and apply editing modifications. Built as part of Android development coursework at USC.

GitHub: https://github.com/markshperkin/CameraXApp

## What It Does

Three primary capabilities:

- **Photo and video capture** — direct capture from the device camera using Android's CameraX API
- **Gallery integration** — select images from the device's photo library via a third-party `ImagePicker` library
- **Image editing** — apply various modification features to selected images

The app builds on a starter application by Robert Bailey, which provided the base camera and video capture functionality. I extended it with gallery selection and custom image editing features.

## Why CameraX

**CameraX** is Android's modern camera library — a Jetpack component designed to be the unified, simpler replacement for the older Camera and Camera2 APIs. It handles:

- Device-specific camera quirks
- Lifecycle integration (start/stop with the Activity/Fragment)
- Common use cases (preview, image capture, video capture, image analysis)

Before CameraX, Android camera development was famously painful — different OEMs implemented Camera/Camera2 with subtle inconsistencies. CameraX abstracts most of that away.

## Tech Stack

- **Language**: Kotlin (100%)
- **Camera framework**: Android CameraX
- **Image picker library**: `ImagePicker` (third-party Android library for gallery selection)
- **Build**: Gradle

## My Specific Contributions

The starter app from Robert Bailey provided basic photo and video capture. I extended it with:

### 1. Gallery Image Selection
Integrated the third-party `ImagePicker` library to let users pick existing images from their gallery. This required:
- Library integration via Gradle
- Result-handling for the picker's return
- Display of the selected image in the app's UI

### 2. Custom Image Editing
Added editing features that operate on the selected/captured images. Editing operations and the exact UI for them were my custom work on top of the camera foundation.

## Why I Built It

This was coursework, but the skills it taught are genuinely valuable:

- Working with Android's media frameworks
- Handling permissions for camera and storage access
- Lifecycle-aware components (CameraX is built around lifecycle)
- Image processing on Android
- Integrating third-party libraries
- Building atop a starter codebase (a common real-world scenario)

## Attribution

The README explicitly credits:
- **Robert Bailey's starter application** as the foundational base
- **ImagePicker library** for gallery functionality

Honest attribution is part of how academic and open-source software works. The starter gave us a working camera app; my work extended it with selection and editing.

## My Role

Sole owner of my extensions. Started from Robert Bailey's starter code (provided by my Android course) and built the gallery integration and editing features.

## Keywords

CameraXApp, Android, Kotlin, CameraX API, Jetpack, photo capture, video capture, ImagePicker library, gallery integration, image editing, image processing, mobile development, USC coursework, Robert Bailey starter app, third-party library integration
