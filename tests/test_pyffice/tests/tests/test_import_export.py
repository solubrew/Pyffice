"""Import/Export Test Runner for Pyffice."""
import logging
import os
import sys
import tempfile
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

DOCUMENT_TYPES = {
    "data": ["csv", "json", "xml", "yaml"],
    "config": ["ini", "toml", "env"],
    "presentation": ["pptx"],
    "media": ["video", "audio"],
    "container": ["zip", "tar", "rar", "sevenzip"],
    "ebook": ["epub", "mobi", "azw"],
    "cad": ["obj", "stl", "scad", "dxf", "dwg", "step", "iges", "blend", "fbx", "gltf"],
    "script": ["rtf", "odt", "latex", "rst", "asciidoc"],
}


def create_sample_file(doc_type, filepath):
    ext = os.path.splitext(filepath)[1]
    
    if doc_type == "csv":
        with open(filepath, "w") as f:
            f.write("name,value\ntest,123\n")
    elif doc_type == "json":
        with open(filepath, "w") as f:
            f.write('{"name": "test", "value": 123}')
    elif doc_type == "yaml":
        with open(filepath, "w") as f:
            f.write("name: test\nvalue: 123\n")
    elif doc_type == "xml":
        with open(filepath, "w") as f:
            f.write('<?xml version="1.0"?><root><item name="test" value="123"/></root>')
    elif doc_type == "ini":
        with open(filepath, "w") as f:
            f.write("[section]\nkey = value\n")
    elif doc_type == "toml":
        with open(filepath, "w") as f:
            f.write('[section]\nkey = "value"\n')
    elif doc_type == "env":
        with open(filepath, "w") as f:
            f.write("KEY=value\n")
    elif doc_type == "zip":
        import zipfile
        with zipfile.ZipFile(filepath, "w") as zf:
            zf.writestr("test.txt", "content")
    elif doc_type == "tar":
        import tarfile
        with tarfile.open(filepath, "w") as tf:
            import io
            data = b"content"
            tf.addfile(tarfile.TarInfo("test.txt"), io.BytesIO(data))
    elif doc_type == "epub":
        from pyffice.ebook import epub
        epub.create("Test", "Author", "<p>Chapter 1 content</p>", filepath)
    elif doc_type == "obj":
        with open(filepath, "w") as f:
            f.write("v 1.0 2.0 3.0\nf 1 2 3\n")
    elif doc_type == "stl":
        with open(filepath, "w") as f:
            f.write("solid test\nendsolid test\n")
    elif doc_type == "gltf":
        with open(filepath, "w") as f:
            f.write('{"asset": {"version": "2.0"}, "scene": 0}')
    else:
        with open(filepath, "w") as f:
            f.write(f"Sample {doc_type} content")


def test_import_export(doc_type, category):
    logger.info(f"\n=== Testing {category}/{doc_type} ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, f"test.{doc_type}")
        create_sample_file(doc_type, src_file)
        
        dst_file = os.path.join(tmpdir, f"test_{doc_type}_exported.{doc_type}")
        
        try:
            if category == "data":
                if doc_type == "csv":
                    from pyffice.data import csv
                    data = csv.read(src_file)
                    csv.write(dst_file, data)
                elif doc_type == "json":
                    from pyffice.data import json
                    data = json.read(src_file)
                    json.write(dst_file, data)
                elif doc_type == "yaml":
                    from pyffice.data import yaml
                    data = yaml.load(src_file)
                    yaml.dump(dst_file, data)
                elif doc_type == "xml":
                    from pyffice.data import xml
                    data = xml.parse(src_file)
                    xml.write(dst_file, data)
            
            elif category == "config":
                if doc_type == "ini":
                    from pyffice.config import ini
                    data = ini.load(src_file)
                    ini.write(dst_file, data)
                elif doc_type == "toml":
                    from pyffice.config import toml
                    data = toml.load(src_file)
                    toml.write(dst_file, data)
                elif doc_type == "env":
                    from pyffice.config import env
                    data = env.load(src_file)
                    env.write(dst_file, data)
            
            elif category == "container":
                if doc_type == "zip":
                    from pyffice.container import zip
                    zip.extract(src_file, tmpdir + "/extract")
                    zip.compress(tmpdir + "/extract", dst_file)
                elif doc_type == "tar":
                    from pyffice.container import tar
                    tar.extract(src_file, tmpdir + "/extract")
                    tar.compress(tmpdir + "/extract", dst_file)
            
            elif category == "ebook":
                if doc_type == "epub":
                    from pyffice.ebook import epub
                    book = epub.read(src_file)
                    epub.write(dst_file, book)
            
            elif category == "cad":
                if doc_type == "obj":
                    from pyffice.cad import obj
                    data = obj.read(src_file)
                    obj.write(dst_file, data)
                elif doc_type == "stl":
                    from pyffice.cad import stl
                    data = stl.read(src_file)
                    stl.write(dst_file, data)
                elif doc_type == "gltf":
                    from pyffice.cad import gltf
                    data = gltf.read(src_file)
                    gltf.write(dst_file, data)
            
            if os.path.exists(dst_file):
                size = os.path.getsize(dst_file)
                logger.info(f"  ✅ {doc_type}: Exported ({size} bytes)")
                return True
            else:
                logger.info(f"  ❌ {doc_type}: Export failed")
                return False
                
        except Exception as e:
            logger.info(f"  ❌ {doc_type}: Error - {str(e)}")
            return False


def run_all_tests():
    logger.info("=" * 60)
    logger.info("Pyffice Import/Export Test Runner")
    logger.info("=" * 60)
    
    results = {"passed": 0, "failed": 0}
    
    for category, types in DOCUMENT_TYPES.items():
        for doc_type in types:
            success = test_import_export(doc_type, category)
            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1
    
    logger.info("\n" + "=" * 60)
    logger.info(f"Results: {results['passed']} passed, {results['failed']} failed")
    logger.info("=" * 60)
    
    return results


if __name__ == "__main__":
    run_all_tests()
