# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.1.0] - 2023-05-12

Initial release!

### Added

- A function that reads the environment and returns a `DATABASES` setting for a multi-region Fly Postgres database
- A router that routes reads to a replica database if the `DATABASES` setting has a `replica` key
- A middleware that sets the `Fly-Server` header containing the Fly server and region that served the request
- Initial documentation (README.md)
- Initial tests
- Initial CI/CD (GitHub Actions)

[unreleased]: https://github.com/joshuadavidthomas/django-flyio/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/joshuadavidthomas/django-flyio/releases/tag/v0.1.0
