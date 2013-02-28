### Từ gói cài đặt cho các bản phân phối Linux thông dụng

Đây là cách đơn giản nhất.

* Tải file [deb](https://github.com/BoGoEngine/ibus-bogo-python/downloads) cho Ubuntu/Debian/Mint và cài đặt bằng lệnh:

        sudo dpkg -i <tên file deb>

    Hoặc thêm [ppa:ndtrung4419/bogo](https://launchpad.net/~ndtrung4419/+archive/bogo)
và cài gói `ibus-bogo`:

        sudo add-apt-repository ppa:ndtrung4419/bogo 
        sudo apt-get update 
        sudo apt-get install ibus-bogo

* File AUR cho [Arch Linux](https://aur.archlinux.org/packages/ibus-bogo/) (đóng góp của bạn [Ngô Huy](https://github.com/NgoHuy))
* Fedora (Đang cập nhật)

**NOTE** Nếu bạn muốn đóng gói BoGo cho các bản phân phối khác thì hãy xem 
hướng dẫn trong file [PACKAGING.md](https://github.com/BoGoEngine/ibus-bogo-python/blob/master/README.md)
Sau đó đừng ngần ngại thông báo với chúng tôi để trang hướng dẫn này được cập nhật liên tục cho các bản phân phối mới nhất.
:D

### Từ mã nguồn

IBus BoGo Engine được xây dựng có sử dụng các thành phần sau, hãy chắc
chắn rằng các thành phần này đã được cài trên máy nếu bạn cần cài đặt
từ mã nguồn:

* ibus 1.4
* python 3.2
* python-gobject (pygobject)
* gir1.2-ibus-1.0 (gobject introspection data)

Tải mã nguồn tại [đây](https://github.com/BoGoEngine/ibus-bogo-python/tags).

Giải nén và chạy lệnh sau để cài đặt:

    mkdir build && cd build
    cmake .. && make install

Gỡ cài đặt:

    cd build && sudo make uninstall

### Cấu hình sau khi cài đặt (optional)

Để đảm bảo chương trình vận hành như ý muốn. Thêm các dòng sau vào
file ~/.profile sau đó logout và login:
    
    export GTK_IM_MODULE=ibus
    export XMODIFIERS=@im=ibus
    export QT_IM_MODULE=xim
