#!/bin/bash
# extract.sh - Wrapper script for MarkItDown extraction using Pixi

if [ -z "$1" ]; then
  echo "Usage: $0 <input_file> [output_file]"
  exit 1
fi

INPUT_FILE="$(readlink -f "$1")"
if [ -n "$2" ]; then
  OUTPUT_FILE="$(readlink -f "$2")"
else
  OUTPUT_FILE=""
fi

# Change to the scripts directory to use the pixi environment
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

if [ -z "$OUTPUT_FILE" ]; then
  pixi run extract "$INPUT_FILE"
else
  pixi run extract "$INPUT_FILE" > "$OUTPUT_FILE"
fi
