#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for fngbot.py
"""
from __future__ import print_function, unicode_literals

import fngbot

try:
    import unittest
except ImportError:
    import unittest2 as unittest


class TestIt(unittest.TestCase):

    def test_1(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  "Creator",
                  "2014",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title by Creator (2014) http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_2(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  "Creator",
                  "ajoittamaton",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title by Creator http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_3(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  "Creator",
                  None,
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title by Creator http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_1_creator_is_none(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  None,
                  "2014",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title (2014) http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_2_creator_is_none(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  None,
                  "ajoittamaton",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_3_creator_is_none(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  None,
                  None,
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_1_creator_is_empty(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  "",
                  "2014",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title (2014) http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_2_creator_is_empty(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  "",
                  "ajoittamaton",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_3_creator_is_empty(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "English title", "Swedish title",
                  "",
                  None,
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "English title http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_1_long_title(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "Finnish title", "A long English title which would mean the length of the tweet, with added creator, creation date and both links, would exceed the maximum permitted 140 characters.", "Swedish title",
                  "Creator",
                  "2014",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "A long English title which would mean the length of the tweet, with added c… by Creator (2014) http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")

    def test_unnamed(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  "nimetön", "", "",
                  "Creator",
                  "2014",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "unnamed by Creator (2014) http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")


    def test_unicode_unnamed(self):
        # Arrange
        artwork = [["ID001", "ID002"],
                  u"nimetön", "", "",
                  "Creator",
                  "2014",
                  "http://example.com/thing/ABC123"]

        # Act
        tweet = fngbot.build_tweet(artwork)

        # Assert
        self.assertEqual(tweet, "unnamed by Creator (2014) http://example.com/thing/ABC123&lang=en http://kokoelmat.fng.fi/app?action=image&iid=ID001&profile=topicartworkbignew#.jpg")


if __name__ == '__main__':
    unittest.main()

# End of file
