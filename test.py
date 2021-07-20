import unittest
from app import Urls

class TestApp(unittest.TestCase):

    def test_model(self):
        """
        GIVEN a Url model
        WHEN a new Url is created
        THEN check the "long" url and "short" url are defined correctly
        """
        url = Urls('https://blog.gds-gov.tech/terragrunt-in-retro-i-would-have-done-these-few-things-e5aaac451942', 'http://172.104.63.163/n4lm9')
        self.assertEqual(url.long,'https://blog.gds-gov.tech/terragrunt-in-retro-i-would-have-done-these-few-things-e5aaac451942')
        self.assertEqual(url.short,'http://172.104.63.163/n4lm9')

if __name__ == '__main__':
    unittest.main()