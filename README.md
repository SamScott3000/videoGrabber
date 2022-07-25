# Video Grabber

Video Grabber is a project to download and display videos uploaded at the coordinates of various global airports.

## Prerequisites

**Warning - This project was intended for personal use and as a result will likely not work in many development environments. Use at own risk.**

You must have access to the [YouTube API](https://developers.google.com/youtube/v3), a developer key and a Google API plan.

## Getting it working

Once your personal developer key has been added, simply clone the Repo and add your developer key to the below.

```python
youtube = googleapiclient.discovery.build(
api_service_name, api_version, developerKey="insert-developer-key-here")
return youtube
```

## Misc.

You can read more about this project on my [Website.](https://www.samscott.dev/projects/generic)