# -*- coding: utf-8 -*-

__title__ = 'transliterate.tests'
__version__ = '0.7'
__build__ = 0x000007
__author__ = 'Artur Barseghyan'
__all__ = ('TransliterateTest',)

import unittest

#import simple_timer

from transliterate import autodiscover
from transliterate.conf import set_setting, get_setting
from transliterate import defaults
from transliterate.utils import get_available_language_codes, translit, detect_language, slugify
from transliterate.utils import get_available_language_packs
from transliterate.decorators import transliterate_function, transliterate_method
from transliterate.base import TranslitLanguagePack, registry
from transliterate.contrib.apps.translipsum import TranslipsumGenerator

TRACK_TIME = True

def track_time(func):
    """
    Prints some useful info.
    """
    if not TRACK_TIME:
        return func

    def inner(self, *args, **kwargs):
        #timer = simple_timer.Timer() # Start timer

        result = func(self, *args, **kwargs)

        #timer.stop() # Stop timer

        print '\n%s' % func.__name__
        print '============================'
        print '""" %s """' % func.__doc__.strip()
        print '----------------------------'
        if result is not None: print result
        #print 'done in %s seconds' % timer.duration

        return result
    return inner


class TransliterateTest(unittest.TestCase):
    """
    Tests of ``transliterate.utils.translit``.
    """
    def setUp(self):
        self.latin_text = "Lorem ipsum dolor sit amet"
        self.armenian_text = u'Լօրեմ իպսում դoլoր սիտ ամետ'
        self.cyrillic_text = u'Лорем ипсум долор сит амет'
        self.georgian_text = u''

    @track_time
    def test_01_get_available_language_codes(self):
        """
        Test ``autodiscover`` and ``get_available_language_codes``.
        """
        res = get_available_language_codes()
        res.sort()
        c = ['ru', 'ka', 'hy']
        c.sort()
        self.assertEqual(res, c)
        return res

    @track_time
    def test_02_translit_latin_to_armenian(self):
        """
        Test transliteration from Latin to Armenian.
        """
        res = translit(self.latin_text, 'hy')
        self.assertEqual(res, u'Լօրեմ իպսում դօլօր սիտ ամետ')
        return res

    @track_time
    def __test_02_translit_latin_to_georgian(self):
        """
        Test transliteration from Latin to Georgian.
        """
        res = translit(self.latin_text, 'ka')
        self.assertEqual(res, u'')
        return res

    @track_time
    def test_03_translit_latin_to_cyrillic(self):
        """
        Test transliteration from Latin to Cyrillic.
        """
        res = translit(self.latin_text, 'ru')
        self.assertEqual(res, u'Лорем ипсум долор сит амет')
        return res

    @track_time
    def test_04_translit_armenian_to_latin(self):
        """
        Test transliteration from Armenian to Latin.
        """
        res = translit(self.armenian_text, 'hy', reversed=True)
        self.assertEqual(res, 'Lorem ipsum dolor sit amet')
        return res

    @track_time
    def __test_04_translit_georgian_to_latin(self):
        """
        Test transliteration from Georgian to Latin.
        """
        # TODO
        res = translit(self.georgian_text, 'ka', reversed=True)
        self.assertEqual(res, 'Lorem ipsum dolor sit amet')
        return res

    @track_time
    def test_05_translit_cyrillic_to_latin(self):
        """
        Test transliteration from Cyrillic to Latun.
        """
        res = translit(self.cyrillic_text, 'ru', reversed=True)
        self.assertEqual(res, 'Lorem ipsum dolor sit amet')
        return res

    @track_time
    def test_06_function_decorator(self):
        """
        Testing the function decorator from Latin to Armenian.
        """
        @transliterate_function(language_code='hy')
        def decorator_test_armenian(text):
            return text

        res = decorator_test_armenian(self.latin_text)
        self.assertEqual(res, u'Լօրեմ իպսում դօլօր սիտ ամետ')

    @track_time
    def test_07_method_decorator(self):
        """
        Testing the method decorator from Latin to Cyrillic.
        """
        class DecoratorTest(object):
            @transliterate_method(language_code='ru')
            def decorator_test_russian(self, text):
                return text

        res = DecoratorTest().decorator_test_russian(self.latin_text)
        self.assertEqual(res, u'Лорем ипсум долор сит амет')
        return res

    @track_time
    def test_08_function_decorator(self):
        """
        Testing the function decorator (reversed) from Armenian to Latin.
        """
        @transliterate_function(language_code='hy', reversed=True)
        def decorator_test_armenian_reversed(text):
            return text

        res = decorator_test_armenian_reversed(self.armenian_text)
        self.assertEqual(res, 'Lorem ipsum dolor sit amet')
        return res

    @track_time
    def test_09_register_custom_language_pack(self):
        """
        Testing registering of a custom language pack.
        """
        class ExampleLanguagePack(TranslitLanguagePack):
            """
            Example language pack.
            """
            language_code = "example"
            language_name = "Example"
            mapping = (
                u"abcdefghij",
                u"1234567890",
            )

        registry.register(ExampleLanguagePack)

        assert 'example' in get_available_language_codes()
        res = translit(self.latin_text, 'example')
        self.assertEqual(res, 'Lor5m 9psum 4olor s9t 1m5t')
        return res

    @track_time
    def test_10_translipsum_generator_armenian(self):
        """
        Testing the translipsum generator. Generating lorem ipsum paragraphs in Armenian.
        """
        g_am = TranslipsumGenerator(language_code='hy')
        res = g_am.generate_paragraph()
        assert res
        return res

    @track_time
    def test_11_translipsum_generator_cyrillic(self):
        """
        Testing the translipsum generator. Generating lorem ipsum sentence in Cyrillic.
        """
        g_ru = TranslipsumGenerator(language_code='ru')
        res = g_ru.generate_sentence()
        assert res
        return res

    @track_time
    def test_12_language_detection_armenian(self):
        """
        Testing language detection. Detecting Amenian.
        """
        res = detect_language(self.armenian_text)
        self.assertEqual(res, 'hy')
        return res

    @track_time
    def test_13_language_detection_cyrillic(self):
        """
        Testing language detection. Detecting Russian (Cyrillic).
        """
        res = detect_language(self.cyrillic_text)
        self.assertEqual(res, 'ru')
        return res

    @track_time
    def test_14_slugify_armenian(self):
        """
        Testing slugify from Armenian.
        """
        res = slugify(self.armenian_text)
        self.assertEqual(res, 'lorem-ipsum-dolor-sit-amet')
        return res

    @track_time
    def test_15_slugify_russian(self):
        """
        Testing slugify from Russian.
        """
        res = slugify(self.cyrillic_text)
        self.assertEqual(res, 'lorem-ipsum-dolor-sit-amet')
        return res

    @track_time
    def test_16_override_settings(self):
        """
        Testing settings override.
        """
        def override_settings():
            return get_setting('LANGUAGE_DETECTION_MAX_NUM_KEYWORDS')

        self.assertEqual(defaults.LANGUAGE_DETECTION_MAX_NUM_KEYWORDS, override_settings())

        set_setting('LANGUAGE_DETECTION_MAX_NUM_KEYWORDS', 10)
        
        self.assertEqual(10, override_settings())

        return override_settings()

    @track_time
    def __test_17_mappings(self):
        """
        Testing mappings.
        """
        for language_pack in get_available_language_packs():
            print 'Testing language pack %s %s' % (language_pack.language_code, language_pack.language_name)
            print 'Reversed test:'
            for letter in language_pack.mapping[1]:
                print letter, ' --> ', translit(letter, language_pack.language_code, reversed=True)

            print 'Normal test:'
            for letter in language_pack.mapping[0]:
                print letter, ' --> ', translit(letter, language_pack.language_code)


if __name__ == '__main__':
    unittest.main()
