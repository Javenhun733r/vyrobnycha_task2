from flask import render_template, request, session, redirect, url_for
import requests
import json


class Client:
    def init(self, adress, requests_count=1000):
        self.adress = adress
        self.requests_count = requests_count
        self.free_node = ""
        self.loaded_node = ""
        self.count = 0

    def update_stats(self):
        if self.count == 0:
            stats = json.Loads(requests.get(self.adress + "/getstats").text)
            self.loaded_node = stats[max(stats.values())]
        self.count = (self.count + 1) % self.requests_count

    def read(self):
        self.update_starts()
        return json.loads(requests.get(self.loaded_node + "/readmessage").text)

    def write(self, message):
        self.update_stats()
        request.post(self.free_node + '/writemessage', data=json.dumps(message))