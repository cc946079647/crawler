from bs4 import BeautifulSoup

html = '<p><a href = www.bing.cn >a text<img>img text</img><h3>h3 text<p> p text</p></h3></a></p>'

css_exp = 'p > a'
soup = BeautifulSoup(html, 'html.parser')
findings = soup.select(css_exp)
for finding in findings:
    #text when finding has no tag embedded
    print finding.string
    #text when finding has no tag emneddend
    #list when finding has embedded,the first is the text,then followed embedded tags
    # depth=1,eg <a>a text <h3><p></p></h3?</a>,[a text,<h3><p></p></h3>]
    print finding.contents
    if isinstance(finding.contents, list):
        for content in finding.contents:
            print type(content), content
    #text and if existing,embedded tags as string
    print finding.get_text()
    print finding.get('href')
