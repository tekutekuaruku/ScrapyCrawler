import scrapy

#set item
class Page(scrapy.Item):
    index = scrapy.Field()
    meta = scrapy.Field()
    url = scrapy.Field()
    short_title = scrapy.Field()
    html = scrapy.Field()
    summary_content = scrapy.Field()
    status = scrapy.Field()
    #Make logs an object representation that is easy for humans to read
    def __repr__(self):
        p = Page(self) #Get a page that duplicates this page
        if len(p['html']) > 100:
            p['html'] = p['html'][:100] + '...' #Omitted if longer than 100 characters
        return super(Page, p).__repr__() #Returns the string representation of the duplicated page