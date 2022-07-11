# Changelog
All notable changes to this project will be documented in this file.

## [1.0.0-beta]
**public-api**
- Added initial generate, fetch and status endpoint structure
- Created custom plugin to mute healthcheck logs
- Added kafka integration via helper class
- Added kafka producer to send messages when a QR code is requested
- Added status service integration for generate and status endpoints
- Use 16 character lowercase alphanumeric code for request id
- Added local file functionality for fetch endpoint

**generate-service**
- Added kafka integration via helper class
- Added kafka consumer to receive messages when a QR code is requested
- Added option to save QR code to local file
- Added initial QR code generation functionality

**status-service**
- Added redis integration via helper class
- Added initial API to get and update status changes
- Added support for redis passwords
