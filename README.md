# Pyffice

Pyffice is a Python wrapper for an expanded catalog of open-source office suite tools, built on YAML configurations for each document type. It provides a unified interface to interact with various office document formats using underlying open-source libraries, allowing seamless creation, editing, and manipulation of documents like word processors, spreadsheets, presentations, and more.

## Features

- **YAML-Based Configuration**: Define document structures, styles, and operations using simple YAML files tailored to specific document types (e.g., .docx, .xlsx, .pptx).
- **Wrapper for Open-Source Tools**: Integrates with libraries such as <LIB_WORD> for word processing, <LIB_SPREAD> for spreadsheets, and <LIB_PRESENT> for presentations.
- **Extensible Catalog**: Easily add support for new document types or tools by extending the YAML configs.
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux.
- **API Simplicity**: High-level Pythonic API to abstract complex operations.

## Installation

You can install Pyffice via pip:

```bash
pip install pyffice
```

Alternatively, clone the repository and install from source:

```bash
git clone https://github.com/<USER_OR_ORG>/pyffice.git
cd pyffice
pip install -e .
```

### Requirements

- Python 3.<MIN_VERSION> or higher
- Dependencies: pyyaml, <DEP_LIB1>, <DEP_LIB2> (automatically installed via pip)

## Quick Start

Import the module and load a YAML configuration:

```python
import pyffice

# Load YAML config for a document type
config = pyffice.load_config('path/to/word.yaml')

# Create a new document
doc = pyffice.Document(config)

# Add content
doc.add_text('Hello, World!')
doc.add_image('path/to/image.png')

# Save the document
doc.save('output.<EXT>')
```

## Usage

### Loading Configurations

Pyffice relies on YAML files to define how to handle each document type. A sample YAML for a word document might look like:

```yaml
document_type: word
engine: <LIB_WORD>
styles:
  default_font: Arial
  default_size: 12
operations:
  add_text: method_name_in_engine
  add_table: another_method
```

Use `pyffice.load_config(yaml_path)` to parse and validate the config.

### Creating and Editing Documents

```python
# Initialize with config
config = pyffice.load_config('spreadsheet.yaml')
sheet = pyffice.Spreadsheet(config)

# Perform operations
sheet.set_cell(1, 1, 'Value')
sheet.add_formula(1, 2, '=A1*2')

# Export
sheet.export('output.<EXT>')
```

### Supported Document Types

- Word Processing: .docx, .odt
- Spreadsheets: .xlsx, .ods
- Presentations: .pptx, .odp
- Others: <ADDITIONAL_TYPES> (configurable via YAML)

## Examples

### Example 1: Generating a Report

```python
import pyffice

config = pyffice.load_config('report.yaml')
report = pyffice.Document(config)
report.add_heading('Monthly Report', level=1)
report.add_paragraph('Summary: All systems operational.')
report.add_table(data=[['Item', 'Status'], ['System A', 'OK'], ['System B', 'OK']])
report.save('report.<EXT>')
```

### Example 2: Batch Processing

```python
import pyffice

configs = ['doc1.yaml', 'doc2.yaml']
for cfg_path in configs:
    config = pyffice.load_config(cfg_path)
    doc = pyffice.Document(config)
    # Process and save
    doc.save(f'processed_{cfg_path.split(".")[0]}.<EXT>')
```

## Configuration Guide

Each YAML config must include:

- `document_type`: String identifier (e.g., 'word', 'spreadsheet')
- `engine`: The underlying library or tool to use (e.g., '<LIB_NAME>')
- `styles`: Dictionary of default styles
- `operations`: Mapping of Pyffice methods to engine-specific calls

For advanced customization, refer to the [docs/config-reference.md](docs/config-reference.md).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/<FEATURE_NAME>`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/<FEATURE_NAME>`).
5. Open a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the <LICENSE_TYPE> License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with inspiration from open-source communities.
- Thanks to contributors of underlying libraries like <LIB1>, <LIB2>.