def url_parser():
    with open('/Users/cas/Projects/Plateful/image_urls.txt', 'r') as file:
        lines = file.readlines()

    urls = [line.split('https://', 1)[1].strip() for line in lines if 'https://' in line]

    with open('/Users/cas/Projects/Plateful/only_urls.txt', 'w') as file:
        for url in urls:
            file.write(f'https://{url}\n')
    
    print("URLs have been successfully parsed and saved to only_urls.txt")
    
url_parser()