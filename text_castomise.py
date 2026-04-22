from aiogram.utils.markdown import hlink

# text = link('VK', 'https://vk.com')
test = ['📣 Каналы — 0 👉 1000', '[🔥 Канал 1](https://t.me/)', '[🔥 Канал 2](https://t.me/)', '[🌐 Канал 3](https://t.me/)', '[🥕 Канал 4](https://t.me/)', '[🔞 Канал 5](https://t.me/)', '[🐾 Канал 6](https://t.me/)', '', '📣 Каналы — 1000 👉 5000', '[💋 Канал 1](https://t.me/)', '[🔞Канал 2](https://t.me/)', '', '🗯 Чаты', '[👌 Чат 1](https://t.me/)', '[🔞 Чат 2](https://t.me/)', '', '💦Здоровье',  '[👌 Сейф-Бокс](https://)']

last_test = []

def text_url(caption, url, caption2 = None, url2 = None): 
    if caption2 and url2:
        finally_text = hlink(caption, url) + ' ' + hlink(caption2, url2)
    else:
        finally_text = hlink(caption, url)
    return finally_text
last_test = []
for line in range(len(test)):
    if test[line]:
        if test[line][0] == '[':
            caption = ''
            url = ''
            for l in range(1, len(test[line])):
                if test[line][l] == ']':
                    url += test[line][l+1:]
                    break 
                else:
                    caption += test[line][l]
            url = list(url)
            last_url = ''
            for i in url:
                if i not in ['(', ')']:
                    last_url += i
            last_test.append(text_url(caption, last_url))
    else:
        last_test.append(test[line])


def generate_links(text):
    text_list = text.replace('\n', '').split(')')

    finally_text = ''
    for i,v in enumerate(text_list[:-1]):
        htext = (v.split('('))
        # if i in [10,20]:
        #     finally_text +=''.join('🌀━━━━━━━━━━━━━━━━━🌀\n')
        if len(htext) == 2:
            finally_text += ''.join(f'{text_url(htext[0], htext[1])}\n')
            # print(text_url(htext[0], htext[1]))
        elif len(htext) == 4:
            # print(text_url(htext[0], htext[1], caption2=htext[2], url2=htext[3]))
            finally_text += ''.join(f'{text_url(htext[0], htext[1], caption2=htext[2], url2=htext[3])}\n')
    print(finally_text)
    return finally_text