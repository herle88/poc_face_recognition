# DeepFace Recognition Add-on

## Overview

This add-on provides a web-based face recognition tool powered by [DeepFace](https://github.com/serengil/deepface). Upload images, run face analysis, and the system will group images by unique person.

## How to use

1. Install the add-on from the Home Assistant add-on store
2. Start the add-on
3. Click "Open Web UI" in the add-on info panel
4. Upload images using drag-and-drop or the file picker
5. Adjust settings if needed (model, detector, thresholds)
6. Click "Run Analysis" to identify and group faces

## Settings

The analysis settings panel (click to expand) offers:

- **Model**: Face recognition model (VGG-Face, Facenet, ArcFace, etc.)
- **Detector**: Face detection backend (opencv, mtcnn, retinaface, ssd)
- **Distance Threshold**: How similar faces must be to match (higher = more lenient)
- **Min Confidence**: Filter out low-confidence face detections

## Data

All uploaded images and the SQLite database are stored in the add-on's persistent `/data` directory and survive add-on restarts and updates.

## First run

The first analysis will download the selected face recognition model (~500MB for VGG-Face). This is a one-time download per model.
