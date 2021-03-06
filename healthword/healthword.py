#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import sys

import requests
import yaml

__author__="nosmo@nosmo.me"

class SiteScanner(object):

    def __init__(self):
        self.site_sessions = {}

    def add_site(self, url, term):
        self.site_sessions[url] = {"term": term,
                                   "session": requests.Session()}
    def _test_site(self, url):
        session = self.site_sessions[url]["session"]
        term = self.site_sessions[url]["term"]

        try:
            req = session.get(url, verify=False)
        except requests.exceptions.ConnectionError as e:
            sys.stderr.write("%s: Couldn't connect to check site: %s\n" % (url, str(e)))
        except Exception as e:
            sys.stderr.write("%s: Got exception when connecting: %s\n" % (url, str(e)))
            sys.stderr.write(traceback.format_exc())

        if req.status_code != 200:
            sys.stderr.write("%s: Got a response code of %d!\n" % (url, req.status_code))
            return False
        if term not in req.text:
            sys.stderr.write("%s: Failed to read term \"%s\"\n" % (url, term))
            return False

        return True

    def test_sites(self):
        status = True

        for site in self.site_sessions:
            if not self._test_site(site):
                status = False
        return status

def main():

    config = yaml.load(open("healthword.yaml"))
    site_data = config["sites"]

    a = SiteScanner()
    for site, term in site_data.iteritems():
        a.add_site(site, term)
    a.test_sites()

if __name__ == '__main__':
    main()
