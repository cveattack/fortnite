import requests

class checkers:
    @staticmethod
    def locker(token:str, id:str) -> tuple:
        cosmetics_arrays = {}
        cosmetics_name_and_info_arrays= {}
        seasonsinfo = {}
        mythicskins = [i.strip() for i in open('mythicskins.txt','r',encoding='utf-8').readlines()]
        #print(mythicskins)

        r = requests.post('https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{}/client/QueryProfile?profileId=athena'.format(id),
                        json={},headers={'Authorization':'bearer {}'.format(token),'Accept':'application/json'}).json()

        for i in r['profileChanges'][0]['profile']['items']:
            tid = r['profileChanges'][0]['profile']['items'][i]['templateId']
            if tid.startswith('Athena'):
                idclean = tid.split(':')[1]
                if tid.split(':')[0] not in cosmetics_arrays:
                    cosmetics_arrays[tid.split(':')[0]]=[]
                    cosmetics_name_and_info_arrays[tid.split(':')[0]]=[]
                cosmetics_arrays[tid.split(':')[0]].append(idclean)

        for i in cosmetics_arrays:
            try:
                print(f'<<<<<<<<<<<<<<{i}>>>>>>>>>>>>>')
                listoflists = []
                for _i in range(0, len(cosmetics_arrays[i]), 50):
                    sublist = cosmetics_arrays[i][_i:_i+50]
                    listoflists.append(sublist)
                for cosm in listoflists:
                    r2 = requests.get('https://fortnite-api.com/v2/cosmetics/br/search/ids?language=en&id={}'.format('&id='.join(cosm)))
                    print(r2.text)
                    for i1 in r2.json()['data']:
                        if i == 'AthenaDance':
                            if i1['type']['value'] != 'emote':
                                continue
                        if i1['name'] in mythicskins:
                            i1['rarity']['value'] = 'mythic'
                        #print(i1['name'])
                        cosmetics_name_and_info_arrays[i].append([i1['name'],i1['images']['smallIcon'],i1['rarity']['value']])
            except Exception as e:
                print(e)

        for i in r['profileChanges'][0]['profile']['stats']['attributes']['past_seasons']:
            seasonsinfo[i['seasonNumber']] = [i['seasonLevel'],i['purchasedVIP'],i['bookLevel'],i['numWins']]
        
        curses = r['profileChanges'][0]['profile']['stats']['attributes']
        return cosmetics_arrays, cosmetics_name_and_info_arrays, seasonsinfo, [curses['book_purchased'],curses['level'],curses['book_level'],curses['season']['numWins']]