#!/bin/bash

coverage run -m unittest tests.test_image_slicer tests.test_image_helper tests.test_image_tagger tests.test_upscaler
coverage report -m -i