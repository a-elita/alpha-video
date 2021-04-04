# Alpha-Video

[![docker](https://github.com/unofficial-skills/youtube-alexa-python/actions/workflows/docker-package.yml/badge.svg)](https://github.com/unofficial-skills/youtube-alexa-python/actions/workflows/docker-package.yml)


[![Python](https://github.com/unofficial-skills/youtube-alexa-python/actions/workflows/python.yml/badge.svg)](https://github.com/unofficial-skills/youtube-alexa-python/actions/workflows/python.yml)

[![Build Status](https://dev.azure.com/andrewstech-youtube/alpha-video-python/_apis/build/status/unofficial-skills.alpha-video?branchName=setup)](https://dev.azure.com/andrewstech-youtube/alpha-video-python/_build/latest?definitionId=4&branchName=setup)

## DOCS

Please visit the docs by clicking [here](https://alpha-video.andrewstech.me/)

## Run in docker


docker run -d --restart unless-stopped --name alpha-video -p 5000:5000 -e token=12345 andrewstech/alpha-video:latest
