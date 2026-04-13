"""Database seeding script"""

from config.database import get_db_connection, init_db


def seed_products():
    """Seed the products table with sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    products = [
        # Beer
        ('Carlsberg Lager 500ml', 'Beer', 'Lager', 2.50, 3.00, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Premium Danish lager'),
        ('Stella Artois 500ml', 'Beer', 'Lager', 2.75, 3.25, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Belgian premium lager'),
        ('Guinness Draught 440ml', 'Beer', 'Stout', 3.00, 3.50, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Iconic Irish stout'),
        ('Heineken 500ml', 'Beer', 'Lager', 2.60, 3.10, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Global premium lager'),
        ('Budweiser 500ml', 'Beer', 'Lager', 2.50, 2.99, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'American lager'),
        ('Corona Extra 330ml', 'Beer', 'Lager', 2.99, 3.49, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Mexican lager'),
        ('Amstel 500ml', 'Beer', 'Lager', 2.49, 2.99, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Dutch premium lager'),
        
        # Spirits
        ('Smirnoff Vodka 70cl', 'Spirits', 'Vodka', 14.99, 17.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Premium Russian vodka'),
        ('Gordon\'s Gin 70cl', 'Spirits', 'Gin', 15.49, 18.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Classic London dry gin'),
        ('Jack Daniel\'s 70cl', 'Spirits', 'Whiskey', 19.99, 24.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Tennessee whiskey'),
        ('Captain Morgan Spiced 70cl', 'Spirits', 'Rum', 14.99, 17.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Spiced Caribbean rum'),
        ('Jameson Irish Whiskey 70cl', 'Spirits', 'Whiskey', 16.99, 19.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Smooth Irish whiskey'),
        ('Absolut Vodka 70cl', 'Spirits', 'Vodka', 15.99, 18.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Swedish premium vodka'),
        ('Bacardi White Rum 70cl', 'Spirits', 'Rum', 13.99, 16.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Cuban white rum'),
        ('Chivas Regal 12YO 70cl', 'Spirits', 'Whiskey', 24.99, 29.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'Blended Scotch whisky'),
        ('Beefeater Gin 70cl', 'Spirits', 'Gin', 14.49, 17.99, 'https://images.unsplash.com/photo-1613063087254-66a9b71ec83a?w=300', 'London dry gin'),
        
        # Wine
        ('Barefoot Merlot 75cl', 'Wine', 'Red', 6.99, 8.99, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'California medium-bodied red'),
        ('Hardys Riesling 75cl', 'Wine', 'White', 7.49, 9.49, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'Australian crisp white'),
        ('Pink Elephant Rosé 75cl', 'Wine', 'Rosé', 8.99, 11.99, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'Light and fruity rosé'),
        ('Casillero del Diablo Cabernet Sauvignon 75cl', 'Wine', 'Red', 7.99, 9.99, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'Chilean full-bodied red'),
        ('Jacob\'s Creek Chardonnay 75cl', 'Wine', 'White', 7.49, 8.99, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'Australian buttery white'),
        ('Echo Falls Rosé 75cl', 'Wine', 'Rosé', 6.99, 8.49, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'Refreshing white Zinfandel'),
        ('Blossom Hill Sauvignon Blanc 75cl', 'Wine', 'White', 6.49, 7.99, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=300', 'Zesty South African white'),
        
        # Soft Drinks
        ('Coca-Cola 330ml', 'Soft Drinks', 'Cola', 1.50, 1.79, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Classic cola'),
        ('Red Bull 250ml', 'Soft Drinks', 'Energy', 3.49, 3.99, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Energy drink'),
        ('Fanta Orange 500ml', 'Soft Drinks', 'Fruit', 1.79, 2.09, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Orange soda'),
        ('Lucozade Energy 500ml', 'Soft Drinks', 'Energy', 2.29, 2.79, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Orange energy drink'),
        ('7UP Free 500ml', 'Soft Drinks', 'Fruit', 1.49, 1.79, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Lemon lime soda'),
        ('Dr Pepper 500ml', 'Soft Drinks', 'Fruit', 1.79, 2.09, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Unique flavor soda'),
        ('Sprite 500ml', 'Soft Drinks', 'Fruit', 1.79, 2.09, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Lemon lime soda'),
        ('Monster Energy 500ml', 'Soft Drinks', 'Energy', 2.99, 3.49, 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=300', 'Energy drink'),
        
        # Vapes
        ('Elf Bar 600 Puffs', 'Vapes', 'Disposables', 5.99, 7.99, 'https://images.unsplash.com/photo-1613710639612-9487e9d1d4eb?w=300', 'Disposable vape - mixed berry'),
        ('Lost Mary BM600', 'Vapes', 'Disposables', 5.99, 7.99, 'https://images.unsplash.com/photo-1613710639612-9487e9d1d4eb?w=300', 'Disposable vape - strawberry'),
        ('Oxbar Nexis 3500', 'Vapes', 'Pods', 14.99, 19.99, 'https://images.unsplash.com/photo-1613710639612-9487e9d1d4eb?w=300', 'Rechargeable pod system'),
        ('Elf Bar Crystal 600', 'Vapes', 'Disposables', 4.99, 6.99, 'https://images.unsplash.com/photo-1613710639612-9487e9d1d4eb?w=300', 'Crystal clear disposable'),
        ('GeekVape Aegis Legend 2', 'Vapes', 'Devices', 34.99, 44.99, 'https://images.unsplash.com/photo-1613710639612-9487e9d1d4eb?w=300', 'Advanced box mod'),
        ('Voopoo Drag X Plus', 'Vapes', 'Devices', 29.99, 39.99, 'https://images.unsplash.com/photo-1613710639612-9487e9d1d4eb?w=300', 'Portable pod mod'),
        
        # Tobacco
        ('Marlboro Red 20s', 'Tobacco', 'Cigarettes', 11.99, 13.99, 'https://images.unsplash.com/photo-1585128903994-9788298932a2?w=300', 'Full flavor cigarettes'),
        ('Benson & Hedges 20s', 'Tobacco', 'Cigarettes', 11.49, 13.49, 'https://images.unsplash.com/photo-1585128903994-9788298932a2?w=300', 'Premium cigarettes'),
        ('Golden Virginia 30g', 'Tobacco', 'Rolling', 12.99, 15.99, 'https://images.unsplash.com/photo-1585128903994-9788298932a2?w=300', 'Fine cut rolling tobacco'),
        ('Richmond Super Slims 20s', 'Tobacco', 'Cigarettes', 10.99, 12.99, 'https://images.unsplash.com/photo-1585128903994-9788298932a2?w=300', 'Slim cigarettes'),
        ('Peter Jackson 30g', 'Tobacco', 'Rolling', 11.99, 14.99, 'https://images.unsplash.com/photo-1585128903994-9788298932a2?w=300', 'Australian rolling tobacco'),
        
        # Snacks
        ('Walkers Cheese & Onion 24g', 'Snacks', 'Crisps', 1.29, 1.59, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Classic British crisps'),
        ('Doritos Cool Original 175g', 'Snacks', 'Crisps', 2.49, 2.99, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Tangy tortilla chips'),
        ('Haribo Starmix 350g', 'Snacks', 'Sweets', 3.49, 3.99, 'https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=300', 'Mixed fruit gummies'),
        ('Cadbury Dairy Milk 45g', 'Snacks', 'Chocolate', 1.09, 1.29, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Classic milk chocolate'),
        ('Pringles Original 200g', 'Snacks', 'Crisps', 2.99, 3.49, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Crispy potato chips'),
        ('Maltesers 37g', 'Snacks', 'Chocolate', 1.19, 1.49, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Honeycomb malted balls'),
        ('Skittles Fruits 150g', 'Snacks', 'Sweets', 1.79, 2.19, 'https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=300', 'Fruity chewy sweets'),
        ('Nestlé Kit Kat 4 Finger 41.5g', 'Snacks', 'Chocolate', 1.09, 1.29, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Wafer chocolate bar'),
        ('Toblerone 100g', 'Snacks', 'Chocolate', 3.49, 3.99, 'https://images.unsplash.com/photo-1621447504864-d8686e12698c?w=300', 'Swiss milk chocolate'),
        
        # Groceries
        ('Heinz Tomato Ketchup 570g', 'Groceries', 'Sauces', 3.29, 3.79, 'https://images.unsplash.com/photo-1598866594230-a7c12756260f?w=300', 'Classic tomato ketchup'),
        ('Hellmann\'s Mayonnaise 400ml', 'Groceries', 'Sauces', 3.49, 3.99, 'https://images.unsplash.com/photo-1598866594230-a7c12756260f?w=300', 'Creamy real mayonnaise'),
        ('Tropicana Orange Juice 1L', 'Groceries', 'Juices', 3.99, 4.49, 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=300', '100% orange juice'),
        ('PG Tips 80 Bags', 'Groceries', 'Tea', 3.49, 3.99, 'https://images.unsplash.com/photo-1597318181409-cf64d0b5d8a2?w=300', 'Great British tea'),
        ('Nescafé Classic 200g', 'Groceries', 'Coffee', 5.99, 6.99, 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300', 'Instant coffee granules'),
        ('Cereal Variety Pack 6x375g', 'Groceries', 'Breakfast', 8.99, 10.99, 'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?w=300', 'Assorted breakfast cereals'),
        ('Tinned Tomatoes 4x400g', 'Groceries', 'Pantry', 2.49, 2.99, 'https://images.unsplash.com/photo-1597318181409-cf64d0b5d8a2?w=300', 'Chopped tomatoes'),
        ('Long Grain Rice 2kg', 'Groceries', 'Pantry', 2.99, 3.49, 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300', 'Premium long grain rice'),
        ('Pasta Spaghetti 500g', 'Groceries', 'Pantry', 0.99, 1.29, 'https://images.unsplash.com/photo-1555949258-eb67b1ad0cf3?w=300', 'Italian spaghetti'),
        ('Olive Oil 500ml', 'Groceries', 'Pantry', 4.99, 5.99, 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300', 'Extra virgin olive oil'),
        
        # Cider
        ('Strongbow Rosé 500ml', 'Cider', 'Fruit', 2.99, 3.49, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Rosé cider'),
        ('Rekorderlig Wild Berries 500ml', 'Cider', 'Fruit', 3.49, 3.99, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Swedish cider'),
        ('Aspall Dry Cyder 500ml', 'Cider', 'Traditional', 2.79, 3.29, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Traditional English cider'),
        ('Magners Original 500ml', 'Cider', 'Fruit', 3.29, 3.79, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=300', 'Irish cloudy cider'),
        
        # More Groceries
        ('Brita Water Filter Cartridges 3 Pack', 'Groceries', 'Household', 14.99, 17.99, 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300', 'Water filter replacements'),
        ('Kitchen Roll 2 Roll', 'Groceries', 'Household', 3.49, 3.99, 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=300', 'Absorbent kitchen paper'),
        ('Washing Liquid 1.3L', 'Groceries', 'Household', 7.99, 9.99, 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=300', 'Liquid laundry detergent'),
        ('Dishwasher Tablets 30 Pack', 'Groceries', 'Household', 4.99, 5.99, 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=300', 'All in one tablets'),
        ('Bin Bags 50 Pack', 'Groceries', 'Household', 5.99, 6.99, 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=300', 'Black bin liners'),
        
        # More Beverages
        ('Lidocaine Coffee 750g', 'Beverages', 'Coffee', 8.99, 10.99, 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300', 'Premium ground coffee'),
        ('Tetley Tea 80 Bags', 'Beverages', 'Tea', 2.99, 3.49, 'https://images.unsplash.com/photo-1597318181409-cf64d0b5d8a2?w=300', 'British tea bags'),
        ('Yorkshire Tea 80 Bags', 'Beverages', 'Tea', 3.99, 4.49, 'https://images.unsplash.com/photo-1597318181409-cf64d0b5d8a2?w=300', 'Premium Yorkshire tea'),
        ('Twinings Earl Grey 50 Bags', 'Beverages', 'Tea', 3.49, 3.99, 'https://images.unsplash.com/photo-1597318181409-cf64d0b5d8a2?w=300', 'Classic Earl Grey'),
        ('Hot Chocolate Sachets 10 Pack', 'Beverages', 'Drinks', 2.49, 2.99, 'https://images.unsplash.com/photo-1542990243-2b9a2d54e451?w=300', 'Chocolate powder drink'),
        ('Milkshake Powder 750g', 'Beverages', 'Drinks', 6.99, 7.99, 'https://images.unsplash.com/photo-1542990243-2b9a2d54e451?w=300', 'Vanilla milkshake mix'),
    ]
    
    for product in products:
        try:
            cursor.execute('''
                INSERT INTO products (name, category, subcategory, price, original_price, image, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', product)
        except Exception as e:
            print(f"Error inserting {product[0]}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Seeded {len(products)} products!")

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Seeding products...")
    seed_products()
    print("Done!")
