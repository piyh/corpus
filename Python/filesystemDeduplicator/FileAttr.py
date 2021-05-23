#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileAttr():
    name: str
    path: Path
    size: int
    mtime: int
    #fileParts: set
