# Stock Images Pipeline

This tool is inteneded to speed up the process of sending images created with generative AI to image banks like Adobe Stock, Dreamstime and others.

It works through jobs which could be invoked in a batch or separately.

## Available Jobs

- Slice
- Upscale
- Embed metadata
- Upload

### Slicing
The slice feature is intended for processing Midjourney preview images, extracting each quadrant in a separate image.

### Upscaling

Upscale uses OpenVino Super Resolution model which is limited to 16:9 images. Hopefully we have a workaround for it.

## Tests
With **activated venv** run: 

```sh tests/run-tests.sh```

It's a convenient script to run all available tests and show coverage.
### Coverage
```
coverage run -m unittest tests.test_image_slicer tests.test_image_helper
```
```
coverage report -m -i
```
It's worth to mention the -i parameter. It's workaround for a unittest lib bug.

## Usage

### Setting up env
- Create a venv and activate it
- From the venv run 
```
pip install -r requirements.txt
```

### Running

```
python3 main.py <command>
```
Available commands are:
- slice
- upscale
- tag
- upload
- read_tags
- process
- alljobs