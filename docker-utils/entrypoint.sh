#!/bin/bash
set -e

echo "Starting in production mode with Lambda runtime"
exec ["main.handler"]
