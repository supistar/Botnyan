# -*- encoding:utf8 -*-

import re

DOCUMENTS = [
    {
        'Keywords': [
            'いらっしゃい',
            'いつもの',
            'ぱちん',
            'パチン',
            'パッチン',
            'おーい',
            '設定要求'
        ],
        'DocumentID': '16ArfIOBjMB4moqgOoEYJtKWfb5-xB1NkWQXHVBWf6h0'
    },
    {
        'Keywords': 'チャンネル一覧',
        'DocumentID': '1i8yhKieTHRJb8mhOU5i9y-VQ0BJqLBeSSprxkaNkZXA'
    },
    {
        'Keywords': '地域チャンネル',
        'DocumentID': '1fb2ls79RPflv4AIQbNFZCDkrkEHvuH4ZYosVPjgnYQQ'
    }
]

BOTNAME = 'botnyan'
RE_FLAGS = re.IGNORECASE
