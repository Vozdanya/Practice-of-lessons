from fastapi import Body

examples = [
    {"title": "Сочи Парк Отель", "location": "Континентальный просп., 6, п. г. т. Сириус"},
    {"title": "Sls Dubai Hotel & Residences", "location": "Sls Dubai Hotel & Residences, Бизнес Бей, эмират Дубай"},
]

examples_create_hotel = Body(openapi_examples={
    '1': {
        'summary': 'Сочи',
        'value': examples[0]
    },
    '2': {
        'summary': 'Дубай',
        'value': examples[1]
    }
})