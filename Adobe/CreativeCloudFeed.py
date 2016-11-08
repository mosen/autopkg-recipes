#!/usr/bin/python

import json
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["CreativeCloudFeed"]

URL = 'https://prod-rel-ffc-ccm.oobesaas.adobe.com/adobe-ffc-external/core/v4/products/all?&channel=ccm&channel=sti&platform=osx10&platform=osx10-64&payload=true&productType=Desktop&_type=json'

class CreativeCloudFeed(Processor):
    """Fetch information about product(s) from the Creative Cloud products feed."""

    input_variables = {
        "platform_id": {
            "default": "osx10-64",
            "description": "The deployment platform, defaults to osx10-64."
        },
        "product_id": {
            "description": "The product sap code"
        },
        "base_version": {
            "description": "The base product version"
        }
    }

    output_variables = {
        "product_info_url": {
            "description": "Product main information URL"
        },
        "icon_url": {
            "description": "Icon download URL"
        },
        "base_version": {
            "description": "The basic (major.minor) version"
        },
        "product_version": {
            "description": "The full length version"
        }
    }

    def main(self):
        product_id = self.get('product_id')
        base_version = self.get('base_version')

        req = urllib2.Request(URL, headers={
            'User-Agent': 'Creative Cloud',
            'x-adobe-app-id': 'AUSST_4_0',
        })
        data = json.loads(urllib2.urlopen(req).read())
        ccm_data = {}
        for channel in data['channel']:
            if channel['name'] == 'ccm':
                ccm_data.update(channel)

        matching_prods = []
        for prod in ccm_data['products']['product']:
            if prod['id'] != product_id:
                continue

            if prod['platforms']['platform'][0]['languageSet'][0].get('baseVersion') == base_version:
                matching_prods.append(prod)


if __name__ == "__main__":
    processor = CreativeCloudFeed()
    processor.execute_shell()

