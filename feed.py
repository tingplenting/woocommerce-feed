from xml.etree import ElementTree as et
from sys import exit
from inc import cur

import re

def fetch_feed():
    stmt = """
    SELECT p.ID as pid, attachment.ID att_id, p.post_title as title, p.post_name as slug, p.post_content as content, pm.meta_value
    FROM wp_posts p
    INNER JOIN wp_posts attachment ON (attachment.post_parent = p.ID)
    INNER JOIN wp_postmeta pm ON (pm.post_id = attachment.ID)
    WHERE p.post_type = 'product'
    AND pm.meta_key = '_wp_attached_file'
    """

    cur.execute(stmt)
    rows = cur.fetchall()

    if not rows:
        exit("if not rows")

    return rows

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

site = "domain.com"
site_title = "Site Title"
campaign = 'shoppingfeed'
product_price = 'USD 20'
product_category = '187' # category for 'Shoes'
product_url = f'https://{site}/product/'
upload_path = f'https://{site}/wp-content/uploads/'

rss = et.Element('rss')
rss.set('xmlns:g', 'http://base.google.com/ns/1.0')
rss.set('version', '2.0')
channel = et.SubElement(rss, 'channel')

title = et.SubElement(channel, 'title')
title.text = 'Shopping Feed'
link = et.SubElement(channel, 'link')
link.text = f'https://{site}'
description = et.SubElement(channel, 'description')
description.text = f'{site_title} Google Shopping Data Feed XML'

for row in fetch_feed():

    product_id = row['pid']
    post_title = row['title']
    post_content = re.findall('<p.*?p>', row['content'], re.I | re.M)
    post_str = ''.join(post_content)
    content = clean_html(post_str)
    post_link = product_url + row['slug']
    image_link = upload_path + row['meta_value']
    sku = str(product_id) + "_unit"

    item = et.SubElement(channel, 'item')
    gid = et.SubElement(item, 'g:id')
    gid.text = str(product_id)
    gidentifier = et.SubElement(item, 'g:identifier_exists')
    gidentifier.text = 'no'
    gtitle = et.SubElement(item, 'g:title')
    gtitle.text = post_title
    gdesc = et.SubElement(item, 'g:description')
    gdesc.text = content
    glink = et.SubElement(item, 'g:link')
    glink.text = f"{post_link}/?utm_source=Google%20Shopping&utm_campaign={campaign}&utm_medium=cpc&utm_term={product_id}"
    gimage_link = et.SubElement(item, 'g:image_link')
    gimage_link.text = image_link
    gavailability = et.SubElement(item, 'g:availability')
    gavailability.text = 'in stock'
    gprice = et.SubElement(item, 'g:price')
    gprice.text = product_price
    ggoogle_product_category = et.SubElement(item, 'g:google_product_category')
    ggoogle_product_category.text = product_category
    gmpn = et.SubElement(item, 'g:mpn')
    gmpn.text = sku
    gcondition = et.SubElement(item, 'g:condition')
    gcondition.text = 'New'
    channel.append(item)

feed = et.tostring(rss, encoding="unicode")  
with open("google_shopping_feed.xml", "w") as f:
    f.write(feed)
