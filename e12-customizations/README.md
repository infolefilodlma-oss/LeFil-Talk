# E12 Customizations for Le Fil Echo

This directory contains the Le Fil Echo (E12) customization files for FluffyChat 2.11.5.

## Files

- `lib/pages/intro/intro_page.dart` - Le Fil Echo branded intro page with French text and links
- `assets/logo/mini/le_fil_echo_logo.jpg` - Le Fil Echo logo

## Usage

These files are applied by the GitHub Actions workflow to override the default FluffyChat files during the web build process.

The workflow:
1. Clones FluffyChat 2.11.5
2. Applies these E12 customizations
3. Verifies file integrity
4. Compiles the web version

## Build via GitHub Actions

The build is triggered manually from the main branch workflow on GitHub Actions.
