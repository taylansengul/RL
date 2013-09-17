pickable_item_properties = 'pickable, drawable'
dictionary = {
    'apple': {
        'ID': 'apple',
        'color': 'blue',
        'description': 'yummy',
        'effects': [{'effects': 'hunger', 'change': [30], 'type': 'temporary'}],
        'icon': 'F',
        'image': 'eggplant_32.png',
        'properties': pickable_item_properties + 'edible, consumable, stackable',
        'type': 'game item'},
    'small medkit': {
        'ID': 'small medkit',
        'color': 'blue',
        'description': 'heals 1 hp for 2 turns',
        'effects': [{'effects': 'hp', 'change': [1, 1], 'type': 'temporary'}],
        'icon': 'm',
        'image': 'medkit_32.png',
        'properties': pickable_item_properties + 'drinkable, consumable, stackable',
        'type': 'game item'},
    'large medkit': {
        'ID': 'large medkit',
        'color': 'blue',
        'description': 'heals 2 hp for 2 turns',
        'effects': [{'effects': 'hp', 'change': [2, 2], 'type': 'temporary'}],
        'icon': 'M',
        'image': 'medkit_32.png',
        'properties': pickable_item_properties + 'drinkable, consumable, stackable',
        'type': 'game item'},
    'lantern': {
        'ID': 'lantern',
        'color': 'blue',
        'description': 'no usage',
        'icon': 'L',
        'properties': pickable_item_properties,
        'type': 'game item'}}