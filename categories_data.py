from marketplace.models import Category

categories_data = [
    # PRODUCT CATEGORIES
    {'name': 'Electronics', 'icon': 'laptop', 'description': 'Laptops, phones, tablets, accessories, and electronic gadgets'},
    {'name': 'Textbooks & Books', 'icon': 'book', 'description': 'Course textbooks, novels, study guides, and reference materials'},
    {'name': 'Fashion & Clothing', 'icon': 'shirt', 'description': 'Clothing, shoes, bags, accessories, and fashion items'},
    {'name': 'Furniture', 'icon': 'couch', 'description': 'Chairs, tables, beds, wardrobes, and home furniture'},
    {'name': 'Sports & Fitness', 'icon': 'dumbbell', 'description': 'Sports equipment, gym gear, fitness accessories'},
    {'name': 'Musical Instruments', 'icon': 'music', 'description': 'Guitars, keyboards, drums, and other musical instruments'},
    {'name': 'Kitchen & Appliances', 'icon': 'utensils', 'description': 'Kitchen utensils, appliances, cookware, and dining items'},
    {'name': 'Beauty & Personal Care', 'icon': 'sparkles', 'description': 'Cosmetics, skincare, hair care, and grooming products'},
    {'name': 'Stationery & Supplies', 'icon': 'pen', 'description': 'Pens, notebooks, calculators, and school supplies'},
    {'name': 'Bicycles & Vehicles', 'icon': 'bike', 'description': 'Bicycles, motorcycles, scooters, and vehicle parts'},
    {'name': 'Gaming', 'icon': 'gamepad', 'description': 'Video games, consoles, controllers, and gaming accessories'},
    {'name': 'Art & Crafts', 'icon': 'palette', 'description': 'Art supplies, craft materials, paintings, and handmade items'},
    {'name': 'Photography', 'icon': 'camera', 'description': 'Cameras, lenses, tripods, and photography equipment'},
    {'name': 'Jewelry & Watches', 'icon': 'watch', 'description': 'Jewelry, watches, and fashion accessories'},
    {'name': 'Pet Supplies', 'icon': 'paw', 'description': 'Pet food, accessories, and care products'},
    
    # SERVICE CATEGORIES
    {'name': 'Tutoring & Academic Help', 'icon': 'graduation-cap', 'description': 'Private tutoring, assignment help, exam preparation'},
    {'name': 'Writing Services', 'icon': 'file-text', 'description': 'Essay writing, proofreading, editing, and content creation'},
    {'name': 'Tech & Programming', 'icon': 'code', 'description': 'Web development, app development, coding help, tech support'},
    {'name': 'Graphic Design', 'icon': 'image', 'description': 'Logo design, poster design, photo editing, digital art'},
    {'name': 'Photography & Videography', 'icon': 'video', 'description': 'Event photography, video editing, content creation'},
    {'name': 'Fitness & Training', 'icon': 'activity', 'description': 'Personal training, workout plans, fitness coaching'},
    {'name': 'Music & Entertainment', 'icon': 'music-note', 'description': 'Music lessons, DJ services, event entertainment'},
    {'name': 'Beauty Services', 'icon': 'scissors', 'description': 'Hair styling, makeup, nail services, beauty treatments'},
    {'name': 'Cleaning Services', 'icon': 'trash', 'description': 'Room cleaning, laundry services, organizing'},
    {'name': 'Food & Catering', 'icon': 'utensils-crossed', 'description': 'Meal prep, catering, baking, food delivery'},
    {'name': 'Transportation', 'icon': 'car', 'description': 'Ride services, delivery services, moving assistance'},
    {'name': 'Event Planning', 'icon': 'calendar', 'description': 'Party planning, event coordination, decoration services'},
    {'name': 'Repair & Maintenance', 'icon': 'wrench', 'description': 'Phone repair, laptop repair, electronics fixing'},
    {'name': 'Fashion & Styling', 'icon': 'shopping-bag', 'description': 'Personal styling, wardrobe consulting, fashion advice'},
    {'name': 'Language & Translation', 'icon': 'globe', 'description': 'Language tutoring, translation services, interpretation'},
    {'name': 'Research & Data', 'icon': 'bar-chart', 'description': 'Research assistance, data analysis, survey creation'},
    {'name': 'Marketing & Social Media', 'icon': 'megaphone', 'description': 'Social media management, digital marketing, content strategy'},
    {'name': 'Administrative Services', 'icon': 'clipboard', 'description': 'Virtual assistance, typing, data entry, documentation'},
    {'name': 'Counseling & Mentorship', 'icon': 'users', 'description': 'Career counseling, academic mentorship, life coaching'},
    {'name': 'Other Services', 'icon': 'more-horizontal', 'description': 'Miscellaneous services not listed above'},
]

created_count = 0
updated_count = 0

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'icon': cat_data['icon'],
            'description': cat_data['description'],
            'is_active': True
        }
    )
    
    if created:
        created_count += 1
        print(f"Created: {category.name}")
    else:
        category.icon = cat_data['icon']
        category.description = cat_data['description']
        category.is_active = True
        category.save()
        updated_count += 1
        print(f"Updated: {category.name}")

print(f"\nSummary:")
print(f"Created: {created_count} categories")
print(f"Updated: {updated_count} categories")
print(f"Total: {Category.objects.count()} categories")