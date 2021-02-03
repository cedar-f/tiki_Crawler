from crawler import Crawler

list_link_to_accessories = ['https://www.thegioididong.com/sac-dtdd#m:0&o:3&i:3',
                  'https://www.thegioididong.com/sac-cap#m:0&o:3&i:14',
                  'https://www.thegioididong.com/tai-nghe#m:0&o:3&i:7',
                  'https://www.thegioididong.com/loa-laptop#m:0&o:3&i:3',
                  'https://www.thegioididong.com/the-nho-dien-thoai', 'https://www.thegioididong.com/usb',
                  'https://www.thegioididong.com/o-cung-di-dong',
                  'https://www.thegioididong.com/chuot-ban-phim#m:0&o:3&i:2',
                  'https://www.thegioididong.com/mieng-dan-op-lung#m:0&o:3&i:5',
                  'https://www.thegioididong.com/tui-chong-soc#m:0&o:3&i:1',
                  'https://www.thegioididong.com/camera-giam-sat',
                  'https://www.thegioididong.com/thiet-bi-mang#m:0&o:3&i:2',
                  'https://www.thegioididong.com/phu-kien-oto',
                  'https://www.thegioididong.com/may-tinh-cam-tay',
                  'https://www.thegioididong.com/thiet-bi-nha-thong-minh',
                  'https://www.thegioididong.com/thiet-bi-thong-minh',
                  'https://www.thegioididong.com/do-choi-dien-thoai#m:0&o:3&i:6',
                  'https://www.thegioididong.com/phu-kien-thong-minh', 'https://www.thegioididong.com/phan-mem']

app = Crawler(list_link_to_accessories)

app.run()
