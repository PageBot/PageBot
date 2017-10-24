Within this directory, the manually edited markdown files are under version control (index, howto, license).
Every markdown file inside the `Docs/pagebot` directory is generated, and thus the `.gitignore` file here excludes them.

They are copied to the Docs folder by the `builddoc` script, and you can regenerate them by running, in the root of the repository:

    python builddoc.py -w
