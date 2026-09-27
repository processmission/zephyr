"""
External content
################

Copyright (c) 2021 Nordic Semiconductor ASA
SPDX-License-Identifier: Apache-2.0

Introduction
============

This extension allows to import sources from directories out of the Sphinx
source directory. They are copied to the source directory before starting the
build. Note that the copy is *smart*, that is, only updated files are actually
copied. Therefore, incremental builds detect changes correctly and behave as
expected.

Paths for external content included via e.g. figure, literalinclude, etc.
are adjusted as needed.

Configuration options
=====================

- ``external_content_contents``: A list of external contents. Each entry is
  a tuple with two fields: the external base directory and a file glob pattern.
- ``external_content_directives``: A list of directives that should be analyzed
  and their paths adjusted if necessary. Defaults to ``DEFAULT_DIRECTIVES``.
- ``external_content_keep``: A list of file globs (relative to the destination
  directory) that should be kept even if they do not exist in the source
  directory. This option can be useful for auto-generated files in the
  destination directory.
- ``external_content_exclude``: Absolute directories omitted from source collection.
- ``external_content_overlay``: Optional source directory whose relative paths replace matching
  narrative files in the assembled tree. Generated files are not selected from this directory.
"""

import filecmp
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from sphinx.application import Sphinx

__version__ = "0.1.0"


DEFAULT_DIRECTIVES = ("figure", "image", "include", "literalinclude")
"""Default directives for included content."""


def adjust_includes(
    fname: Path,
    basepath: Path,
    directives: list[str],
    encoding: str,
    dstpath: Path | None = None,
    source_map: dict[Path, Path] | None = None,
) -> None:
    """Adjust included content paths.

    Args:
        fname: File to be processed.
        basepath: Base path to be used to resolve content location.
        directives: Directives to be parsed and adjusted.
        encoding: Sources encoding.
        dstpath: Destination path for fname if its path is not the actual destination.
        source_map: Original source paths mapped to their assembled destinations.
    """

    if fname.suffix != ".rst":
        return

    dstpath = dstpath or fname.parent

    def _adjust(m):
        directive, fpath = m.groups()

        # ignore absolute paths
        if fpath.startswith("/"):
            fpath_adj = fpath
        else:
            target = (basepath / fpath).resolve()
            if directive == "include" and source_map is not None:
                target = source_map.get(target, target)
            fpath_adj = Path(os.path.relpath(target, dstpath)).as_posix()

        return f".. {directive}:: {fpath_adj}"

    with open(fname, "r+", encoding=encoding) as f:
        content = f.read()
        content_adj, modified = re.subn(
            r"\.\. (" + "|".join(directives) + r")::\s*([^`\n]+)", _adjust, content
        )
        if modified:
            f.seek(0)
            f.write(content_adj)
            f.truncate()


def sync_contents(app: Sphinx) -> None:
    """Synchronize external contents.

    Args:
        app: Sphinx application instance.
    """

    srcdir = Path(app.srcdir).resolve()
    to_copy = []
    to_delete = set(f for f in srcdir.glob("**/*") if not f.is_dir())
    to_keep = set(
        f for k in app.config.external_content_keep for f in srcdir.glob(k) if not f.is_dir()
    )

    def _pattern_excludes(f):
        # backup files
        return (
            f.match('.#*')
            or f.match('*~')
            or any(f.is_relative_to(Path(path)) for path in app.config.external_content_exclude)
        )

    for content in app.config.external_content_contents:
        prefix_src, glob = content
        for src in prefix_src.glob(glob):
            if src.is_dir():
                to_copy.extend(
                    [
                        (f, prefix_src)
                        for f in src.glob("**/*")
                        if (not f.is_dir() and not _pattern_excludes(f))
                    ]
                )
            elif not _pattern_excludes(src):
                to_copy.append((src, prefix_src))

    source_map = {src.resolve(): srcdir / src.relative_to(prefix) for src, prefix in to_copy}
    overlay = app.config.external_content_overlay
    for entry in to_copy:
        src, prefix_src = entry
        dst = (srcdir / src.relative_to(prefix_src)).resolve()
        original = src
        if overlay and src.suffix in (".rst", ".html", ".txt"):
            translation = Path(overlay) / src.relative_to(prefix_src)
            if translation.is_file():
                src = translation

        if dst in to_delete:
            to_delete.remove(dst)

        if not dst.parent.exists():
            dst.parent.mkdir(parents=True)

        # Compare assembled RST, including after a translation is removed or replaced by
        # an older file. Source mtimes alone cannot detect a change of language source.
        if src.suffix == ".rst":
            with tempfile.TemporaryDirectory() as td:
                adjusted = Path(td) / src.name
                shutil.copy(src, adjusted)
                adjust_includes(
                    adjusted,
                    original.parent,
                    app.config.external_content_directives,
                    app.config.source_encoding,
                    dstpath=dst.parent,
                    source_map=source_map,
                )
                if not dst.exists() or not filecmp.cmp(adjusted, dst, shallow=False):
                    shutil.copyfile(adjusted, dst)
            continue

        if overlay and src.suffix in (".html", ".txt"):
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                shutil.copyfile(src, dst)
            continue

        # just copy if it does not exist
        if not dst.exists():
            shutil.copy(src, dst)
            adjust_includes(
                dst,
                src.parent,
                app.config.external_content_directives,
                app.config.source_encoding,
            )
        # if origin file is modified only copy if different
        elif src.stat().st_mtime > dst.stat().st_mtime:
            with tempfile.TemporaryDirectory() as td:
                # adjust origin includes before comparing
                src_adjusted = Path(td) / src.name
                shutil.copy(src, src_adjusted)
                adjust_includes(
                    src_adjusted,
                    src.parent,
                    app.config.external_content_directives,
                    app.config.source_encoding,
                    dstpath=dst.parent,
                )

                if not filecmp.cmp(src_adjusted, dst):
                    dst.unlink()
                    shutil.move(os.fspath(src_adjusted), os.fspath(dst))

    # remove any previously copied file not present in the origin folder,
    # excepting those marked to be kept.
    for file in to_delete - to_keep:
        file.unlink()


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("external_content_contents", [], "env")
    app.add_config_value("external_content_directives", DEFAULT_DIRECTIVES, "env")
    app.add_config_value("external_content_keep", [], "")
    app.add_config_value("external_content_exclude", [], "env")
    app.add_config_value("external_content_overlay", "", "env")

    app.connect("builder-inited", sync_contents)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
