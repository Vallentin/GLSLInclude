
# GLSL Include

GLSL Include is a simple GLSL tool for preprocessing `#include` directives.


## Install

```bash
pip install git+https://github.com/Vallentin/GLSLInclude
```


## Example

The default search path is the current working directory.
The input is read from `input.glsl` and the written to `output.glsl`.
If an output filename is omitted then the output is written stdout.

```bash
python -m glslinclude --output "output.glsl" "input.glsl"
```

*Any missing directories in the output filename are automatically created.*


## Search Path

If the current working directory shouldn't be the default search path, then a custom search path can be specified using `--search-path`.

```bash
python -m glslinclude --search-path "shaders" --output "output.glsl" "input.glsl"
```


### Multiple Paths

The search path can include multiple semicolon separated paths.

```bash
python -m glslinclude --search-path "shaders;shaders/utilities" --output "output.glsl" "input.glsl"
```


### Search Order & Extensions

Searching the paths are done in the order they're given. Either until a file is found, if not an error is raised.


### Extensions

Both `#include "common"` and  `#include "common.glsl"` is allowed.

```python
"", ".glsl", ".vert", ".tesc", ".tese", ".geom", ".frag", ".comp"
```

Searching is done for each extension and then for each path in the search path.

```python
for ext in extensions:
    for path in search_path:
        ...
```
