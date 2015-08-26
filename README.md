# Pyvec

[![Join the chat at https://gitter.im/KeironO/Pyvec](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/KeironO/Pyvec?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Pyvec attempts to solve a paramount issue in deep learning, the vectorisation of raw data. The idea of the project is to make vectorisation as easy as humanly possible, and to enable data scientists to focus on more important issues.

## Quick start

There are a number of ways to get started with Pyvec.

- [Download the latest release](https://github.com/KeironO/Pyvec/archive/master.zip).
- Clone the repo ```git clone https://www.github.com/KeironO/Pyvec```.

## What can it do now?

* Convert images into vectors
* Serialise data to pickle files.
* Import serialised pickled data.
* That's about it... for now!

## Usage

### Loading images

Firstly, you will be required to load the module in. This is a simple process.

```
import imp
pyvec_api = imp.load_source('api', '../../pyvec/core/api.py')
```

Set the width, height and percentage split.

```
height = 1337
width = 1337
split = 0.5
withTest = False
```

To then load the data...

```
train_data, train_label, val_data, val_label = pyvec_api.load_images(save_path, custom_height,                      custom_width, split, withTest)
```

## Bugs and feature requests

We are actively looking for contributions from the free software community. But please, [before opening a new issue](https://github.com/KeironO/Pyvec/issues/new) - search for [closed or existing issues](https://github.com/KeironO/Pyvec/issues) beforehand.

## Creators

**Keiron O'Shea**

* http://www.github.com/KeironO/
* http://users.aber.ac.uk/keo7

## License

All code is released under the [MIT License](https://github.com/KeironO/Pyvec/blob/master/LICENSE).
