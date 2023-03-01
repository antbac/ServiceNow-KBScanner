from credentials_retriever import retrieve_credentials
from scanner import run as run_scanner

def scan_url(domain, config):
    result = retrieve_credentials(domain, timeout=config['timeout'])
    if not result['ScanSuccessful']:
        print(f'[{domain}]\nThe site does not seem to be hosting knowledge base articles\n')
        return

    result = run_scanner(domain, result['Credentials'], timeout=config['timeout'], mode=config['mode'])
    print(result)

if __name__ == '__main__':
    config = {}
    with open('config.json') as f:
        import json
        config = json.load(f)

    import threading
    import time
    threads = [threading.Thread(target=scan_url, args=(domain[:-1] if domain.endswith('/') else domain, config,)) for domain in config['domains']]

    print()
    print('          STARTING SCAN          ')
    print('---------------------------------')
    print()

    active_threads = []
    for thread in threads:
        if len(active_threads) < config['parallelScans']:
            thread.start()
            active_threads.append(thread)
            continue

        while len(active_threads) == config['parallelScans']:
            for i in range(len(active_threads)):
                if not active_threads[i].is_alive():
                    active_threads.pop(i)
                    break
            time.sleep(0.2)
    
    while len(active_threads) > 0:
        if not active_threads[0].is_alive():
            active_threads.pop().join()
            continue
        time.sleep(0.2)
    
    print('---------------------------------')
    print('          SCAN COMPLETE          ')
    print()
        