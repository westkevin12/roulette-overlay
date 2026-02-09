# Release Notes: Fixed Icon Loading

## Title
v1.1.0 - Fixed Icon Loading

## Description
This release fixes an issue where the application icon would fail to load when running the executable on some systems.

### Changes
- Fixed relative path (icon) loading issue by implementing a `resource_path` helper function.
- Verified support for both standard and CustomTkinter versions.
