import requests
import json

def run(domain, credentials, timeout=5, mode='basic'):
    url = f'{domain}/api/now/sp/rectangle/fe379905db30320099f93691f0b8f571'

    payload_template = '{\"keyword\":\"*\",\"language\":\"\",\"variables\":{\"tags\":[]},\"resource\":\"\",\"kb_query\":\"\",\"social_query\":\"\",\"category_as_tree\":false,\"order\":\"relevancy,true\",\"start\":START_INDEX,\"end\":END_INDEX,\"attachment\":true,\"portal_suffix\":\"\",\"knowledge_fields\":[\"text\",\"summary\",\"description\",\"author\",\"sys_updated_on\",\"external\"],\"social_fields\":[\"profile\",\"views\",\"sys_updated_on\",\"votes\",\"answer_count\"]}'
    payload = json.dumps({'payload': payload_template.replace('START_INDEX', '0').replace('END_INDEX', '1')})
    headers = {
        'X-Usertoken': credentials['Token'],
        'Content-Type': 'application/json',
        'Cookie': None if credentials['Cookies'] == None else '; '.join([f"{key}={credentials['Cookies'][key]}" for key in credentials['Cookies']])
    }

    if headers['X-Usertoken'] == None:
        del headers['X-Usertoken']
    if headers['Cookie'] == None:
        del headers['Cookie']

    try:
        response = json.loads(requests.request('POST', url, headers=headers, data=payload, timeout=timeout).text)
    except:
        return f'[{domain}]\nThe site does not seem to be hosting knowledge base articles\n'

    def get_number_of_returned_articles(response_data):
        path = [
            'result',
            'data',
            'results',
            'meta',
            'returned_results',
        ]

        number_of_public_articles = response_data
        for x in path:
            if not x in number_of_public_articles:
                return -1
            number_of_public_articles = number_of_public_articles[x]
        return number_of_public_articles
    
    has_public_articles = get_number_of_returned_articles(response) > 0

    if mode == 'basic' or not has_public_articles:
        return f'[{domain}]\n{("is exposing" if has_public_articles else "does not expose")} knowledge base articles to the public\n'
    
    import re
    attachments_pattern = r'sys_attachment\.do\?sys_id=([0-9a-f]+)[^0-9a-f]'
    attachments = set()

    current_index = 0
    page_size = 1000
    number_of_public_articles = 0
    while True:
        try:
            payload = json.dumps({'payload': payload_template.replace('START_INDEX', str(current_index)).replace('END_INDEX', str(current_index + page_size))})
            raw_data = requests.request('POST', url, headers=headers, data=payload).text
            response = json.loads(raw_data)
            
            for attachment in re.findall(attachments_pattern, raw_data):
                attachments.add(attachment)

            number_of_returned_articles = get_number_of_returned_articles(response)
            number_of_public_articles += number_of_returned_articles
            if number_of_returned_articles != page_size:
                break
        except:
            return f'[{domain}]\nA total of {str(number_of_public_articles)} public articles and {str(len(attachments))} attachments had been discovered when an error occurred. Try scanning again later for a complete output\n'
        
        current_index += page_size

    import random
    all_attachments_accessible = True
    for attachment in random.choices(list(attachments), k=min(5, len(attachments))):
        try:
            url = f'{domain}/sys_attachment.do?sys_id={attachment}'
            response = requests.request('GET', url, headers=headers)
            if response.status_code != 200 or len(response.content) < 256:
                all_attachments_accessible = False
                break
        except:
            all_attachments_accessible = False
            break
    
    if len(attachments) == 0:
        return f'[{domain}]\nA total of {str(number_of_public_articles)} public articles but no {str(len(attachments))} attachments were found\n'
    
    if mode == 'deep':
        return f'[{domain}]\nA total of {str(number_of_public_articles)} public articles and {str(len(attachments))} attachments were found, {"and all the attachments" if all_attachments_accessible else "but the attachments do not"} seem to be accessible\n'

    if mode == 'complete':
        attachments_output = '\n'.join(list(map(lambda x: f'{domain}/sys_attachment.do?sys_id={x}&view=true', list(attachments))))
        return f'[{domain}]\nA total of {str(number_of_public_articles)} public articles and {str(len(attachments))} attachments were found, {"and all the attachments" if all_attachments_accessible else "but the attachments do not"} seem to be accessible.\nThese are all the discovered attachments:\n{attachments_output}\n'

    return f'[{domain}]\n{("is exposing" if has_public_articles else "does not expose")} knowledge base articles to the public\n'

