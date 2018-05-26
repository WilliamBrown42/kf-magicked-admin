"""
    webhook.py
    Object for creating and POSTing messages to Discord webhooks.
"""

import json
import requests
import time
import datetime
import ast
from collections import defaultdict
#from utils.logger import logger

class Webhook:

    """Discord Webhook Embeds for Python

    Attributes:
        author (str): Username to display
        author_icon (str): URL of profile picture
        author_url (str): Username link destination
        color (int): Color code for embed object
        desc (str): Embed description
        fields (list): List of field objects
        footer (str): Embed footer text
        footer_icon (str): URL of footer icon
        image (str): URL of image to display in embed
        msg (str): Text to send
        thumbnail (str): URL of image thumbnail
        title (str): Embed title
        title_url (str): Embed title link destination
        ts (bool|int): `True` to use current timestamp or an `int` timestamp
        url (str): Destination to POST webhook JSON
    """

    def __init__(self, url, **kwargs):
        """
        Initialise a Webhook Embed Object

        Args:
            url (str): Destination to POST webhook JSON
            **kwargs: Webhook object parameters
        """

        self.url = url
        self.msg = kwargs.get('msg')
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.title_url = kwargs.get('title_url')
        self.author = kwargs.get('author')
        self.author_icon = kwargs.get('author_icon')
        self.author_url = kwargs.get('author_url')
        self.desc = kwargs.get('desc')
        self.fields = kwargs.get('fields', [])
        self.image = kwargs.get('image')
        self.thumbnail = kwargs.get('thumbnail')
        self.footer = kwargs.get('footer')
        self.footer_icon = kwargs.get('footer_icon')
        self.ts = kwargs.get('ts')

    def add_field(self, **kwargs):
        '''Adds a field to `self.fields`

        Args:
            **kwargs: Name, value, and inline parameters
        '''
        name = kwargs.get('name')
        value = kwargs.get('value')
        inline = kwargs.get('inline', True)

        field = {

            'name': name,
            'value': value,
            'inline': inline

        }

        self.fields.append(field)

    def set_desc(self, desc):
        """Sets the embed description

        Args:
            desc (str): Description
        """
        self.desc = desc

    def set_author(self, **kwargs):
        """Define info about message author

        Args:
            **kwargs: Author name, icon, and avatar URL
        """
        self.author = kwargs.get('name')
        self.author_icon = kwargs.get('icon')
        self.author_url = kwargs.get('url')

    def set_title(self, **kwargs):
        """Define embed title information

        Args:
            **kwargs: Title text and href
        """
        self.title = kwargs.get('title')
        self.title_url = kwargs.get('url')

    def set_thumbnail(self, url):
        """Define the image thumbnail for the embed

        Args:
            url (str): Thumbnail URL
        """
        self.thumbnail = url

    def set_image(self, url):
        """Define the full-size image for the embed

        Args:
            url (str): Image URL
        """
        self.image = url

    def set_footer(self, **kwargs):
        """Define the footer of the embed

        Args:
            **kwargs: Embed footer, icon, and timestamp
        """
        self.footer = kwargs.get('text')
        self.footer_icon = kwargs.get('icon')
        ts = kwargs.get('ts')
        if ts is True:
            self.ts = str(datetime.datetime.utcfromtimestamp(time.time()))
        elif ts:
            self.ts = str(datetime.datetime.utcfromtimestamp(ts))

    def del_field(self, index):
        """Remove a field from the embed

        Args:
            index (int): Field to remove
        """
        self.fields.pop(index)

    @property
    def json(self):
        """Formats the data into a payload

        Returns:
            dict: JSON-formatted version of Webhook data
        """

        data = {}

        data["embeds"] = []
        embed = defaultdict(dict)
        if self.msg:
            data["content"] = self.msg
        if self.author:
            embed["author"]["name"] = self.author
        if self.author_icon:
            embed["author"]["icon_url"] = self.author_icon
        if self.author_url:
            embed["author"]["url"] = self.author_url
        if self.color:
            embed["color"] = self.color
        if self.desc:
            embed["description"] = self.desc
        if self.title:
            embed["title"] = self.title
        if self.title_url:
            embed["url"] = self.title_url
        if self.image:
            embed["image"]['url'] = self.image
        if self.thumbnail:
            embed["thumbnail"]['url'] = self.thumbnail
        if self.footer:
            embed["footer"]['text'] = self.footer
        if self.footer_icon:
            embed['footer']['icon_url'] = self.footer_icon
        if self.ts:
            embed["timestamp"] = self.ts

        if self.fields:
            embed["fields"] = []
            for field in self.fields:
                f = {}
                f["name"] = field['name']
                f["value"] = field['value']
                f["inline"] = field['inline']
                embed["fields"].append(f)

        data["embeds"].append(dict(embed))

        empty = all(not d for d in data["embeds"])

        if empty and 'content' not in data:
            print('You cant post an empty payload.')
        if empty:
            data['embeds'] = []

        return json.dumps(data, indent=4)

	def post(self, rate_limit_remaning):
		"""
		Send the JSON formated object to the specified `self.url`.
		"""

		headers = {'Content-Type': 'application/json'}
        # Should hand back the things needed to deal with rate limits Here
        #https://developer.twitter.com/en/docs/basics/rate-limiting.html
        #https://github.com/Rapptz/discord.py/blob/async/discord/ext/commands/cooldowns.py
		# Needs to make this into actual limitor
		# switch to epoch time?
		if rate_limit_remaning < 2:
			print("Slow down bucko")
			#int(time.time())
			time.sleep(10) # This should be done better
			# How to deal with this?
			#print(str(result_dict['X-RateLimit-Limit']) + str(result_dict['X-RateLimit-Remaining']))
		else:
			result = requests.post(self.url, data=self.json, headers=headers)
			print("You good fam")
			#print(str(result_dict['X-RateLimit-Limit']) + str(result_dict['X-RateLimit-Remaining']))

        # Change this to proper debugging
        if result.status_code == 209:
            print("Payload delivered successfuly")
		elif result.status_code == 409:
			print("Post Failed, you are being rate limited. error 409")
		elif result.status_code == 400:
            print("Post Failed, error 400")
        else:
			print("Code : "+str(result.status_code))

        result_headers = result.headers
        result_dict = ast.literal_eval(str(result_headers))
        print(str(result_dict['X-RateLimit-Limit']) + str(result_dict['X-RateLimit-Remaining']))
        return int(result_dict['X-RateLimit-Remaining'])
