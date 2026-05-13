# CameraXApp — Implementation Notes

## CameraX Setup

CameraX is Android's modern camera Jetpack component. The basic setup involves:

### 1. Add CameraX Dependencies
In `build.gradle`:
```gradle
implementation "androidx.camera:camera-core:..."
implementation "androidx.camera:camera-camera2:..."
implementation "androidx.camera:camera-lifecycle:..."
implementation "androidx.camera:camera-video:..."
implementation "androidx.camera:camera-view:..."
```

### 2. Camera Permissions
Standard runtime permissions for `CAMERA` and (for video) `RECORD_AUDIO` and `WRITE_EXTERNAL_STORAGE` (or scoped storage on newer Android).

### 3. Preview Setup
A `PreviewView` in the layout shows the live camera feed. Bind it to a CameraX `Preview` use case in the Activity:
```kotlin
val preview = Preview.Builder().build().also {
    it.setSurfaceProvider(viewFinder.surfaceProvider)
}
```

### 4. Capture Use Cases
Image capture and video capture are separate use cases:
```kotlin
val imageCapture = ImageCapture.Builder().build()
val videoCapture = VideoCapture.Builder().build()
```

### 5. Bind to Lifecycle
CameraX is lifecycle-aware. Bind the use cases to a lifecycle owner:
```kotlin
cameraProvider.bindToLifecycle(
    this,
    cameraSelector,
    preview,
    imageCapture,
    videoCapture
)
```

This ensures the camera starts/stops automatically with the Activity lifecycle. No manual `release()` needed.

## Gallery Integration with ImagePicker

The third-party `ImagePicker` library simplifies the gallery selection flow. Without it, you'd have to:
- Create an `Intent` with `ACTION_PICK`
- Launch it for result
- Handle the result Uri
- Convert the Uri to a usable image

`ImagePicker` wraps all this in a fluent API:
```kotlin
ImagePicker.with(this)
    .galleryOnly()
    .compress(1024)
    .start()
```

The result is delivered to `onActivityResult`, where you can grab the selected image's path or Uri.

## Image Editing Features

The editing layer takes a captured or selected image and applies modifications. Common operations include:
- Cropping
- Rotation
- Brightness / contrast / saturation adjustments
- Filters (grayscale, sepia, etc.)
- Drawing on top of the image

Implementation typically uses Android's `Bitmap` and `Canvas` APIs for in-app editing, or a third-party library for richer features.

## Key Challenges

### Camera Lifecycle
The camera must be released when the Activity is paused/stopped, or you'll get errors when it tries to reopen. CameraX handles this automatically via the lifecycle binding, but pre-CameraX patterns required manual management.

### Image Orientation
Mobile photos often have EXIF orientation metadata that doesn't match the actual pixel orientation. If you don't read and apply the EXIF rotation, your displayed image is sideways. This bites everyone exactly once.

### Storage and File Paths
Modern Android (10+) uses scoped storage. You can't just write to `/sdcard/` anymore. Saved images need to use:
- The app's private directory (no permissions needed)
- The MediaStore API (for sharing with other apps)
- A `ContentProvider` for fine-grained access control

### Aspect Ratios
The camera preview, the captured image, and the display may have different aspect ratios. Center-cropping vs. letterboxing requires care.

## Why Building on a Starter App Is Realistic

This project mirrors a real-world software situation: most engineers don't start from scratch. They inherit codebases, fork starter projects, or pick up where someone else left off.

Skills exercised:
- Reading and understanding someone else's code
- Identifying the seams where new features fit
- Integrating new libraries without breaking existing functionality
- Respecting the original architecture even when extending it

## Lessons Learned

### CameraX Is Worth It
The pre-CameraX Android camera ecosystem was famously inconsistent. CameraX consolidates and simplifies. For any new Android camera work, default to CameraX.

### Lifecycle Awareness Is Pervasive
CameraX, location services, network requests, observers — all of them benefit from lifecycle-awareness. Learning Android's lifecycle deeply is one of the highest-leverage skills for the platform.

### Third-Party Libraries Have Tradeoffs
`ImagePicker` saves a ton of boilerplate but introduces a dependency. For a coursework project, that's fine. For a production app, consider whether the dependency is worth it (maintenance burden, security implications, build size).

### Image Processing Is a World of Edge Cases
Orientation, color space, compression artifacts, memory pressure — image processing on Android is a deep topic. A coursework project barely scratches the surface.

## What I'd Add If I Continued

- Real-time filters during preview (using ML Kit or OpenCV)
- More editing operations (cropping, rotation, drawing)
- Cloud upload integration
- Sharing to other apps via Android share sheets
- Photo metadata viewing/editing

## Connection to Other Projects

This project, along with MiniPaint, Sensor-Game-Application, and Location, were all part of my Android development sequence. Each built skills that compound:
- Permissions handling
- Activity lifecycle
- UI patterns
- Library integration

Together they gave me solid Android fundamentals — relevant later if I ever build mobile apps for ML model deployment.

## Keywords

CameraX, Android Jetpack, photo capture, video capture, lifecycle binding, PreviewView, ImagePicker library, gallery selection, image editing, Bitmap manipulation, Canvas API, EXIF orientation, scoped storage, MediaStore, third-party library integration, starter app, Robert Bailey, USC Android coursework
