# Pyffice Documentation

Comprehensive documentation for the Pyffice unified office automation framework.

## Quick Links

- [README](../README.md) - Project overview
- [CLI Reference](CLI.md) - Command-line interface
- [Agent Guidelines](../AGENT.md) - Development patterns
- [Changelog](../CHANGES.md) - Version history

## Modules

### Document Processing
- `document.py` - Core document handling
- `script/` - Script execution
- `ebook/` - EPUB, AZW, MOBI support

### Media
- `images/` - Image processing (PNG, JPG, GIF, BMP, WEBP, HEIC)
- `video/` - Video handling (MP4, AVI, MKV, MOV)
- `audio/` - Audio processing (MP3, WAV, FLAC, OGG)
- `cad/` - CAD file support (DXF, DWG)

### Data
- `matrix/` - Spreadsheet operations
- `databases/` - Database connectivity
- `analytics/` - Data analytics
- `reports/` - Report generation

### Communication
- `email/` - SMTP/IMAP email
- `calendars/` - Calendar events
- `contacts/` - Contact management
- `socials/` - Social media integration

### Automation
- `workflows/` - Workflow automation
- `script/` - Script execution
- `forms/` - Form handling

### Utilities
- `web/` - Web utilities
- `tags/` - Tagging system
- `config/` - Configuration
- `updates/` - Update management

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
pylint pyffice/
```

### CLI Help
```bash
pyffice --help
```
