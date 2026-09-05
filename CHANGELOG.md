# Changelog

All notable changes to this project are documented here.

## [0.0.1.0] - 2026-09-05

### Added

- README explaining how to use the password strength checker, with the safer
  stdin-piped invocation shown first and a note on why (command-line arguments
  can leak into shell history and process listings).

### Changed

- Ignored a stray session lock file so it never gets committed.
