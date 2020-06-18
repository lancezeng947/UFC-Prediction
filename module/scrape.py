def remove_space_lines(text):
    pattern1 = re.compile(r'[\s\s+]')
    return re.sub(pattern1, ' ', text)


#Determine if observation is a title-bout
def find_belt(img_tag):
    try:
        image_link = img_tag['src']
        if re.match(r'.*belt.*', image_link) != None:
            return True
    except:
        return False
    
    
def get_fight_auxiliary(soup):
    '''
    Input: beautifulsoup of an event url: (ie. http://www.ufcstats.com/event-details/53278852bcd91e11)
    Outputs: pandas Series
        date, location, attendance
    '''
    
    table = []
    
    auxiliary_table = soup.find_all('li', {'class': 'b-list__box-list-item'})
    for item in auxiliary_table:
        attribute = remove_space_lines(item.text).strip()

        #If attribute is missing, replace with ''
        try:
            attribute = re.findall(r'\s\s+(.*)', attribute)[0]
        except:
            attribute = '' 
        
        table.append(attribute)
        
    table_series = pd.Series(table)
    table_series.index = ['date', 'location', 'attendance']
    
    if table_series['attendance'] != '':
        table_series['attendance'] = re.sub(',', '', table_series['attendance'])
        table_series['attendance'] = int(table_series['attendance'])
    
    table_series['date'] = dt.strptime(table_series['date'], '%B %d, %Y').strftime('%d-%m-%Y')

    return table_series



def get_page_stats(url):
    
    '''
    Input: url of an event page (ie. http://www.ufcstats.com/event-details/53278852bcd91e11)
    Outputs: Summary statistics in pandas DataFrame
    '''
    
    #Change url into BeautifulSoup object:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #Contents of the main table in HTML
    stat_table = soup.findAll('table')[0].contents 
    
    table_data = stat_table[3] #first 2 indices are empty strings, table_data is html starting from first table row
    detail_data = table_data.find_all('p') #within table rows, there are <p> labels for table text    
    #image_data = table_data.find_all('img') #get image links to find belt for 
    
    
    #Initialize return objects:
    contents = [] #table that will hold all statistics
    title_match_index = [] #list to track which fights are title_bouts
    
    #Loop through elements of detail_data (html table) to scrape fight details:
    for index, item in enumerate(detail_data):
        
        #find image of belt == title_bout
        image = item.find('img')
        if find_belt(image):
            title_match_index.append(index) #get index of fight in which belt appears
            
        #contents is list of all text from each element of table     
        contents.append(item.text)  

    
    #Clean up elements
    contents = list(map(lambda x: remove_space_lines(x), contents))
    contents = list(map(lambda x: x.strip(), contents)) 
    
    draw_index = []
    
    #When there's a draw or NC, additional tags are created --> remove the tag to reformat correctly   
    for i in np.arange(0, len(contents)-10, 16):

        if contents[i] != 'win':
            
            #Get the index of the match that was drawn & remove that element
            draw_index.append(np.floor_divide(i, 16)) 
            contents.pop(i)
                    
    #Extract links to more detailed fight statistics
    fight_links = table_data.find_all('a', {'class': 'b-flag b-flag_style_green'})
    fight_links = [item['href'] for item in fight_links]
    
    draw_links = table_data.find_all('a', {'class': 'b-flag b-flag_style_bordered'})
    draw_links = [item['href'] for item in draw_links]
    draw_links = list(dict.fromkeys(draw_links)) #Remove duplicate links from the drawn fights
    
    for index, link in zip(draw_index, draw_links):
        fight_links.insert(index, link)
    
    #each row of data is 16 elements: reformats 1 observation per row
    formatted_contents = np.array(contents).reshape((-1, 16))
    formatted_contents = pd.DataFrame(formatted_contents)
    
    #the first row is a list of 'wins'
    #formatted_contents.drop(0, axis = 1, inplace = True)
    
    #Run a floor_divide to put the image of the belt in the correct fight

    title_match = np.floor_divide(title_match_index, 16) 

    #Initialize title_bout column with all 0's
    titles = np.zeros(16)
    if len(title_match) != 0:
        titles[title_match] = 1
    
    title_series = pd.Series(titles)
    
    formatted_contents['title_bout'] = title_series
    
    #rename columns
    formatted_contents.columns = ['Winner', 'R_fighter', 'B_fighter', 'R_STR', 'B_STR', 
                               'R_TD', 'B_TD', 'R_SUB', 'R_SUB', 'R_PASS', 'B_PASS',
                              'WEIGHT_CLASS', 'METHOD', 'DETAIL', 'ROUND', 'TIME', 'title_bout']
    
    #convert columns to appropriate data types
    formatted_contents.replace('--', 99999, inplace = True)
    formatted_contents = formatted_contents.astype(data_types)
    formatted_contents['TIME'] = formatted_contents['TIME'].apply(lambda x: dt.strptime(x, '%M:%S').time())
    formatted_contents['link'] = fight_links
    
    auxiliary_data = get_fight_auxiliary(soup) #Returns date, location, attendance of event
    
    return (formatted_contents, auxiliary_data)


if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    import numpy as np
    import pandas as pd
    import re
    from html import unescape
    from datetime import datetime as dt
    import time
    print('imported!')
