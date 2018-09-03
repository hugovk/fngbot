fngbot
======

[![Build Status](https://travis-ci.org/hugovk/fngbot.svg?branch=master)](https://travis-ci.org/hugovk/fngbot)
[![Coverage Status](https://coveralls.io/repos/github/hugovk/fngbot/badge.svg?branch=master)](https://coveralls.io/github/hugovk/fngbot?branch=master)

I am a bot that tweets an object from the collection of the Finnish National Gallery: Ateneum, Kiasma and Sinebrychoff art museums.

Thanks to the Finnish National Gallery for releasing data on their 36 000+ artworks.

Follow along:

 * https://twitter.com/AteneumBot
 * https://twitter.com/KiasmaBot
 * https://twitter.com/SinebrychoffBot


To use, create an app on Twitter with write permissions and put the Twitter key and secret in a YAML file. Specify the art museum with the --unit argument, otherwise it'll pick a random artwork from the whole collection.

```python
usage: fngbot.py [-h] [-y YAML] [-x] [-nw] [-u {ateneum,kiasma,sinebrychoff}]

optional arguments:
  -h, --help            show this help message and exit
  -y YAML, --yaml YAML  YAML file location containing Twitter key and secret
                        (default: M:/bin/data/fngbot.yaml)
  -x, --test            Test mode: don't tweet (default: False)
  -nw, --no-web         Don't open a web browser to show the tweeted tweet
                        (default: False)
  -u {ateneum,kiasma,sinebrychoff}, --unit {ateneum,kiasma,sinebrychoff}
                        Unit of Finnish National Gallery that houses the
                        artwork. Either Ateneum, Kiasma or Sinebrychoff Art
                        Museum (SF). Sinebrychoff Art Museum houses old
                        international art from the 14th century to the early
                        19th century. The Ateneum Art Museum houses pre-1960
                        Finnish art and international art from the 19th and
                        20th centuries. The Museum of Contemporary Art Kiasma
                        houses post-1960 Finnish and international art.
                        (default: None)
```

See also:

 * http://kokoelmat.fng.fi/api/v2support/docs/
 * https://github.com/hugovk/finnishnationalgallery
 * https://github.com/hugovk/fng-tools

