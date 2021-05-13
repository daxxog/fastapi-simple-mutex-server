#!/bin/bash
lambda() {
    python3 -c "import sys; sys.stdout.write(''.join(map(lambda line: ${1}, sys.stdin)))"
}
