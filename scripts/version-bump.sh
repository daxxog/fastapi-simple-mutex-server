#!/bin/bash
source scripts/lambda.sh

APP_VERSION=$(cat VERSION)
# bump the minor version
APP_VERSION_NEXT=$(echo ${APP_VERSION} | lambda "'.'.join([line.split('.')[0], line.split('.')[1], str(int(line.split('.')[2]) + 1)])")

echo ""
echo Current version: ${APP_VERSION}
echo New version: ${APP_VERSION_NEXT}

echo ""
echo bumping version in 10 seconds . . .
echo press CTRL+C to cancel
sleep 10

echo ${APP_VERSION_NEXT} > VERSION
git diff VERSION
