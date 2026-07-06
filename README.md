# Pyffice

**Unified Python Office Automation & Productivity Suite**

Pyffice provides a unified Python interface for document processing, CAD, media handling, email, calendar, and comprehensive office automation with an extensible port architecture.

---

## Features

### Document Processing
- **Word Processing**: DOC, DOCX, ODT, RTF, PDF, LaTeX
- **Spreadsheets**: XLS, XLSX, ODS, CSV
- **Presentations**: PPT, PPTX, ODP
- **Ebooks**: EPUB, MOBI, AZW
- **Technical**: Markdown, reStructuredText, AsciiDoc

### Media Handling
- **Images**: PNG, JPG, GIF, BMP, WEBP, HEIC, SVG, TIFF
- **Video**: MP4, AVI, MKV, MOV, WEBM
- **Audio**: MP3, WAV, FLAC, OGG, M4A, AAC
- **CAD**: DXF, DWG (limited)

### Office Integration
- **Email**: SMTP/IMAP with send/receive capabilities
- **Calendar**: iCal support with event management
- **Contacts**: Contact management and search
- **Tasks**: Task and project tracking

### Automation & Workflows
- **Workflows**: Custom workflow creation and execution
- **Scripts**: Python script execution framework
- **CLI**: 72+ command-line operations
- **Ports**: Extensible architecture for custom integrations

### Data & Analytics
- **Charts**: Chart generation and visualization
- **Analytics**: Data analytics and reporting
- **Databases**: Database connectivity (SQLite, PostgreSQL)
- **Matrix**: Matrix operations and calculations

### Web & Utilities
- **Web**: URL fetching, parsing, scraping
- **Forms**: Form creation and validation
- **Tags**: Tagging system for organization
- **Filesystems**: Virtual filesystem management

---

## Installation

### From PyPI
```bash
pip install pyffice
```

### From Source
```bash
git clone https://github.com/solubrew/pyffice.git
cd pyffice
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/solubrew/pyffice.git
cd pyffice
pip install -e ".[dev]"
pip install pylint pytest bandit
```

---

## Quick Start

### CLI Usage

```bash
# Document operations
pyffice document convert input.docx output.pdf
pyffice document info input.docx

# Spreadsheet operations
pyffice spreadsheet convert data.xlsx data.csv
pyffice spreadsheet info data.xlsx

# Media operations
pyffice image convert photo.png photo.jpg
pyffice video convert video.mov video.mp4
pyffice audio convert audio.wav audio.mp3

# Email operations
pyffice email send --to user@example.com --subject "Hello" --body "Message"

# Calendar operations
pyffice calendar list
pyffice calendar add --title "Meeting" --date 2026-06-25

# Workflow operations
pyffice workflow run my-workflow
pyffice workflow list
```

### Python API

```python
from pyffice import Pyffice

# Initialize
app = Pyffice()

# Document processing
app.document.convert("input.docx", "output.pdf")

# Media conversion
app.image.convert("photo.png", "photo.jpg")
app.video.convert("video.mov", "video.mp4")

# Email
app.email.send(
    to="user@example.com",
    subject="Hello",
    body="Message"
)

# Calendar
events = app.calendar.list()

# Workflow
app.workflow.run("my-workflow")
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [CLI.md](CLI.md) | Complete CLI command reference |
| [AGENT.md](AGENT.md) | Agent system documentation |
| [STATE.md](STATE.md) | Project state and roadmap |
| [CHANGES.md](CHANGES.md) | Changelog and release notes |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## Architecture

### Port System

Pyffice uses a flexible port architecture for extensibility:

```python
from pyffice.ports import DocumentPort, ImagePort, MediaPort

# Create custom document handler
class MyHandler(DocumentPort):
    def read(self, path):
        # Custom implementation
        pass
    
    def write(self, path, content):
        # Custom implementation
        pass
```

### Module Structure

```
pyffice/
├── calendars/      # Calendar & event management
├── charts/         # Chart generation
├── config/         # Configuration management
├── contacts/       # Contact management
├── filesystems/    # Virtual filesystem
├── forms/          # Form handling
├── images/         # Image processing
├── items/          # Item utilities & colors
├── matrix/         # Matrix operations
├── notebooks/      # Jupyter notebooks
├── ports/          # Extensible port system
├── script/         # Script execution
├── skills/         # Skill framework
├── tags/           # Tagging system
├── updates/        # Update management
├── web/            # Web utilities
├── workflows/      # Workflow automation
├── cli.py          # CLI interface (72 commands)
├── document.py     # Document processing
└── pyffice.py      # Main entry point
```

---

## Configuration

Create `pyffice.yaml` in your project root:

```yaml
# General settings
general:
  debug: false
  log_level: INFO

# Email configuration
email:
  smtp_host: smtp.gmail.com
  smtp_port: 587
  imap_host: imap.gmail.com
  imap_port: 993

# Database configuration
database:
  default: sqlite
  connections:
    sqlite:
      path: ./data/pyffice.db
    
# Workflow configuration
workflows:
  default_timeout: 3600
  max_parallel: 4
```

---

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Linting
pylint pyffice/

# Security
bandit -r pyffice/

# Type checking
pyright pyffice/
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Coding standards
- Pull request workflow
- Release process

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Support

- **Issues**: https://github.com/solubrew/pyffice/issues
- **Discussions**: https://github.com/solubrew/pyffice/discussions
