from django.core.management.base import BaseCommand
from marketplace.models import Category


class Command(BaseCommand):
    help = 'Populate database with marketplace categories'

    def handle(self, *args, **kwargs):
        categories_data = [
    # ELECTRONICS & TECHNOLOGY
    {'name': 'Electronics', 'icon': 'laptop', 'description': 'Laptops, phones, tablets, accessories, and electronic gadgets'},
    {'name': 'Gaming', 'icon': 'gamepad', 'description': 'Video games, consoles, controllers, and gaming accessories'},
    {'name': 'Photography', 'icon': 'camera', 'description': 'Cameras, lenses, tripods, and photography equipment'},
    {'name': 'Audio & Headphones', 'icon': 'headphones', 'description': 'Headphones, speakers, earbuds, and audio equipment'},
    {'name': 'Computer Accessories', 'icon': 'mouse', 'description': 'Keyboards, mice, monitors, cables, and PC accessories'},
    {'name': 'Smart Devices', 'icon': 'smartphone', 'description': 'Smart watches, fitness trackers, smart home devices'},
    
    # EDUCATION & BOOKS
    {'name': 'Textbooks & Books', 'icon': 'book', 'description': 'Course textbooks, novels, study guides, and reference materials'},
    {'name': 'Stationery & Supplies', 'icon': 'pen', 'description': 'Pens, notebooks, calculators, and school supplies'},
    {'name': 'Educational Materials', 'icon': 'book-open', 'description': 'Study materials, flashcards, educational tools'},
    
    # FASHION & ACCESSORIES
    {'name': 'Fashion & Clothing', 'icon': 'shirt', 'description': 'Clothing, shoes, bags, accessories, and fashion items'},
    {'name': 'Jewelry & Watches', 'icon': 'watch', 'description': 'Jewelry, watches, and fashion accessories'},
    {'name': 'Shoes & Footwear', 'icon': 'shoe', 'description': 'Sneakers, boots, sandals, and all types of footwear'},
    {'name': 'Bags & Luggage', 'icon': 'briefcase', 'description': 'Backpacks, handbags, suitcases, and travel bags'},
    {'name': 'Sunglasses & Eyewear', 'icon': 'glasses', 'description': 'Sunglasses, prescription glasses, and eyewear accessories'},
    
    # HOME & LIVING
    {'name': 'Furniture', 'icon': 'couch', 'description': 'Chairs, tables, beds, wardrobes, and home furniture'},
    {'name': 'Kitchen & Appliances', 'icon': 'utensils', 'description': 'Kitchen utensils, appliances, cookware, and dining items'},
    {'name': 'Home Decor', 'icon': 'home', 'description': 'Wall art, decorative items, plants, and home accessories'},
    {'name': 'Bedding & Bath', 'icon': 'bed', 'description': 'Bedsheets, towels, pillows, and bathroom accessories'},
    {'name': 'Lighting', 'icon': 'lightbulb', 'description': 'Lamps, LED lights, fairy lights, and lighting fixtures'},
    {'name': 'Storage & Organization', 'icon': 'box', 'description': 'Storage boxes, organizers, shelving, and space solutions'},
    {'name': 'Garden & Outdoor', 'icon': 'tree', 'description': 'Plants, gardening tools, outdoor furniture, and decor'},
    
    # HEALTH & BEAUTY
    {'name': 'Beauty & Personal Care', 'icon': 'sparkles', 'description': 'Cosmetics, skincare, hair care, and grooming products'},
    {'name': 'Health & Wellness', 'icon': 'heart-pulse', 'description': 'Vitamins, supplements, health monitors, wellness products'},
    {'name': 'Fragrances', 'icon': 'spray', 'description': 'Perfumes, colognes, body sprays, and fragrances'},
    
    # SPORTS & OUTDOORS
    {'name': 'Sports & Fitness', 'icon': 'dumbbell', 'description': 'Sports equipment, gym gear, fitness accessories'},
    {'name': 'Outdoor & Camping', 'icon': 'tent', 'description': 'Camping gear, hiking equipment, outdoor adventure items'},
    {'name': 'Bicycles & Vehicles', 'icon': 'bike', 'description': 'Bicycles, motorcycles, scooters, and vehicle parts'},
    {'name': 'Swimming & Water Sports', 'icon': 'waves', 'description': 'Swimwear, goggles, water sports equipment'},
    
    # HOBBIES & ENTERTAINMENT
    {'name': 'Musical Instruments', 'icon': 'music', 'description': 'Guitars, keyboards, drums, and other musical instruments'},
    {'name': 'Art & Crafts', 'icon': 'palette', 'description': 'Art supplies, craft materials, paintings, and handmade items'},
    {'name': 'Collectibles & Antiques', 'icon': 'trophy', 'description': 'Collectible items, vintage goods, memorabilia'},
    {'name': 'Board Games & Puzzles', 'icon': 'puzzle', 'description': 'Board games, card games, puzzles, and tabletop games'},
    {'name': 'Movies & Music', 'icon': 'film', 'description': 'DVDs, CDs, vinyl records, and media collections'},
    
    # BABY & KIDS
    {'name': 'Baby Products', 'icon': 'baby', 'description': 'Baby care items, diapers, feeding supplies, nursery items'},
    {'name': 'Toys & Games', 'icon': 'toy-brick', 'description': 'Children\'s toys, educational games, and play items'},
    {'name': 'Kids Fashion', 'icon': 'shirt', 'description': 'Children\'s clothing, shoes, and accessories'},
    
    # PETS
    {'name': 'Pet Supplies', 'icon': 'paw', 'description': 'Pet food, accessories, and care products'},
    {'name': 'Pet Furniture & Accessories', 'icon': 'dog', 'description': 'Pet beds, cages, carriers, and furniture'},
    
    # AUTOMOTIVE
    {'name': 'Auto Parts & Accessories', 'icon': 'car', 'description': 'Car parts, accessories, tools, and maintenance items'},
    {'name': 'Motorcycle Parts', 'icon': 'bike', 'description': 'Motorcycle parts, gear, and accessories'},
    
    # FOOD & BEVERAGES
    {'name': 'Food & Snacks', 'icon': 'pizza', 'description': 'Packaged foods, snacks, beverages, and treats'},
    {'name': 'Coffee & Tea', 'icon': 'coffee', 'description': 'Coffee beans, tea leaves, brewing equipment'},
    
    # OFFICE & BUSINESS
    {'name': 'Office Supplies', 'icon': 'briefcase', 'description': 'Office equipment, desk accessories, business supplies'},
    {'name': 'Printing & Paper', 'icon': 'printer', 'description': 'Printers, ink, paper, and printing supplies'},
    
    # MISCELLANEOUS PRODUCTS
    {'name': 'Handmade & Custom', 'icon': 'hand', 'description': 'Handcrafted items, custom-made products, artisan goods'},
    {'name': 'Gift Items', 'icon': 'gift', 'description': 'Gift sets, greeting cards, gift wrapping supplies'},
    {'name': 'Party Supplies', 'icon': 'party-popper', 'description': 'Party decorations, balloons, themed supplies'},
    {'name': 'Other Products', 'icon': 'more-horizontal', 'description': 'Miscellaneous items not listed above'},
    
    # ========== SERVICE CATEGORIES ==========
    
    # EDUCATIONAL SERVICES
    {'name': 'Tutoring & Academic Help', 'icon': 'graduation-cap', 'description': 'Private tutoring, assignment help, exam preparation'},
    {'name': 'Language & Translation', 'icon': 'globe', 'description': 'Language tutoring, translation services, interpretation'},
    {'name': 'Test Preparation', 'icon': 'clipboard-check', 'description': 'SAT, GRE, GMAT, IELTS, TOEFL preparation services'},
    {'name': 'Career Counseling', 'icon': 'briefcase', 'description': 'Career guidance, resume writing, interview preparation'},
    {'name': 'Online Courses', 'icon': 'monitor', 'description': 'Online learning, video courses, skill development'},
    
    # CREATIVE SERVICES
    {'name': 'Graphic Design', 'icon': 'image', 'description': 'Logo design, poster design, photo editing, digital art'},
    {'name': 'Writing Services', 'icon': 'file-text', 'description': 'Essay writing, proofreading, editing, and content creation'},
    {'name': 'Video Editing', 'icon': 'video', 'description': 'Video production, editing, animation, and post-production'},
    {'name': 'Photography & Videography', 'icon': 'camera', 'description': 'Event photography, video coverage, content creation'},
    {'name': 'Music Production', 'icon': 'music-note', 'description': 'Music composition, mixing, mastering, sound design'},
    {'name': 'Voice Over Services', 'icon': 'mic', 'description': 'Voice recording, narration, dubbing services'},
    {'name': '3D Modeling & Animation', 'icon': 'cube', 'description': '3D design, modeling, rendering, and animation'},
    
    # TECH SERVICES
    {'name': 'Tech & Programming', 'icon': 'code', 'description': 'Web development, app development, coding help, tech support'},
    {'name': 'Website Development', 'icon': 'layout', 'description': 'Website design, development, and maintenance'},
    {'name': 'Mobile App Development', 'icon': 'smartphone', 'description': 'iOS and Android app development'},
    {'name': 'IT Support', 'icon': 'hard-drive', 'description': 'Technical support, troubleshooting, IT consulting'},
    {'name': 'Database Services', 'icon': 'database', 'description': 'Database design, management, and optimization'},
    {'name': 'Cybersecurity', 'icon': 'shield', 'description': 'Security audits, penetration testing, protection services'},
    {'name': 'Cloud Services', 'icon': 'cloud', 'description': 'Cloud setup, migration, and management services'},
    
    # BUSINESS SERVICES
    {'name': 'Marketing & Social Media', 'icon': 'megaphone', 'description': 'Social media management, digital marketing, content strategy'},
    {'name': 'SEO & Content Marketing', 'icon': 'search', 'description': 'SEO optimization, content marketing, link building'},
    {'name': 'Business Consulting', 'icon': 'trending-up', 'description': 'Business strategy, planning, and consulting services'},
    {'name': 'Accounting & Finance', 'icon': 'calculator', 'description': 'Bookkeeping, accounting, tax preparation, financial planning'},
    {'name': 'Legal Services', 'icon': 'scale', 'description': 'Legal advice, document drafting, contract review'},
    {'name': 'Administrative Services', 'icon': 'clipboard', 'description': 'Virtual assistance, typing, data entry, documentation'},
    {'name': 'Research & Data', 'icon': 'bar-chart', 'description': 'Research assistance, data analysis, survey creation'},
    {'name': 'Email Marketing', 'icon': 'mail', 'description': 'Email campaigns, newsletter design, automation'},
    {'name': 'Sales & Lead Generation', 'icon': 'target', 'description': 'Lead generation, sales support, CRM management'},
    
    # PERSONAL SERVICES
    {'name': 'Fitness & Training', 'icon': 'activity', 'description': 'Personal training, workout plans, fitness coaching'},
    {'name': 'Nutrition & Diet Planning', 'icon': 'apple', 'description': 'Meal planning, diet consultation, nutrition advice'},
    {'name': 'Beauty Services', 'icon': 'scissors', 'description': 'Hair styling, makeup, nail services, beauty treatments'},
    {'name': 'Massage & Spa', 'icon': 'spa', 'description': 'Massage therapy, spa treatments, relaxation services'},
    {'name': 'Fashion & Styling', 'icon': 'shopping-bag', 'description': 'Personal styling, wardrobe consulting, fashion advice'},
    {'name': 'Counseling & Mentorship', 'icon': 'users', 'description': 'Career counseling, academic mentorship, life coaching'},
    {'name': 'Therapy & Mental Health', 'icon': 'brain', 'description': 'Mental health support, counseling, therapy services'},
    
    # HOME SERVICES
    {'name': 'Cleaning Services', 'icon': 'trash', 'description': 'Room cleaning, laundry services, organizing'},
    {'name': 'Repair & Maintenance', 'icon': 'wrench', 'description': 'Phone repair, laptop repair, electronics fixing'},
    {'name': 'Plumbing Services', 'icon': 'droplet', 'description': 'Plumbing repairs, installations, maintenance'},
    {'name': 'Electrical Services', 'icon': 'zap', 'description': 'Electrical repairs, wiring, installations'},
    {'name': 'Carpentry & Woodwork', 'icon': 'hammer', 'description': 'Furniture making, repairs, custom woodwork'},
    {'name': 'Painting & Decorating', 'icon': 'paint-brush', 'description': 'Interior/exterior painting, wall decoration'},
    {'name': 'Pest Control', 'icon': 'bug', 'description': 'Pest removal, fumigation, prevention services'},
    {'name': 'Landscaping & Gardening', 'icon': 'leaf', 'description': 'Garden maintenance, landscaping, lawn care'},
    {'name': 'HVAC Services', 'icon': 'wind', 'description': 'Air conditioning, heating, ventilation services'},
    {'name': 'Moving & Relocation', 'icon': 'truck', 'description': 'Moving services, packing, furniture transport'},
    
    # EVENT SERVICES
    {'name': 'Event Planning', 'icon': 'calendar', 'description': 'Party planning, event coordination, decoration services'},
    {'name': 'Catering Services', 'icon': 'utensils-crossed', 'description': 'Event catering, meal prep, food services'},
    {'name': 'DJ & Entertainment', 'icon': 'disc', 'description': 'DJ services, MC hosting, entertainment services'},
    {'name': 'Wedding Services', 'icon': 'heart', 'description': 'Wedding planning, coordination, vendor management'},
    {'name': 'Decoration Services', 'icon': 'sparkles', 'description': 'Event decoration, balloon art, setup services'},
    
    # TRANSPORTATION & DELIVERY
    {'name': 'Transportation', 'icon': 'car', 'description': 'Ride services, delivery services, moving assistance'},
    {'name': 'Delivery Services', 'icon': 'package', 'description': 'Package delivery, courier services, logistics'},
    {'name': 'Driver Services', 'icon': 'steering-wheel', 'description': 'Personal driver, chauffeur services'},
    
    # LESSONS & COACHING
    {'name': 'Music Lessons', 'icon': 'music', 'description': 'Instrument lessons, vocal training, music theory'},
    {'name': 'Dance Lessons', 'icon': 'user-dance', 'description': 'Dance classes, choreography, performance training'},
    {'name': 'Art Lessons', 'icon': 'palette', 'description': 'Drawing, painting, sculpture, art classes'},
    {'name': 'Sports Coaching', 'icon': 'trophy', 'description': 'Sports training, coaching, skill development'},
    {'name': 'Driving Lessons', 'icon': 'car-front', 'description': 'Driving instruction, license preparation'},
    
    # PET SERVICES
    {'name': 'Pet Care', 'icon': 'paw', 'description': 'Pet sitting, walking, grooming, and care services'},
    {'name': 'Veterinary Services', 'icon': 'stethoscope', 'description': 'Pet health care, vet consultations, treatment'},
    {'name': 'Pet Training', 'icon': 'dog', 'description': 'Pet training, behavior modification, obedience classes'},
    
    # MISCELLANEOUS SERVICES
    {'name': 'Printing Services', 'icon': 'printer', 'description': 'Document printing, binding, large format printing'},
    {'name': 'Rental Services', 'icon': 'key', 'description': 'Equipment rental, space rental, item lending'},
    {'name': 'Security Services', 'icon': 'shield-check', 'description': 'Security guards, surveillance, safety consulting'},
    {'name': 'Insurance Services', 'icon': 'umbrella', 'description': 'Insurance consultation, policy management'},
    {'name': 'Real Estate Services', 'icon': 'building', 'description': 'Property listing, rental assistance, real estate advice'},
    {'name': 'Astrology & Spiritual', 'icon': 'star', 'description': 'Astrology readings, spiritual guidance, fortune telling'},
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
                self.stdout.write(self.style.SUCCESS(f"Created: {category.name}"))
            else:
                # Update existing categories
                category.icon = cat_data['icon']
                category.description = cat_data['description']
                category.is_active = True
                category.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Updated: {category.name}"))

        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Summary:"))
        self.stdout.write(self.style.SUCCESS(f"Created: {created_count} categories"))
        self.stdout.write(self.style.SUCCESS(f"Updated: {updated_count} categories"))
        self.stdout.write(self.style.SUCCESS(f"Total: {Category.objects.count()} categories"))
        self.stdout.write(self.style.SUCCESS(f"\nProduct Categories: ~50"))
        self.stdout.write(self.style.SUCCESS(f"Service Categories: ~70"))
        self.stdout.write(self.style.SUCCESS(f"Total Categories in Script: {len(categories_data)}"))