import scrapy

"""
The command to generate stand alone spider is 
scrapy genspider table espn.com
"""
# the utility function to get five rows
def fifth(lst):
    start = 0
    end = 5
    while end <=len(lst):
        yield lst[start:end]
        start +=5
        end += 5
        
    
class TableSpider(scrapy.Spider):
    name = "table"
   # allowed_domains = ["espn.com"]
    start_urls = ["https://www.espn.com/soccer/standings/_/league/UEFA.CHAMPIONS/"]

    def parse(self, response):
        dt ={}
        team_rows = response.css('table')[0].css('tr')
        detail_rows = response.css('table')[1].css('tr')
        
        for group,group_detail in zip(
            fifth(team_rows),
            fifth(detail_rows)
            ):
            group_label = group[0].css("td span::text").get()
            dt[group_label] ={}
            for team ,detail in zip(group[1:],group_detail[1:]):
                team_label = team.css("td span.hide-mobile a::text").get()
                table_details =detail.css('td span::text').getall()
                dt[group_label][team_label]={
                    "wins":table_details[1],
                    "draw":table_details[2],
                    "loses":table_details[3],
                    "points":table_details[-1],
                }
                
                
        yield dt
           
        
