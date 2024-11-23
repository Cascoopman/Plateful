import logging
from os import getenv

import requests
from dotenv import load_dotenv

logging.basicConfig

load_dotenv()


class Language:
    Arabic = 'ara'
    Bulgarian = 'bul'
    Chinese_Simplified = 'chs'
    Chinese_Traditional = 'cht'
    Croatian = 'hrv'
    Danish = 'dan'
    Dutch = 'dut'
    English = 'eng'
    Finnish = 'fin'
    French = 'fre'
    German = 'ger'
    Greek = 'gre'
    Hungarian = 'hun'
    Korean = 'kor'
    Italian = 'ita'
    Japanese = 'jpn'
    Norwegian = 'nor'
    Polish = 'pol'
    Portuguese = 'por'
    Russian = 'rus'
    Slovenian = 'slv'
    Spanish = 'spa'
    Swedish = 'swe'
    Turkish = 'tur'


class OcrClient:
    def __init__(
        self,
        endpoint='https://api.ocr.space/parse/image',
        api_key=getenv('OCR_API_KEY'),
        language=Language.English,
        ocr_engine=2,
    ):
        """
        :param endpoint: API endpoint to contact
        :param api_key: API key string
        :param language: document language
        :param **kwargs: other settings to API
        """
        self.endpoint = endpoint
        self.payload = {
            'isOverlayRequired': True,
            'apikey': api_key,
            'language': language,
            'OCREngine': ocr_engine,
        }

    def _parse(self, raw):
        if isinstance(raw, str):
            raise ValueError(raw)

        if raw['IsErroredOnProcessing']:
            raise RuntimeError(raw['ErrorMessage'][0])

        logging.debug("Processing time (ms): %s", raw.get('ProcessingTimeInMillisencds'))

        parsed_lines = []

        lines = raw.get('ParsedResults', [])[0].get('TextOverlay', {}).get('Lines', [])

        for line in lines:
            line_text = line.get('LineText', '')

            words = line.get('Words', [])
            parsed_words = [{
                'WordText': word.get('WordText', ''),
                'Left': int(word.get('Left', 0)),
                'Top': int(word.get('Top', 0)),
                'Height': int(word.get('Height', 0)),
                'Width': int(word.get('Width', 0))} for word in words
                ]

            parsed_lines.append({'LineText': line_text, 'Words': parsed_words})

        logging.debug(parsed_lines)

        return parsed_lines

    def ocr_file(self, fp):
        """
        Process image from a local path.
        :param fp: A path or pointer to your file
        :return: Result in JSON format
        """
        with (open(fp, 'rb') if type(fp) == str else fp) as f:
            r = requests.post(
                self.endpoint,
                files={'filename': f},
                data=self.payload,
            )
        return self._parse(r.json())

    def ocr_url(self, url):
        """
        Process an image at a given URL.
        :param url: Image url
        :return: Result in JSON format.
        """
        data = self.payload
        data['url'] = url
        r = requests.post(
            self.endpoint,
            data=data,
        )
        return self._parse(r.json())

    def ocr_base64(self, base64image):
        """
        Process an image given as base64.
        :param base64image: Image represented as Base64
        :return: Result in JSON format.
        """
        data = self.payload
        data['base64Image'] = base64image
        r = requests.post(
            self.endpoint,
            data=data,
        )
        return self._parse(r.json())
