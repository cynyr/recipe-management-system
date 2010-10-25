#!/usr/bin/env python
from __future__ import print_function
from PrintOut import Recipe,do_print_out
import urllib2,re

class Allrecipes(Recipe):
    """ A recipe class that knows how to deal with http://allrecipes.com"""
    
    def __init__(self, url, *args,**kwords):
        Recipe.__init__(self,*args, **kwords)

        self.re_div = """<div class=\"%s\".*?<\/div>"""
        self.re_span = """<span class=\"%s\".*?<\/span>"""
        self.re_title = """(?<=<title>)\s*([\w\-\.]+ *?)+(?=\s*</title)"""
        self.re_preptime = r"(?<=Prep Time: )(\w+ *)+(?=Cook)"
        self.re_cooktime = r"(?<=Cook Time: )(\w+ *)+(?=Ready)"
        self.re_tag = r"<.*?>"
        self.re_ul_list = r"<ul>.*?</ul>"
        self.re_ol_list = r"<ol>.*?</ol>"
        self.re_multispace = r"\s{2,}"
        self.re_list_tags = r"(\s*</*?ul>\s*)|(\s*<li.*?>\s*)|(\s*</*?ol>\s*)"
        self.re_span_tags = r"\s*</*span.*?>"

        self.url=url

        self._get_recipe_html_text()
        self._get_title()
        self._get_times()
        self._get_author()
        self._get_ingredients()
        self._get_directions()
    
    def _get_recipe_html_text(self,):
        """Gets the whole html page for a recipe."""
        self.html = urllib2.urlopen(self.url)
        self.html = "".join(self.html.readlines())
    
    def _get_div(self,string):
        """Gets a div with the class=string """
        m = re.search(self.re_div % (string,), self.html, re.DOTALL)
        if m:
            return m.group(0)
        return string
    
    def _get_times_div(self,):
        """Returns the text for the div with the class="times" """
        return self._get_div("times")
    
    def _get_author_div(self,):
        """Returns the text for the div with the class="author-name" """
        return self._get_div("author-name")
    
    def _get_ingredients_div(self,):
        """Returns the text for the div with the class="ingredients" """
        return self._get_div("ingredients")

    def _get_directions_div(self,):
        """Returns the text for the div with the class="directions" """
        return self._get_div("directions")
    
    def _get_list(self, string):
        """Returns the html of a <ul> or <ol> html list."""
        m = re.search(self.re_ol_list, string, re.DOTALL)
        if m:
            return m.group(0)
        else:
            m = re.search(self.re_ul_list, string, re.DOTALL)
            if m:
                return m.group(0)
        return string

    def _rm_tags(self, s):
        """Remove all <.*> from string"""
        return re.sub(self.re_tag,"", s).strip()

    def _rm_multispace(self, s):
        """Removes all double \s from string)"""
        #re.sub() is recursive
        #even though 4 spaces would become 2 it ends up as 1
        return re.sub(self.re_multispace," ",s)

    def _rm_list_tags(self, s):
        """Removes all list tags from string"""
        return re.sub(self.re_list_tags, "", s)

    def _rm_span_tags(self, s):
        """Removes all span tags from string"""
        return re.sub(self.re_span_tags, "", s)
    
    def _get_times(self,):
        """Sets the Prep and Cook times from self.html"""
        s = self._rm_multispace(self._rm_tags(self._get_times_div()))
        m = re.search(self.re_preptime, self._rm_multispace(s))
        if m:
            self.Preptime = m.group(0).strip()
        m = re.search(self.re_cooktime, s)
        if m:
            self.Cooktime = m.group(0).strip()
    
    def _get_title(self,):
        """Sets the title from self.html"""
        m = re.search(self.re_title, self.html, re.DOTALL)
        if m:
            self.Title = m.group(0).strip()
            self.Title = self.Title.replace(" Recipe - Allrecipes.com","")
    
    def _get_author(self,):
        "Sets the author from self.html"""
        div=self._get_author_div()
        s = self._rm_multispace(self._rm_tags(div))
        self.Author = re.sub(r"[\;,\']|(By:)|(&nbsp)", "", s).strip()
    
    def _get_ingredients(self,):
        """Sets the Ingredients from self.html"""
        div = self._get_ingredients_div()
        ings = self._rm_multispace(self._get_list(div))
        ings = self._rm_list_tags(ings)
        li = "</li>"
        self.Ingredients = ings.strip(li).split(li)

    def _get_directions(self,):
        """Sets the Instructions from self.html"""
        div = self._get_directions_div()
        dirs = self._rm_multispace(self._get_list(div))
        dirs = self._rm_span_tags(self._rm_list_tags(dirs))
        li = "</li>"
        self.Instructions = [x.strip() for x in dirs.strip(li).split(li)]

if __name__ == "__main__":
    import sys

    if "--help" in sys.argv or "-h" in sys.argv:
        print("Takes a Allrecipes.com url and makes a 4x6 note card")

    for x in sys.argv[1:]:
        r = Allrecipes(x)
        do_print_out(r,(4,6))
