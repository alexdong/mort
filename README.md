# What's `mrt`?

Mrt is a Mobile Responsibility Regression Test tool for web developers and designers. 

There are only two commands to it.

`mrt capture`: Mrt generates full-page screen shots of any web pages specified, from **real devices and in parallel. **. Instead of manually clicking through each pages and fiddle with different device resolutions, the capture utility makes it trivial for one to see all variations by flipping through the images.

`mrt compare 7102ce ed92de`: Mrt will compare all the screen shots in two directories and surface the ones that have changed between these two versions. This feature makes it possible to establish a baseline and make sure that no unexpected changes have been introduced into the system. One can even use the `git bisect` approach to pinpoint the particular version where an issue first appears.

# How's it different from Gemini? Or Needle?

Think gemini or Needle as a unit test tool and mrt as an integration suite. You should have both.

[gemini-testing](https://github.com/gemini-testing/gemini) allows you to zoom in to a DOM element and run visual regression tests on this one node only. It aims to provide a harness for testing css and it even provides a nice feature to extract css converage data. 

# Dependencies & Assumptions

Mrt is a simple, albeit a tasteful, wrapper over three important services that do the heavylifting. 

* It uses [BrowserStack](https://www.browserstack.com/screenshots/api) for real device, parralel screenshoting. BrowserStack is not free.  Nor is your time. 

* It relies on [scikit-image](https://github.com/scikit-image/scikit-image)'s `skimage.measure.compare_ssim` algorithm to compute the mean Structural Similarity Index between two images. 

The [SSIM (PDF)](http://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf) approach gives more control over both the comparison process, eg multichannel, dynamic range or gaussian weights, and more output details regards the similarities, making it superior to the hard coded approach used in Yandex's [looks-same](https://github.com/gemini-testing/looks-same) or Yahoo's [blink-diff](https://github.com/yahoo/blink-diff). (Recommended [default parameters](https://github.com/scikit-image/scikit-image/blob/adc1a19dd5083f89cf04caf8cd9ff19916a4a293/skimage/measure/_structural_similarity.py#L67) have been set to match the implementation of Wang et. al)

* Mrt relies on **git**'s hash value for different versions. Different from the `gemini` approach, instead of maintaining a golden standard of a set of screen shots, which inevitably brings the burden of maintaining it, mrt takes a lightweight approach: it generates the screen shots with the current git hash, retrieved by running `git rev-parse HEAD`. 

# Commands & Options

`mrt capture`: Generate all screen shots. It's recommended that this becomes part of your CI configuration with the thumbnails saved into a drive synched via Dropbox. 
`mrt compare`: Compare all screen shots between two versions.

There are a few options that give fine control over the scope for `capture` and `compare`. 

By default, mrt runs on all devices for all targeted urls, which can take quite some time.
    `mrt capture`: default

The `--target` allows us to focus on one or a few specific sets of browser and operation systems. It takes a comma-separated regular expression or a json dump of targets to match. 

    # Only run for all iPhone devices
    mrt capture --target iPhone 

    # Only run chrome on all devices starts with `iP`, like "iPhone 6s" or "iPad 4th".
    mrt capture --target iP.*,chrome 

    # Only run IE 11 on Windows 7
    mrt capture --target '{os: "windows", browser:"ie", os_version: 7, browser_version: 11.0}'

The `--urls` allows us to zoom in onto a set of urls that we are working on:

    # Only run for one specified url `/products/wall-dots`
    mrt capture --urls /products/wall-dots

    # Only run against all urls under `/products/`, equivalent to `/products/.*`
    mrt capture --urls /products/.*

    # Only run for any urls that ends with `html`
    mrt capture --urls html$

# Installation

- `pip install -r requirements.txt`
- Modify the `local_conf.py.sample` to your needs and save it as `mtr/local_conf.py`

# Develop

- `brew install modd`
- `modd`

# TODO

Mrt scratches my own itch and I don't have any near term plan to extend it. But it's far from finished by any stretch of imagination. Following is a list of some areas PR will be greatly appreciated. 

- `mrt init`: Generate the default `mrt.config.js` file if one doesn't exist in the current folder by taking the user through a list of questions. 
- Support login and authentication