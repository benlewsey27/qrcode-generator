# Changelog
All notable changes to this project will be documented in this file.

## [0.6.0]
- [generate-service] Added initial QR code generation functionality
- [generate-service] Added option to save QR code to local file
- [public-api] Added local file functionality for fetch endpoint

## [0.5.0]
- [public-api] Use 16 character lowercase alphanumeric code for request id

## [0.4.0]
- [status-service] Added redis integration via helper class
- [status-service] Added initial API to get and update status changes
- [public-api] Added status service integration for generate and status endpoints

## [0.3.0]
- [generate-service] Added kafka integration via helper class
- [generate-service] Added kafka consumer to receive messages when a QR code is requested

## [0.2.0]
- [public-api] Added kafka integration via helper class
- [public-api] Added kafka producer to send messages when a QR code is requested

## [0.1.0]
- [public-api] Added initial generate, fetch and status endpoint structure
- [public-api] Created custom plugin to mute healthcheck logs
