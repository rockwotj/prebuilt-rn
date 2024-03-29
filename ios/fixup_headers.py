#!/usr/bin/env python3
import codemod

def import_line_matcher(line):
    if not line.endswith(".h>\n"):
        return False
    return line.startswith("#import <React/") or line.startswith("#import <yoga/")


def header_transform(line):
    stripped = (
        line.removeprefix("#import <React/")
        .removeprefix("#import <yoga/")
        .removesuffix(">\n")
    )
    return f'#import "{stripped}"\n'


q = codemod.Query(
    codemod.line_transformation_suggestor(
        header_transform, line_filter=import_line_matcher
    ),
    root_directory="./build/",
    path_filter=codemod.path_filter(["h"]),
)

print("Fixing up system imports")
codemod.run_interactive(q)


def module_line_matcher(line):
    return line == "module React {\n"


def modulemap_transform(line):
    return f"framework {line}"


q = codemod.Query(
    codemod.line_transformation_suggestor(
        modulemap_transform, line_filter=module_line_matcher
    ),
    root_directory="./build/",
    path_filter=codemod.path_filter(["modulemap"]),
)

print("Fixing up modulemaps")
codemod.run_interactive(q)
