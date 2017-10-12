# What's `mort`?

Mort is a Mobile Responsibility Regression Test tool for web developers and designers. 

There are only two commands to it.

`mort capture`: Mort generates full-page screen shots of any web pages specified, from **real devices and in parallel. **. Instead of manually clicking through each pages and fiddle with different device resolutions, the capture utility makes it trivial for one to see all variations by flipping through the images.

`mort compare 7102ce ed92de`: Mort will compare all the screen shots in two directories and surface the ones that have changed between these two versions. This feature makes it possible to establish a baseline and make sure that no unexpected changes have been introduced into the system. One can even use the `git bisect` approach to pinpoint the particular version where an issue first appears.

# How's it different from Gemini? Or Needle?

Think gemini or Needle as a unit test tool and mort as an integration suite. You should have both.

[gemini-testing](https://github.com/gemini-testing/gemini) allows you to zoom in to a DOM element and run visual regression tests on this one node only. It aims to provide a harness for testing css and it even provides a nice feature to extract css converage data. 

# Concepts & Terminology

* `target`: a descriptor for a combination of a specific version of os and browser. A target is the basic unit for scheduling and comparison. The full list can be found on [BrowserStack's Browsers & Mobile Devices for Screenshot Testing page](https://www.browserstack.com/list-of-browsers-and-platforms?product=screenshots). Here is a couple of examples:

        {
            "os": "ios",
            "os_version": "6.0",
            "browser": "Mobile Safari"
            "browser_version": null
            "device": "iPhone 4S (6.0)"
        }

        {
            "os": "OS X",
            "os_version": "El Capitan",
            "browser": "firefox",
            "device": "",
            "browser_version": "45.0",
            "real_mobile": ""
        }

* `pattern`: a json structure that limits the scope of the targets. The keys are the same used in the `target` list and the substrings we're looking for in the values. Let's look at a few examples:

        # Matches all iPhone 4S devices
        { "device": "4s" }

        # Matches only Mobile Safari 6.0 running on iPhone 4S
        { "device": "4s", "os_version": "6" }

        # Matches Chrome 50.0 on El Captan
        { "os_version": "El Capitan", "browser_version": "50" }


# Commands & Options

`mort update`: Download the latest target list from BrowserStack.
`mort capture`: Generate all screen shots. It's recommended that this becomes part of your CI configuration with the thumbnails saved into a drive synched via Dropbox. 
`mort compare`: Compare all screen shots between two versions.

There are a few options that give fine control over the scope for `capture` and `compare`. 

By default, mort runs on all devices for all targeted urls, which can take quite some time.
    `mort capture`: default

The `--target` allows us to focus on one or a few specific sets of browser and operation systems. It takes a comma-separated regular expression or a json dump of targets to match. 

    # Only run for all iPhone devices
    mort capture --target iPhone 

    # Only run chrome on all devices starts with `iP`, like "iPhone 6s" or "iPad 4th".
    mort capture --target iP.*,chrome 

    # Only run IE 11 on Windows 7
    mort capture --target '{os: "windows", browser:"ie", os_version: 7, browser_version: 11.0}'

The `--urls` allows us to zoom in onto a set of urls that we are working on:

    # Only run for one specified url `/products/wall-dots`
    mort capture --urls /products/wall-dots

    # Only run against all urls under `/products/`, equivalent to `/products/.*`
    mort capture --urls /products/.*

    # Only run for any urls that ends with `html`
    mort capture --urls html$

# Installation

Configure it with your own settings with `cp local_conf.py.sample mort/local_conf.py`, then go to BrowserStack
and paste in the access key.

Additionally, you can fetch the latest os-device-list by running `mort update`.

# Develop

    git clone git@github.com:alexdong/mort.git
    cd mort
    python -m venv . ; . bin/activate
    pip install -r requirements.txt

    brew install modd
    modd
    pytest


# Giant shoulders

Mort is a simple, albeit a tasteful, wrapper over three important services that do the heavylifting.

<div align="center">
  <a href="https://www.browserstack.com/screenshots/api">
    <img width="200" src="https://raw.githubusercontent.com/alexdong/mort/master/assets/browserstack.svg">
  </a>
  <a href="http://scikit-image.org/">
    <img width="200" heigth="200" src="https://raw.githubusercontent.com/alexdong/mort/master/assets/scikit-image.png">
  </a>
  <a href="https://opencv.org/">
    <img width="100" src="https://raw.githubusercontent.com/alexdong/mort/master/assets/opencv.svg">
  </a>
</div>

* It uses [BrowserStack](https://www.browserstack.com/screenshots/api) for real device, parallel screenshots capturing.
    BrowserStack is not free.  Nor is your time.

* It relies on [scikit-image](https://github.com/scikit-image/scikit-image)'s `skimage.measure.compare_ssim` algorithm to compute the mean Structural Similarity Index between two images.

* Mort relies on **git**'s hash value for different versions. Different from the `gemini` approach, instead of maintaining a golden standard of a set of screen shots, which inevitably brings the burden of maintaining it, mort takes a lightweight approach: it generates the screen shots with the current git hash, retrieved by running `git rev-parse HEAD`.


# Tech notes and limitations

The main limitation of `mort` is that it's colour blind. It can only tell the differences between two greyscale images.
This is not a limitation of the [SSIM algorithm(PDF)](http://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf) but rather
a deliberate trade off that's made by `scikit-image`.

If you treat `mort` as an integration tool and use it alongside unit test tools like `gemini` or `needle`, then you
should be well covered. There is also the potential for us to implement a simpler pixel-by-pixel comparison algorithm
that's used Yandex's [looks-same](https://github.com/gemini-testing/looks-same) or Yahoo's [blink-diff](https://github.com/yahoo/blink-diff).
