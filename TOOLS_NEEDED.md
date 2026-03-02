# External Tools Required

Some Pyffice document formats require external tools or libraries that are not bundled.

## Container Formats

| Format | Tool | Install |
|--------|------|---------|
| rar | unrar | `apt install unrar` |
| sevenzip | 7z | `apt install p7zip-full` |

## Ebook Formats

| Format | Library | Install |
|--------|---------|---------|
| epub | ebooklib | `pip install ebooklib` |
| mobi | calibre | `pip install calibre` |
| azw | calibre | `pip install calibre` |

## CAD Formats

| Format | Library | Install |
|--------|---------|---------|
| obj | trimesh | `pip install trimesh` |
| stl | trimesh | `pip install trimesh` |
| dxf | ezdxf | `pip install ezdxf` |
| dwg | ODA File Converter | External tool |
| step | pythonocc | `pip install pythonocc-core` |
| iges | pythonocc | `pip install pythonocc-core` |
| blend | urllib (read mesh) | Built-in |
| fbx | fbx-sdk | External |
| gltf | trimesh | `pip install trimesh` |

## Presentation

| Format | Library | Install |
|--------|---------|---------|
| pptx | python-pptx | `pip install python-pptx` |

## Media

| Format | Tool | Install |
|--------|------|---------|
| video | ffmpeg | `apt install ffmpeg` |
| audio | ffmpeg | `apt install ffmpeg` |

## Document Formats

| Format | Library | Install |
|--------|---------|---------|
| rtf | python-docx | `pip install python-docx` |
| odt | odfpy | `pip install odfpy` |
| latex | subprocess | Requires LaTeX |
| rst | docutils | `pip install docutils` |
| asciidoc | asciidoc | `apt install asciidoc` |

## Installation Script

```bash
# Core dependencies
pip install ebooklib trimesh ezdxf python-pptx python-docx odfpy docutils

# System tools
apt install unrar p7zip-full ffmpeg asciidoc
```
