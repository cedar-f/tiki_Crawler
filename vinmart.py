from crawler import Crawler

list_cat = ['/Thịt%20-%20Hải%20sản%20-%20Trứng-c11707', '/Rau%20-%20Củ%20-%20Trái%20cây-c11708',
            '/Dầu%20ăn%20-%20Gia%20vị%20-%20Đồ%20khô-c11709', '/Thực%20phẩm%20đông%20lạnh-c11710',
            '/Sữa%20-%20Sản%20phẩm%20từ%20sữa-c11726', '/Bánh%20kẹo%20-%20Đồ%20ăn%20vặt-c14854',
            '/Hóa%20phẩm%20-%20Giấy-c11711', '/Đồ%20uống%20-%20Giải%20khát-c11712']

app = Crawler('https://vinmart.com',list_cat)

app.run()
